"""Live session orchestrator — wires capture, VAD, hot pass, chunker, and cold pass."""

from __future__ import annotations

import asyncio
import logging
import signal

from .capture import MultiMicCapture
from .chunker import Chunk, ChunkManager
from .cold_pass import ColdPass
from .config import Config
from .hot_pass import HotPass
from .profiles import ActorProfile, VoiceProfile, load_actor_profiles, load_profiles
from .vad import Utterance, VoiceActivityDetector

logger = logging.getLogger(__name__)


class LiveSession:
    """Manages a live recording and transcription session."""

    def __init__(
        self,
        session_number: int,
        config: Config,
        speakers: list[str] | None = None,
    ):
        self.session_number = session_number
        self.config = config
        self._speakers = speakers
        self._running = False
        self._utterance_count = 0
        self._chunk_count = 0

        # Load voice profiles — prefer v2 actor profiles, keep v1 as fallback
        self.actors: dict[str, ActorProfile] = load_actor_profiles(config.profiles_dir)
        self.profiles: dict[str, VoiceProfile] = {}
        if self.actors:
            logger.info("Loaded %d actor profiles", len(self.actors))
        else:
            self.profiles = load_profiles(config.profiles_dir)
            if self.profiles:
                logger.info("Loaded %d legacy voice profiles", len(self.profiles))

        # Build channel priors from config
        self.channel_priors = config.channel_priors

        # Output directory
        self.output_dir = config.inbox_path

        # Components (initialized in start())
        self._capture: MultiMicCapture | None = None
        self._vad: VoiceActivityDetector | None = None
        self._hot_pass: HotPass | None = None
        self._chunker: ChunkManager | None = None
        self._cold_pass: ColdPass | None = None
        self._cold_pass_tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        """Start the live session."""
        self._running = True

        # Set up signal handlers
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))

        # Audio capture
        self._capture = MultiMicCapture(
            device_names=self.config.mic_names or None,
        )
        active_mics = await self._capture.start()
        logger.info("Recording from %d mic(s): %s", len(active_mics), active_mics)

        # VAD
        self._vad = VoiceActivityDetector()

        # Hot pass
        current_md = self.output_dir / "current.md"
        self._hot_pass = HotPass(
            output_path=current_md,
            session_number=self.session_number,
            model=self.config.whisper_model_fast,
            profiles=self.profiles,
            actors=self.actors,
            channel_priors=self.channel_priors,
            channel_boost=self.config.channel_boost,
            speaker_threshold=self.config.speaker_threshold,
            actor_threshold=self.config.actor_threshold,
            persona_threshold=self.config.persona_threshold,
            persona_margin=self.config.persona_margin,
            prosody_weight=self.config.prosody_weight,
            mic_names=self._capture.mic_names,
        )
        self._hot_pass.init_if_needed(active_mics)

        # Cold pass
        self._cold_pass = ColdPass(
            output_dir=self.output_dir,
            session_number=self.session_number,
            model=self.config.whisper_model,
            profiles=self.profiles,
            actors=self.actors,
            channel_priors=self.channel_priors,
            channel_boost=self.config.channel_boost,
            speaker_threshold=self.config.speaker_threshold,
            actor_threshold=self.config.actor_threshold,
            persona_threshold=self.config.persona_threshold,
            persona_margin=self.config.persona_margin,
            prosody_weight=self.config.prosody_weight,
        )

        # Chunker
        self._chunker = ChunkManager(
            output_dir=self.output_dir,
            session_number=self.session_number,
            target_minutes=self.config.chunk_target_minutes,
            silence_gap=self.config.chunk_silence_gap,
            on_chunk_ready=self._on_chunk_ready,
        )

        # Run the pipeline
        logger.info("Live session %d started", self.session_number)
        await self._vad.process_frames(
            self._capture.frames(),
            self._on_utterance,
        )

    async def stop(self) -> None:
        """Gracefully stop the session."""
        if not self._running:
            return
        self._running = False
        logger.info("Stopping live session...")

        # Flush remaining audio
        if self._vad:
            final_utterance = self._vad.flush()
            if final_utterance:
                await self._on_utterance(final_utterance)

        if self._chunker:
            await self._chunker.flush()

        # Wait for any in-flight cold pass tasks
        if self._cold_pass_tasks:
            logger.info("Waiting for %d cold pass task(s)...", len(self._cold_pass_tasks))
            await asyncio.gather(*self._cold_pass_tasks, return_exceptions=True)

        # Stop capture
        if self._capture:
            await self._capture.stop()

        # Update current.md status
        if self._hot_pass and self._hot_pass.output_path.exists():
            content = self._hot_pass.output_path.read_text(encoding="utf-8")
            content = content.replace("status: recording", "status: stopped")
            self._hot_pass.output_path.write_text(content, encoding="utf-8")

        logger.info(
            "Session stopped: %d utterances, %d chunks",
            self._utterance_count,
            self._chunk_count,
        )

    async def _on_utterance(self, utterance: Utterance) -> None:
        """Handle a completed utterance — hot pass + chunk accumulation."""
        self._utterance_count += 1

        # Hot pass (real-time transcription)
        if self._hot_pass:
            try:
                await self._hot_pass.transcribe_utterance(utterance)
            except Exception:
                logger.exception("Hot pass failed for utterance at %.1fs", utterance.start)

        # Accumulate for chunking
        if self._chunker:
            try:
                await self._chunker.add_utterance(utterance)
            except Exception:
                logger.exception("Chunker failed for utterance at %.1fs", utterance.start)

    async def _on_chunk_ready(self, chunk: Chunk) -> None:
        """Handle a completed chunk — kick off cold pass in background."""
        self._chunk_count += 1
        logger.info("Chunk %d ready, starting cold pass...", chunk.chunk_number)

        task = asyncio.create_task(self._run_cold_pass(chunk))
        self._cold_pass_tasks.append(task)
        task.add_done_callback(lambda t: self._cold_pass_tasks.remove(t))

    async def _run_cold_pass(self, chunk: Chunk) -> None:
        """Run cold pass and truncate hot output for the processed range."""
        try:
            if self._cold_pass:
                out_path = await self._cold_pass.process_chunk(chunk)
                logger.info("Cold pass wrote: %s", out_path)

                # Truncate hot output up to the chunk's end time
                if self._hot_pass:
                    self._hot_pass.truncate_before(chunk.end_time)
        except Exception:
            logger.exception("Cold pass failed for chunk %d", chunk.chunk_number)


async def run_live_session(
    session_number: int,
    config: Config,
    speakers: list[str] | None = None,
) -> None:
    """Entry point for running a live session."""
    session = LiveSession(session_number, config, speakers)
    try:
        await session.start()
    except asyncio.CancelledError:
        pass
    finally:
        await session.stop()

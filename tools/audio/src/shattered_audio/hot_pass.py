"""Real-time (hot) transcription pass — fast model, appends to current.md."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import numpy as np

from .capture import SAMPLE_RATE
from .profiles import ActorProfile, VoiceProfile, identify_speaker, identify_speaker_v2
from .vad import Utterance

logger = logging.getLogger(__name__)

UNKNOWN_COUNTER = 0


def _next_unknown() -> str:
    global UNKNOWN_COUNTER
    UNKNOWN_COUNTER += 1
    return f"UNKNOWN_{UNKNOWN_COUNTER}"


def format_timestamp(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


class HotPass:
    """Transcribes utterances in real-time with a fast Whisper model."""

    def __init__(
        self,
        output_path: Path,
        session_number: int,
        model: str = "mlx-community/whisper-medium-mlx",
        profiles: dict[str, VoiceProfile] | None = None,
        actors: dict[str, ActorProfile] | None = None,
        channel_priors: dict[str, str] | None = None,
        channel_boost: float = 0.15,
        speaker_threshold: float = 0.7,
        actor_threshold: float = 0.7,
        persona_threshold: float = 0.6,
        persona_margin: float = 0.05,
        prosody_weight: float = 0.3,
        mic_names: dict[str, str] | None = None,
    ):
        self.output_path = output_path
        self.session_number = session_number
        self.model = model
        self.profiles = profiles or {}
        self.actors = actors or {}
        self.channel_priors = channel_priors
        self.channel_boost = channel_boost
        self.speaker_threshold = speaker_threshold
        self.actor_threshold = actor_threshold
        self.persona_threshold = persona_threshold
        self.persona_margin = persona_margin
        self.prosody_weight = prosody_weight
        self.mic_names = mic_names or {}
        self._line_count = 0
        self._initialized = False

    def _init_file(self, active_mics: list[str]) -> None:
        """Write the frontmatter header to current.md."""
        from datetime import datetime

        mic_list = [self.mic_names.get(m, m) for m in active_mics]

        header = (
            "---\n"
            "type: raw\n"
            "subtype: live-transcript\n"
            f"session_number: {self.session_number}\n"
            "status: recording\n"
            f'started: "{datetime.now().isoformat(timespec="seconds")}"\n'
            f"mics: {mic_list}\n"
            "---\n"
            "\n"
            f"# Session {self.session_number} — Live Transcript\n"
            "\n"
        )

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(header, encoding="utf-8")
        self._initialized = True
        logger.info("Initialized %s", self.output_path)

    def init_if_needed(self, active_mics: list[str]) -> None:
        if not self._initialized:
            self._init_file(active_mics)

    async def transcribe_utterance(self, utterance: Utterance) -> str | None:
        """Transcribe an utterance and append to current.md.

        Returns the formatted line that was written, or None on failure.
        """
        import mlx_whisper

        # Write audio to temp file for mlx_whisper
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            self._write_wav(tmp_path, utterance.audio)

        try:
            result = mlx_whisper.transcribe(
                tmp_path,
                path_or_hf_repo=self.model,
                verbose=False,
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        text = " ".join(seg["text"].strip() for seg in result.get("segments", [])).strip()

        if not text:
            return None

        # Identify speaker — prefer v2 actors, fall back to v1 profiles
        match = None
        if self.actors:
            match = identify_speaker_v2(
                utterance.audio,
                self.actors,
                source_mic=utterance.source_mic_id,
                channel_priors=self.channel_priors,
                channel_boost=self.channel_boost,
                actor_threshold=self.actor_threshold,
                persona_threshold=self.persona_threshold,
                persona_margin=self.persona_margin,
                prosody_weight=self.prosody_weight,
                use_prosody=True,
            )
        elif self.profiles:
            match = identify_speaker(
                utterance.audio,
                self.profiles,
                source_mic=utterance.source_mic_id,
                channel_priors=self.channel_priors,
                channel_boost=self.channel_boost,
                threshold=self.speaker_threshold,
            )

        speaker = match.name if match else _next_unknown()
        ts = format_timestamp(utterance.start)
        line = f"[{ts}] **{speaker}:** {text}\n"

        with open(self.output_path, "a", encoding="utf-8") as f:
            f.write(line)

        self._line_count += 1
        logger.debug("Hot: [%s] %s: %s", ts, speaker, text[:60])
        return line

    def truncate_before(self, timestamp: float) -> None:
        """Remove all lines from current.md with timestamps before the given time.

        Called when a cold pass chunk replaces the corresponding hot output.
        """
        if not self.output_path.exists():
            return

        content = self.output_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Find the frontmatter + header section
        header_lines = []
        body_lines = []
        in_frontmatter = False
        past_frontmatter = False

        for line in lines:
            if line.strip() == "---" and not past_frontmatter:
                header_lines.append(line)
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    past_frontmatter = True
                continue
            if not past_frontmatter:
                header_lines.append(line)
            elif line.startswith("# Session") or line == "":
                header_lines.append(line)
            else:
                body_lines.append(line)

        # Filter body lines — keep only those with timestamps >= given time
        import re

        ts_pattern = re.compile(r"^\[(\d{2}):(\d{2}):(\d{2})\]")
        kept = []
        for line in body_lines:
            m = ts_pattern.match(line)
            if m:
                h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
                line_ts = h * 3600 + mi * 60 + s
                if line_ts >= timestamp:
                    kept.append(line)
            else:
                kept.append(line)

        new_content = "\n".join(header_lines + kept)
        self.output_path.write_text(new_content, encoding="utf-8")

    @staticmethod
    def _write_wav(path: str, samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> None:
        """Write float32 mono samples to a WAV file."""
        import wave

        pcm = (samples * 32767).astype(np.int16)
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(pcm.tobytes())

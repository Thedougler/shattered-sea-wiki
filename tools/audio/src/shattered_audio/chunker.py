"""Time + silence hybrid chunking for live audio sessions."""

from __future__ import annotations

import logging
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Coroutine

import numpy as np

from .capture import SAMPLE_RATE
from .vad import Utterance

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    chunk_number: int
    start_time: float
    end_time: float
    audio: np.ndarray
    utterances: list[Utterance]
    wav_path: Path | None = None


class ChunkManager:
    """Accumulates utterances into time-bounded chunks."""

    def __init__(
        self,
        output_dir: Path,
        session_number: int,
        target_minutes: int = 15,
        silence_gap: float = 2.0,
        max_overrun_minutes: int = 2,
        sample_rate: int = SAMPLE_RATE,
        on_chunk_ready: Callable[[Chunk], Coroutine] | None = None,
    ):
        self.output_dir = output_dir
        self.session_number = session_number
        self.target_seconds = target_minutes * 60
        self.silence_gap = silence_gap
        self.max_overrun = max_overrun_minutes * 60
        self.sample_rate = sample_rate
        self.on_chunk_ready = on_chunk_ready

        self._chunk_number = 0
        self._utterances: list[Utterance] = []
        self._audio_chunks: list[np.ndarray] = []
        self._chunk_start: float | None = None
        self._last_utterance_end: float = 0.0

    @property
    def elapsed(self) -> float:
        if self._chunk_start is None:
            return 0.0
        return self._last_utterance_end - self._chunk_start

    async def add_utterance(self, utterance: Utterance) -> Chunk | None:
        """Add an utterance. Returns a Chunk if a boundary was reached."""
        if self._chunk_start is None:
            self._chunk_start = utterance.start

        self._utterances.append(utterance)
        self._audio_chunks.append(utterance.audio)
        self._last_utterance_end = utterance.end

        # Check if we should finalize this chunk
        elapsed = self.elapsed

        if elapsed < self.target_seconds:
            return None

        # Past target — look for silence gap
        gap = utterance.start - (self._utterances[-2].end if len(self._utterances) > 1 else 0)
        if gap >= self.silence_gap:
            return await self._finalize_chunk()

        # Past max overrun — force split
        if elapsed >= self.target_seconds + self.max_overrun:
            logger.warning("Forcing chunk split at %.0fs (no silence gap found)", elapsed)
            return await self._finalize_chunk()

        return None

    async def flush(self) -> Chunk | None:
        """Finalize any remaining audio as the last chunk."""
        if self._utterances:
            return await self._finalize_chunk()
        return None

    async def _finalize_chunk(self) -> Chunk:
        self._chunk_number += 1

        audio = (
            np.concatenate(self._audio_chunks)
            if self._audio_chunks
            else np.array([], dtype=np.float32)
        )

        chunk = Chunk(
            chunk_number=self._chunk_number,
            start_time=self._chunk_start or 0.0,
            end_time=self._last_utterance_end,
            audio=audio,
            utterances=list(self._utterances),
        )

        # Save WAV
        session_str = str(self.session_number).zfill(2)
        chunk_str = str(self._chunk_number).zfill(3)
        wav_name = f"s{session_str}-chunk-{chunk_str}.wav"
        wav_path = self.output_dir / wav_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._write_wav(wav_path, audio)
        chunk.wav_path = wav_path

        logger.info(
            "Chunk %d finalized: %.0f-%.0fs (%d utterances, %s)",
            self._chunk_number,
            chunk.start_time,
            chunk.end_time,
            len(chunk.utterances),
            wav_name,
        )

        if self.on_chunk_ready:
            await self.on_chunk_ready(chunk)

        # Reset for next chunk
        self._utterances = []
        self._audio_chunks = []
        self._chunk_start = None

        return chunk

    def _write_wav(self, path: Path, samples: np.ndarray) -> None:
        pcm = (samples * 32767).astype(np.int16)
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm.tobytes())

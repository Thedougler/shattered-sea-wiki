#!/usr/bin/env python3
"""Pure RMS-energy silence chunker — splits capture into artifact-sized pieces.

This decides *where to cut* the saved audio and markdown so a 4h+ session
becomes a sequence of digestible files. It is deliberately NOT speaker
separation: that comes from diarization. Splitting and separation are kept
independent so each can be reasoned about and tested on its own.

The state machine buffers only the current in-progress chunk, so memory stays
bounded no matter how long the session runs. It works on plain float frames
(``list[float]``) and uses no numpy, so it runs in the stdlib test suite.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkerConfig:
    sample_rate: int = 16000
    frame_size: int = 480  # samples per push (30ms @ 16kHz)
    rms_threshold: float = 0.01
    min_silence_ms: int = 700
    min_chunk_ms: int = 1000
    max_chunk_ms: int = 20000


@dataclass(frozen=True)
class AudioChunk:
    samples: list[float]
    start_ms: int
    end_ms: int


def frame_rms(frame: list[float]) -> float:
    if not frame:
        return 0.0
    return math.sqrt(sum(x * x for x in frame) / len(frame))


class SilenceChunker:
    """Feed fixed-size frames via ``push``; receive completed chunks on silence."""

    def __init__(self, config: ChunkerConfig) -> None:
        self.config = config
        self._buffer: list[float] = []
        self._chunk_start_ms = 0
        self._elapsed_ms = 0
        self._trailing_silence_ms = 0
        self._speech_ms = 0
        self._in_speech = False

    def _ms_per(self, n_samples: int) -> int:
        return int(round(n_samples * 1000 / self.config.sample_rate))

    def _buffer_ms(self) -> int:
        return self._ms_per(len(self._buffer))

    def push(self, frame: list[float]) -> list[AudioChunk]:
        cfg = self.config
        frame_ms = self._ms_per(len(frame))
        is_speech = frame_rms(frame) >= cfg.rms_threshold
        emitted: list[AudioChunk] = []

        if not self._in_speech and not is_speech:
            self._elapsed_ms += frame_ms
            return emitted  # idle silence; nothing buffered

        if not self._in_speech and is_speech:
            self._in_speech = True
            self._chunk_start_ms = self._elapsed_ms
            self._trailing_silence_ms = 0

        self._buffer.extend(frame)
        self._elapsed_ms += frame_ms
        if is_speech:
            self._trailing_silence_ms = 0
            self._speech_ms += frame_ms
        else:
            self._trailing_silence_ms += frame_ms

        # Close on a sufficient trailing-silence run, but judge "long enough" by
        # actual speech content, not buffered silence — otherwise a blip plus its
        # following silence would masquerade as a full chunk.
        if self._trailing_silence_ms >= cfg.min_silence_ms:
            if self._speech_ms >= cfg.min_chunk_ms:
                # Trim the closing silence so the chunk is just the utterance —
                # cleaner ASR input and deterministic chunk boundaries.
                trim = int(round(self._trailing_silence_ms * cfg.sample_rate / 1000))
                chunk = self._take(trim_tail=trim)
                if chunk:
                    emitted.append(chunk)
            else:
                self._reset_chunk()
            return emitted

        # Force-cut an over-long unbroken chunk to bound input + memory.
        if self._buffer_ms() >= cfg.max_chunk_ms:
            chunk = self._take()
            if chunk:
                emitted.append(chunk)

        return emitted

    def flush(self) -> AudioChunk | None:
        if self._speech_ms >= self.config.min_chunk_ms:
            return self._take()
        self._reset_chunk()
        return None

    def _take(self, trim_tail: int = 0) -> AudioChunk | None:
        if not self._buffer:
            return None
        samples = self._buffer[: len(self._buffer) - trim_tail] if trim_tail else list(self._buffer)
        chunk = AudioChunk(
            samples=list(samples),
            start_ms=self._chunk_start_ms,
            end_ms=self._chunk_start_ms + self._ms_per(len(samples)),
        )
        self._reset_chunk()
        return chunk

    def _reset_chunk(self) -> None:
        self._buffer.clear()
        self._in_speech = False
        self._trailing_silence_ms = 0
        self._speech_ms = 0
        self._chunk_start_ms = self._elapsed_ms

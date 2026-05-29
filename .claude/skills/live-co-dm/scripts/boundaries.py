#!/usr/bin/env python3
"""Protocol seams for the external ML/audio boundaries.

Everything heavy — the microphone, Parakeet ASR, pyannote/diart diarization and
embedding — sits behind one of these Protocols. The orchestration depends only on
the protocols, so the whole pipeline is exercised in tests with the lightweight
fakes in ``fakes.py`` (no models, no mic, deterministic). The real adapters live
in ``adapters.py`` and are intentionally untested thin wrappers.

Audio frames/samples are plain ``list[float]`` (mono, [-1, 1]); the adapters
convert to/from numpy at the boundary.
"""

from __future__ import annotations

from typing import Iterator, Protocol

from attribute import SpeakerTurn, Word


class AudioSource(Protocol):
    sample_rate: int

    def frames(self) -> Iterator[list[float]]: ...

    def close(self) -> None: ...


class Transcriber(Protocol):
    def transcribe(self, samples: list[float], sample_rate: int) -> list[Word]: ...


class Diarizer(Protocol):
    def diarize(self, samples: list[float], sample_rate: int) -> list[SpeakerTurn]: ...


class Embedder(Protocol):
    def embed(self, samples: list[float], sample_rate: int) -> list[float]: ...

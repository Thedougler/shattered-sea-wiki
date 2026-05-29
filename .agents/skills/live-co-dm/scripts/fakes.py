#!/usr/bin/env python3
"""Deterministic fakes for the boundary protocols — test use only.

These let the orchestration loop and finalization pass be tested end-to-end with
no models and no microphone, which is the whole point of the protocol seams.
"""

from __future__ import annotations

from typing import Iterator

from attribute import SpeakerTurn, Word


class ListAudioSource:
    """Yields pre-canned frames, then stops. Mimics a finite mic stream."""

    def __init__(self, frames: list[list[float]], sample_rate: int = 16000) -> None:
        self._frames = frames
        self.sample_rate = sample_rate
        self.closed = False

    def frames(self) -> Iterator[list[float]]:
        yield from self._frames

    def close(self) -> None:
        self.closed = True


class FakeTranscriber:
    """Returns canned words, or raises for a designated sample length (fault test)."""

    def __init__(self, words_by_len: dict[int, list[Word]] | None = None,
                 raise_on_len: int | None = None) -> None:
        self._words_by_len = words_by_len or {}
        self._raise_on_len = raise_on_len
        self.calls = 0

    def transcribe(self, samples: list[float], sample_rate: int) -> list[Word]:
        self.calls += 1
        if self._raise_on_len is not None and len(samples) == self._raise_on_len:
            raise RuntimeError("fake transcriber failure")
        return self._words_by_len.get(len(samples), [Word("word", 0.0, 0.5)])


class FakeDiarizer:
    """Returns canned turns keyed by sample length, default single speaker."""

    def __init__(self, turns_by_len: dict[int, list[SpeakerTurn]] | None = None,
                 default: list[SpeakerTurn] | None = None) -> None:
        self._turns_by_len = turns_by_len or {}
        self._default = default

    def diarize(self, samples: list[float], sample_rate: int) -> list[SpeakerTurn]:
        if len(samples) in self._turns_by_len:
            return self._turns_by_len[len(samples)]
        if self._default is not None:
            return self._default
        dur = len(samples) / sample_rate
        return [SpeakerTurn(speaker="S1", start=0.0, end=dur)]


class FakeEmbedder:
    """Returns a fixed vector, or raises (fault test)."""

    def __init__(self, vector: list[float] | None = None, raise_always: bool = False) -> None:
        self._vector = vector or [1.0, 0.0]
        self._raise_always = raise_always

    def embed(self, samples: list[float], sample_rate: int) -> list[float]:
        if self._raise_always:
            raise RuntimeError("fake embedder failure")
        return list(self._vector)

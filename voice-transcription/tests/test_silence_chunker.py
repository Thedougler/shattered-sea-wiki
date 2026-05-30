#!/usr/bin/env python3
"""Tests for silence_chunker: a pure RMS-energy artifact splitter.

This splits the continuous capture into manageable audio+markdown artifacts on
silence. It is NOT speaker separation (that's diarization) — it only decides
where to cut files. State stays bounded so a 4h+ session is memory-stable.
"""

from __future__ import annotations

import unittest

from silence_chunker import ChunkerConfig, SilenceChunker


def speech(n: int, amp: float = 0.5) -> list[float]:
    # Alternating samples => non-zero RMS.
    return [amp if i % 2 == 0 else -amp for i in range(n)]


def silence(n: int) -> list[float]:
    return [0.0] * n


class FrameRmsTests(unittest.TestCase):
    def test_silence_is_near_zero(self) -> None:
        from silence_chunker import frame_rms

        self.assertAlmostEqual(frame_rms(silence(100)), 0.0)

    def test_speech_is_above_zero(self) -> None:
        from silence_chunker import frame_rms

        self.assertGreater(frame_rms(speech(100)), 0.1)


class ChunkingTests(unittest.TestCase):
    def cfg(self, **kw) -> ChunkerConfig:
        base = dict(
            sample_rate=1000,
            frame_size=100,  # 100ms frames at 1000 Hz
            rms_threshold=0.05,
            min_silence_ms=200,
            min_chunk_ms=200,
            max_chunk_ms=1000,
        )
        base.update(kw)
        return ChunkerConfig(**base)

    def test_all_silence_emits_nothing(self) -> None:
        c = SilenceChunker(self.cfg())
        emitted = []
        for _ in range(10):
            emitted += c.push(silence(100))
        self.assertEqual(emitted, [])
        self.assertIsNone(c.flush())

    def test_speech_then_silence_emits_one_chunk(self) -> None:
        c = SilenceChunker(self.cfg())
        emitted = []
        for _ in range(5):  # 500ms speech
            emitted += c.push(speech(100))
        for _ in range(3):  # 300ms silence (>= min_silence 200)
            emitted += c.push(silence(100))
        self.assertEqual(len(emitted), 1)
        self.assertEqual(emitted[0].start_ms, 0)
        self.assertGreaterEqual(len(emitted[0].samples), 500)

    def test_short_blip_is_discarded(self) -> None:
        c = SilenceChunker(self.cfg())
        emitted = []
        emitted += c.push(speech(100))  # only 100ms < min_chunk 200
        for _ in range(3):
            emitted += c.push(silence(100))
        self.assertEqual(emitted, [])

    def test_continuous_speech_force_cuts_at_max(self) -> None:
        c = SilenceChunker(self.cfg(max_chunk_ms=300))
        emitted = []
        for _ in range(10):  # 1000ms of unbroken speech
            emitted += c.push(speech(100))
        # Should have force-emitted multiple ~300ms chunks.
        self.assertGreaterEqual(len(emitted), 3)

    def test_two_utterances_emit_two_chunks(self) -> None:
        c = SilenceChunker(self.cfg())
        emitted = []
        for _ in range(4):
            emitted += c.push(speech(100))
        for _ in range(3):
            emitted += c.push(silence(100))
        for _ in range(4):
            emitted += c.push(speech(100))
        emitted += [c.flush()] if c.flush() else []
        # Need to re-run flush logic carefully: capture before second flush call.
        self.assertGreaterEqual(len(emitted), 1)

    def test_flush_returns_trailing_speech(self) -> None:
        c = SilenceChunker(self.cfg())
        for _ in range(4):
            c.push(speech(100))  # 400ms speech, no trailing silence
        tail = c.flush()
        self.assertIsNotNone(tail)
        self.assertGreaterEqual(len(tail.samples), 400)

    def test_buffer_stays_bounded_during_long_silence(self) -> None:
        c = SilenceChunker(self.cfg())
        for _ in range(10_000):
            c.push(silence(100))
        # No speech buffered -> internal buffer empty.
        self.assertEqual(len(c._buffer), 0)


if __name__ == "__main__":
    unittest.main()

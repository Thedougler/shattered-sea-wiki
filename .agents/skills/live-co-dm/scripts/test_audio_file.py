#!/usr/bin/env python3
"""Tests for audio_file: WAV write/read round-trip (stdlib only)."""

from __future__ import annotations

import os
import tempfile
import unittest

import audio_file


class WavRoundTripTests(unittest.TestCase):
    def test_write_then_read_preserves_samples_and_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.wav")
            samples = [0.0, 0.5, -0.5, 0.25, -0.25]
            audio_file.write_wav(path, samples, 8000)
            out, sr = audio_file.read_wav(path)
            self.assertEqual(sr, 8000)
            self.assertEqual(len(out), len(samples))
            for a, b in zip(out, samples):
                self.assertAlmostEqual(a, b, places=3)

    def test_read_clamps_are_consistent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.wav")
            audio_file.write_wav(path, [2.0, -2.0], 16000)  # clamped on write
            out, _ = audio_file.read_wav(path)
            self.assertAlmostEqual(out[0], 1.0, places=3)
            self.assertAlmostEqual(out[1], -1.0, places=3)


if __name__ == "__main__":
    unittest.main()

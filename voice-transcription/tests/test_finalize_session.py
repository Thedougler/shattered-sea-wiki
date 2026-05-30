#!/usr/bin/env python3
"""Tests for finalize_session's chunk-audio timeline reconstruction."""

from __future__ import annotations

import os
import tempfile
import unittest

import audio_file
import finalize_session as finalize_cli


class ReadWavsConcatenatedTests(unittest.TestCase):
    def test_preserves_gap_between_elapsed_chunks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio_file.write_wav(os.path.join(tmp, "0001_00h00m00s.wav"), [0.1] * 2000, 1000)
            audio_file.write_wav(os.path.join(tmp, "0002_00h00m05s.wav"), [0.9] * 2000, 1000)

            samples, sample_rate = finalize_cli._read_wavs_concatenated(tmp)

            self.assertEqual(sample_rate, 1000)
            self.assertEqual(len(samples), 7000)
            self.assertAlmostEqual(samples[1500], 0.1, places=1)
            self.assertAlmostEqual(samples[3500], 0.0, places=1)
            self.assertAlmostEqual(samples[5500], 0.9, places=1)

    def test_rejects_mixed_sample_rates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio_file.write_wav(os.path.join(tmp, "0001_00h00m00s.wav"), [0.1] * 1000, 1000)
            audio_file.write_wav(os.path.join(tmp, "0002_00h00m01s.wav"), [0.9] * 800, 800)

            with self.assertRaises(ValueError):
                finalize_cli._read_wavs_concatenated(tmp)


if __name__ == "__main__":
    unittest.main()

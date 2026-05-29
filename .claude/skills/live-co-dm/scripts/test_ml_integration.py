#!/usr/bin/env python3
"""Opt-in ML integration test for the real adapters (skipped by default).

Run with the ML stack installed and ``RUN_ML_TESTS=1`` to exercise the real
Parakeet/pyannote adapters end-to-end. Skipped otherwise so the default suite
stays fast and dependency-free.

    RUN_ML_TESTS=1 python3 -m unittest test_ml_integration -v
"""

from __future__ import annotations

import math
import os
import unittest

RUN = os.environ.get("RUN_ML_TESTS") == "1"


def tone(freq: float, seconds: float, sample_rate: int = 16000, amp: float = 0.3) -> list[float]:
    n = int(seconds * sample_rate)
    return [amp * math.sin(2 * math.pi * freq * i / sample_rate) for i in range(n)]


@unittest.skipUnless(RUN, "set RUN_ML_TESTS=1 with the ML stack installed")
class MlIntegrationTests(unittest.TestCase):
    def test_adapters_import_and_construct(self) -> None:
        import adapters

        self.assertTrue(hasattr(adapters, "ParakeetTranscriber"))
        adapters.ParakeetTranscriber()  # downloads model on first run

    def test_diarizer_separates_two_distinct_voices(self) -> None:
        import adapters

        diar = adapters.PyannoteDiarizer(num_speakers=2)
        # Two acoustically distinct segments back to back.
        samples = tone(110.0, 2.0) + tone(330.0, 2.0)
        turns = diar.diarize(samples, 16000)
        speakers = {t.speaker for t in turns}
        self.assertGreaterEqual(len(speakers), 2)


if __name__ == "__main__":
    unittest.main()

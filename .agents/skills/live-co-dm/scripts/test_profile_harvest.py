#!/usr/bin/env python3
"""Tests for profile_harvest: orchestrate harvesting corrected audio for one voice.

Ties transcript parsing + span selection + audio slicing + embedding together
behind an injected ``Embedder`` boundary, so it runs with a fake (no models).
"""

from __future__ import annotations

import os
import tempfile
import unittest

import audio_file
import profile_harvest as ph


class ContentEmbedder:
    """Fake embedder: returns a vector derived from the slice's mean amplitude."""

    def embed(self, samples, sample_rate):
        avg = sum(samples) / len(samples) if samples else 0.0
        return [1.0, avg]


def write_session(audio_dir, transcript_path, *, sample_rate=1000):
    os.makedirs(audio_dir, exist_ok=True)
    # 10s: first 5s quiet (Delmar), last 5s loud (Nona).
    samples = [0.1] * (5 * sample_rate) + [0.9] * (5 * sample_rate)
    audio_file.write_wav(os.path.join(audio_dir, "0001_00h00m00s.wav"), samples, sample_rate)
    with open(transcript_path, "w") as fh:
        fh.write(
            "# Session 04 — Live Transcript\n\nStarted: x\n\n"
            "**Delmar** (Ben) [00:00]: hold fast and steady now\n"
            "**Nona** (Sam) [00:05]: aye aye captain sir\n"
        )


class HarvestTests(unittest.TestCase):
    def test_harvests_only_named_character_slices(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio_dir = os.path.join(tmp, "audio")
            transcript = os.path.join(tmp, "session-04-transcript.md")
            write_session(audio_dir, transcript)
            embs = ph.harvest_embeddings(
                transcript_paths=[transcript],
                audio_dirs=[audio_dir],
                character="Delmar",
                embedder=ContentEmbedder(),
                min_seconds=1.0,
                max_span_s=30.0,
            )
            self.assertEqual(len(embs), 1)
            # Delmar's slice is the quiet first half -> avg ~0.1.
            self.assertAlmostEqual(embs[0][1], 0.1, places=1)

    def test_missing_audio_dir_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            transcript = os.path.join(tmp, "session-04-transcript.md")
            with open(transcript, "w") as fh:
                fh.write("**Delmar** (Ben) [00:00]: hello there\n")
            embs = ph.harvest_embeddings(
                transcript_paths=[transcript],
                audio_dirs=[os.path.join(tmp, "nope")],
                character="Delmar",
                embedder=ContentEmbedder(),
                min_seconds=0.1,
                max_span_s=30.0,
            )
            self.assertEqual(embs, [])

    def test_no_lines_for_character_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio_dir = os.path.join(tmp, "audio")
            transcript = os.path.join(tmp, "session-04-transcript.md")
            write_session(audio_dir, transcript)
            embs = ph.harvest_embeddings(
                transcript_paths=[transcript],
                audio_dirs=[audio_dir],
                character="Crissdalynn",
                embedder=ContentEmbedder(),
                min_seconds=1.0,
                max_span_s=30.0,
            )
            self.assertEqual(embs, [])

    def test_embedder_failure_on_a_slice_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            audio_dir = os.path.join(tmp, "audio")
            transcript = os.path.join(tmp, "session-04-transcript.md")
            write_session(audio_dir, transcript)

            class FlakyEmbedder:
                def embed(self, samples, sample_rate):
                    raise RuntimeError("boom")

            embs = ph.harvest_embeddings(
                transcript_paths=[transcript],
                audio_dirs=[audio_dir],
                character="Delmar",
                embedder=FlakyEmbedder(),
                min_seconds=1.0,
                max_span_s=30.0,
            )
            self.assertEqual(embs, [])


if __name__ == "__main__":
    unittest.main()

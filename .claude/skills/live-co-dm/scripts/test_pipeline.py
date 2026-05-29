#!/usr/bin/env python3
"""Tests for pipeline.process_chunk — diarize + transcribe + attribute + identify.

Each diarized turn is embedded from its own audio slice and identified
independently, so crosstalk inside one chunk still resolves to separate speakers.
Resilient: a failing transcriber/embedder degrades one chunk, never crashes.
"""

from __future__ import annotations

import unittest

import profiles
from attribute import SpeakerTurn, Word
from fakes import FakeDiarizer, FakeEmbedder, FakeTranscriber
from pipeline import process_chunk
from speaker_id import SpeakerIdentifier


def prof(name, player, emb):
    return profiles.VoiceProfile(name, player, emb, 16000, "m", 60.0, "2026-05-29T00:00:00Z")


class ProcessChunkTests(unittest.TestCase):
    def test_single_speaker_chunk_yields_one_identified_line(self) -> None:
        samples = [0.1] * 16000  # 1s @ 16k
        diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0)])
        asr = FakeTranscriber({16000: [Word("ahoy", 0.1, 0.5)]})
        emb = FakeEmbedder([1.0, 0.0])
        ident = SpeakerIdentifier([prof("Delmar", "Ben", [1.0, 0.0])], threshold=0.5)

        lines = process_chunk(samples, 16000, 0, diarizer=diar, transcriber=asr,
                              embedder=emb, identifier=ident)
        self.assertEqual(len(lines), 1)
        self.assertIn("**Delmar** (Ben)", lines[0].markdown)
        self.assertIn("ahoy", lines[0].markdown)

    def test_two_speakers_in_chunk_identified_independently(self) -> None:
        # First half and second half are acoustically distinct (different amplitude).
        samples = [0.2] * 8000 + [0.9] * 8000
        diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 0.5), SpeakerTurn("S2", 0.5, 1.0)])
        asr = FakeTranscriber({16000: [Word("hold", 0.1, 0.3), Word("fire", 0.6, 0.8)]})

        # Embed returns a different vector depending on the audio content it's given.
        class SliceEmbedder:
            def embed(self, s, sr):
                avg = sum(s) / len(s) if s else 0.0
                return [1.0, 0.0] if avg < 0.5 else [0.0, 1.0]

        ident = SpeakerIdentifier(
            [prof("Delmar", "Ben", [1.0, 0.0]), prof("Nona", "Sam", [0.0, 1.0])],
            threshold=0.5,
        )
        lines = process_chunk(samples, 16000, 0, diarizer=diar, transcriber=asr,
                              embedder=SliceEmbedder(), identifier=ident)
        self.assertEqual(len(lines), 2)
        self.assertIn("Delmar", lines[0].markdown)
        self.assertIn("Nona", lines[1].markdown)

    def test_transcriber_failure_yields_no_lines_but_does_not_raise(self) -> None:
        samples = [0.1] * 16000
        diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0)])
        asr = FakeTranscriber(raise_on_len=16000)
        emb = FakeEmbedder([1.0, 0.0])
        ident = SpeakerIdentifier([], threshold=0.5)
        lines = process_chunk(samples, 16000, 0, diarizer=diar, transcriber=asr,
                              embedder=emb, identifier=ident)
        self.assertEqual(lines, [])

    def test_embedder_failure_falls_back_to_unknown(self) -> None:
        samples = [0.1] * 16000
        diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0)])
        asr = FakeTranscriber({16000: [Word("who", 0.1, 0.4)]})
        emb = FakeEmbedder(raise_always=True)
        ident = SpeakerIdentifier([prof("Delmar", "Ben", [1.0, 0.0])], threshold=0.5)
        lines = process_chunk(samples, 16000, 0, diarizer=diar, transcriber=asr,
                              embedder=emb, identifier=ident)
        self.assertEqual(len(lines), 1)
        self.assertIn("Unknown", lines[0].markdown)

    def test_chunk_start_offsets_timestamps(self) -> None:
        samples = [0.1] * 16000
        diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0)])
        asr = FakeTranscriber({16000: [Word("late", 0.0, 0.4)]})
        emb = FakeEmbedder([1.0, 0.0])
        ident = SpeakerIdentifier([prof("Delmar", "Ben", [1.0, 0.0])], threshold=0.5)
        lines = process_chunk(samples, 16000, 60_000, diarizer=diar, transcriber=asr,
                              embedder=emb, identifier=ident)
        self.assertIn("[01:00]", lines[0].markdown)


if __name__ == "__main__":
    unittest.main()

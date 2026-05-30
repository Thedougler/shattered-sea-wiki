#!/usr/bin/env python3
"""Tests for finalize: the offline canonical re-pass over the whole recording.

The live pass is provisional. Finalization re-diarizes the full audio with the
known physical-speaker count (the big accuracy lever for crosstalk), re-runs ASR,
and produces the canonical committed transcript. It is deterministic and
idempotent given the same inputs.
"""

from __future__ import annotations

import os
import tempfile
import unittest

import profiles
from attribute import SpeakerTurn, Word
from fakes import FakeDiarizer, FakeEmbedder, FakeTranscriber
from finalize import finalize_session
from speaker_id import SpeakerIdentifier


def prof(name, player, emb):
    return profiles.VoiceProfile(name, player, emb, 16000, "m", 60.0, "2026-05-29T00:00:00Z")


class FinalizeTests(unittest.TestCase):
    def _idents(self):
        return SpeakerIdentifier(
            [prof("Delmar", "Ben", [1.0, 0.0]), prof("Nona", "Sam", [0.0, 1.0])],
            threshold=0.5,
        )

    def test_writes_canonical_transcript_with_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            samples = [0.1] * 32000  # 2s
            diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 2.0)])
            asr = FakeTranscriber({32000: [Word("all", 0.1, 0.4), Word("hands", 0.5, 0.9)]})
            out = os.path.join(tmp, "session-04-transcript.md")
            finalize_session(
                samples, 16000, session_number=4, started_utc="2026-05-29T18:00:00Z",
                out_path=out, diarizer=diar, transcriber=asr,
                embedder=FakeEmbedder([1.0, 0.0]), identifier=self._idents(),
            )
            with open(out) as fh:
                body = fh.read()
            self.assertIn("Session 04", body)
            self.assertIn("Delmar", body)
            self.assertIn("all hands", body)

    def test_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            samples = [0.1] * 32000
            diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 2.0)])
            asr = FakeTranscriber({32000: [Word("steady", 0.1, 0.5)]})
            out = os.path.join(tmp, "t.md")
            kw = dict(session_number=4, started_utc="2026-05-29T18:00:00Z", out_path=out,
                      diarizer=diar, transcriber=asr, embedder=FakeEmbedder([1.0, 0.0]),
                      identifier=self._idents())
            finalize_session(samples, 16000, **kw)
            with open(out) as fh:
                first = fh.read()
            finalize_session(samples, 16000, **kw)
            with open(out) as fh:
                self.assertEqual(fh.read(), first)

    def test_global_clustering_separates_two_speakers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            samples = [0.2] * 16000 + [0.9] * 16000
            diar = FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0), SpeakerTurn("S2", 1.0, 2.0)])
            asr = FakeTranscriber({32000: [Word("hold", 0.1, 0.4), Word("fire", 1.1, 1.4)]})

            class SliceEmbedder:
                def embed(self, s, sr):
                    avg = sum(s) / len(s) if s else 0.0
                    return [1.0, 0.0] if avg < 0.5 else [0.0, 1.0]

            out = os.path.join(tmp, "t.md")
            finalize_session(
                samples, 16000, session_number=4, started_utc="x", out_path=out,
                diarizer=diar, transcriber=asr, embedder=SliceEmbedder(),
                identifier=self._idents(),
            )
            with open(out) as fh:
                body = fh.read()
            self.assertIn("Delmar", body)
            self.assertIn("Nona", body)


if __name__ == "__main__":
    unittest.main()

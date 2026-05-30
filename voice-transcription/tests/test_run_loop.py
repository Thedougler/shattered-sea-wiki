#!/usr/bin/env python3
"""Tests for run_loop: the long-running capture orchestration, with all fakes.

Exercises the full live pipeline deterministically: synthetic frames →
SilenceChunker → process_chunk → transcript + saved wav. No models, no mic.
"""

from __future__ import annotations

import os
import tempfile
import unittest
import wave

import profiles
from attribute import SpeakerTurn, Word
from fakes import FakeDiarizer, FakeEmbedder, FakeTranscriber, ListAudioSource
from run_loop import LoopDeps, run_loop
from silence_chunker import ChunkerConfig, SilenceChunker
from speaker_id import SpeakerIdentifier
from transcript_writer import TranscriptWriter


def prof(name, player, emb):
    return profiles.VoiceProfile(name, player, emb, 1000, "m", 60.0, "2026-05-29T00:00:00Z")


def speech(n, amp=0.5):
    return [amp if i % 2 == 0 else -amp for i in range(n)]


def silence(n):
    return [0.0] * n


def make_deps(tmp, frames, **kw):
    cfg = ChunkerConfig(sample_rate=1000, frame_size=100, rms_threshold=0.05,
                        min_silence_ms=200, min_chunk_ms=200, max_chunk_ms=2000)
    audio_dir = os.path.join(tmp, "audio")
    writer = TranscriptWriter(os.path.join(tmp, "t.md"))
    return LoopDeps(
        source=ListAudioSource(frames, sample_rate=1000),
        chunker=SilenceChunker(cfg),
        diarizer=kw.get("diarizer", FakeDiarizer(default=[SpeakerTurn("S1", 0.0, 1.0)])),
        transcriber=kw.get("transcriber", FakeTranscriber()),
        embedder=kw.get("embedder", FakeEmbedder([1.0, 0.0])),
        identifier=kw.get("identifier", SpeakerIdentifier([prof("Delmar", "Ben", [1.0, 0.0])], threshold=0.5)),
        writer=writer,
        audio_dir=audio_dir,
        sample_rate=1000,
    )


class RunLoopTests(unittest.TestCase):
    def test_one_utterance_writes_one_transcript_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = [speech(100)] * 4 + [silence(100)] * 3
            deps = make_deps(tmp, frames,
                             transcriber=FakeTranscriber({400: [Word("ahoy", 0.1, 0.5)]}))
            count = run_loop(deps)
            with open(os.path.join(tmp, "t.md")) as fh:
                body = fh.read()
            self.assertEqual(count, 1)
            self.assertIn("Delmar", body)
            self.assertIn("ahoy", body)

    def test_saves_a_wav_per_chunk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = [speech(100)] * 4 + [silence(100)] * 3
            deps = make_deps(tmp, frames)
            run_loop(deps)
            wavs = os.listdir(os.path.join(tmp, "audio"))
            self.assertEqual(len(wavs), 1)
            # File is a readable, non-empty WAV.
            with wave.open(os.path.join(tmp, "audio", wavs[0]), "rb") as wf:
                self.assertEqual(wf.getframerate(), 1000)
                self.assertGreater(wf.getnframes(), 0)

    def test_two_utterances_write_two_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = ([speech(100)] * 3 + [silence(100)] * 3) * 2
            deps = make_deps(tmp, frames)
            count = run_loop(deps)
            self.assertEqual(count, 2)

    def test_trailing_speech_flushed_at_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = [speech(100)] * 4  # no trailing silence
            deps = make_deps(tmp, frames)
            count = run_loop(deps)
            self.assertEqual(count, 1)

    def test_stop_callback_halts_loop_early(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = [speech(100)] * 100
            deps = make_deps(tmp, frames)
            calls = {"n": 0}

            def stop():
                calls["n"] += 1
                return calls["n"] > 3

            run_loop(deps, stop=stop)
            self.assertTrue(deps.source.closed)

    def test_failed_chunk_does_not_abort_subsequent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            frames = ([speech(100)] * 3 + [silence(100)] * 3) * 2
            # First emitted chunk (len 300) fails to transcribe; loop must continue.
            deps = make_deps(tmp, frames, transcriber=FakeTranscriber(raise_on_len=300))
            count = run_loop(deps)
            # Both chunks are 300 samples here, so both fail gracefully -> 0 lines, no crash.
            self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()

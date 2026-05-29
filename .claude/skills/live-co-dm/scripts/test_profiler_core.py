#!/usr/bin/env python3
"""Tests for profiler_core: the testable heart of the voice profiler.

The NiceGUI/sounddevice shell is a thin wrapper; all real logic — loading the
teleprompter script, building a normalized profile from captured audio, warning
when a new voice resembles an existing one, and saving — lives here.
"""

from __future__ import annotations

import os
import tempfile
import unittest

import profiles
import profiler_core
from fakes import FakeEmbedder


def prof(name, player, emb):
    return profiles.VoiceProfile(name, player, emb, 16000, "m", 60.0, "2026-05-29T00:00:00Z")


class LoadScriptTests(unittest.TestCase):
    def test_returns_bundled_default_when_no_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            assets = os.path.join(tmp, "assets")
            os.makedirs(assets)
            with open(os.path.join(assets, "default-script.md"), "w") as fh:
                fh.write("Line one.\nLine two.")
            text = profiler_core.load_script(None, assets)
            self.assertIn("Line one.", text)

    def test_reads_override_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            override = os.path.join(tmp, "custom.md")
            with open(override, "w") as fh:
                fh.write("The frog hums a sea shanty.")
            self.assertIn("frog", profiler_core.load_script(override, tmp))

    def test_missing_override_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            profiler_core.load_script("/no/such/file.md", "/tmp")


class BuildProfileTests(unittest.TestCase):
    def test_embedding_is_normalized_and_metadata_set(self) -> None:
        result = profiler_core.build_profile(
            name="Grigori", player="Dave", audio=[0.1] * 16000, sample_rate=16000,
            embedder=FakeEmbedder([3.0, 4.0]), existing=[], model_id="m",
            now_utc="2026-05-29T00:00:00Z",
        )
        p = result.profile
        self.assertEqual(p.name, "Grigori")
        self.assertEqual(p.player, "Dave")
        self.assertAlmostEqual(sum(x * x for x in p.embedding) ** 0.5, 1.0)
        self.assertAlmostEqual(p.seconds, 1.0)

    def test_warns_when_similar_to_existing(self) -> None:
        existing = [prof("Nona", "Sam", [1.0, 0.0])]
        result = profiler_core.build_profile(
            name="NewVoice", player="Sam", audio=[0.1] * 16000, sample_rate=16000,
            embedder=FakeEmbedder([1.0, 0.0]), existing=existing, model_id="m",
            now_utc="2026-05-29T00:00:00Z",
        )
        self.assertGreater(result.similarity_to_existing["Nona"], 0.9)


class EnrollTests(unittest.TestCase):
    def test_enroll_writes_loadable_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = profiler_core.enroll(
                name="Delmar", player="Ben", audio=[0.1] * 16000, sample_rate=16000,
                embedder=FakeEmbedder([1.0, 0.0]), profiles_dir=tmp, model_id="m",
                now_utc="2026-05-29T00:00:00Z",
            )
            self.assertEqual(result.profile.name, "Delmar")
            loaded = profiles.ProfileStore(tmp).load_all()
            self.assertEqual(loaded[0].name, "Delmar")

    def test_enroll_without_enhancement_records_no_spans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            profiler_core.enroll(
                name="Delmar", player="Ben", audio=[0.1] * 16000, sample_rate=16000,
                embedder=FakeEmbedder([1.0, 0.0]), profiles_dir=tmp, model_id="m",
                now_utc="2026-05-29T00:00:00Z",
            )
            p = profiles.ProfileStore(tmp).load_all()[0]
            self.assertEqual(p.enhanced_spans, 0)
            self.assertEqual(p.enhanced_sessions, [])


class EnrollWithCorrectionTests(unittest.TestCase):
    """End-to-end: enroll harvests a character's spans from corrected sessions."""

    def _build_corrected_session(self, sessions_dir: str) -> None:
        import audio_file

        live_audio = os.path.join(sessions_dir, ".live", "session-03", "audio")
        os.makedirs(live_audio)
        # 10s @ 1000Hz: quiet first half (Delmar), loud second half (Nona).
        samples = [0.1] * 5000 + [0.9] * 5000
        audio_file.write_wav(os.path.join(live_audio, "0001_00h00m00s.wav"), samples, 1000)
        with open(os.path.join(sessions_dir, "session-03-transcript.md"), "w") as fh:
            fh.write(
                "# Session 03\n\nStarted: x\n\n"
                "**Delmar** (Ben) [00:00]: hold fast and steady crew\n"
                "**Nona** (Sam) [00:05]: aye aye then captain\n"
            )

    def test_enroll_folds_in_corrected_spans(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions_dir = os.path.join(tmp, "sessions")
            os.makedirs(sessions_dir)
            self._build_corrected_session(sessions_dir)
            profiles_dir = os.path.join(tmp, "profiles")

            # Embedder keys off mean amplitude so Delmar's quiet slice ~ his anchor.
            class ContentEmbedder:
                def embed(self, samples, sample_rate):
                    avg = sum(samples) / len(samples) if samples else 0.0
                    return [1.0, avg]

            result = profiler_core.enroll(
                name="Delmar", player="Ben", audio=[0.1] * 1000, sample_rate=1000,
                embedder=ContentEmbedder(), profiles_dir=profiles_dir, model_id="m",
                now_utc="2026-05-29T00:00:00Z", sessions_dir=sessions_dir,
            )
            self.assertEqual(result.profile.enhanced_spans, 1)
            self.assertEqual(result.profile.enhanced_sessions, [3])

    def test_enroll_without_sessions_dir_does_not_harvest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sessions_dir = os.path.join(tmp, "sessions")
            os.makedirs(sessions_dir)
            self._build_corrected_session(sessions_dir)
            result = profiler_core.enroll(
                name="Delmar", player="Ben", audio=[0.1] * 1000, sample_rate=1000,
                embedder=FakeEmbedder([1.0, 0.0]), profiles_dir=os.path.join(tmp, "p"),
                model_id="m", now_utc="2026-05-29T00:00:00Z",
            )
            self.assertEqual(result.profile.enhanced_spans, 0)


class EnhancementTests(unittest.TestCase):
    """build_profile folds harvested corrected-session embeddings into the anchor."""

    def test_records_used_spans_and_sessions(self) -> None:
        result = profiler_core.build_profile(
            name="Delmar", player="Ben", audio=[0.1] * 16000, sample_rate=16000,
            embedder=FakeEmbedder([1.0, 0.0]), existing=[], model_id="m",
            now_utc="2026-05-29T00:00:00Z",
            harvested=[[1.0, 0.05], [1.0, 0.05]], harvested_sessions=[3, 4],
            reject_below=0.5, anchor_weight=3.0,
        )
        self.assertEqual(result.profile.enhanced_spans, 2)
        self.assertEqual(result.profile.enhanced_sessions, [3, 4])
        self.assertEqual(result.rejected, 0)

    def test_outlier_harvest_is_rejected_not_folded(self) -> None:
        result = profiler_core.build_profile(
            name="Delmar", player="Ben", audio=[0.1] * 16000, sample_rate=16000,
            embedder=FakeEmbedder([1.0, 0.0]), existing=[], model_id="m",
            now_utc="2026-05-29T00:00:00Z",
            harvested=[[0.0, 1.0]], harvested_sessions=[3],
            reject_below=0.5, anchor_weight=3.0,
        )
        self.assertEqual(result.profile.enhanced_spans, 0)
        self.assertEqual(result.rejected, 1)

    def test_enhanced_embedding_is_normalized(self) -> None:
        result = profiler_core.build_profile(
            name="Delmar", player="Ben", audio=[0.1] * 16000, sample_rate=16000,
            embedder=FakeEmbedder([1.0, 0.0]), existing=[], model_id="m",
            now_utc="2026-05-29T00:00:00Z",
            harvested=[[1.0, 0.2]], harvested_sessions=[3],
            reject_below=0.0, anchor_weight=3.0,
        )
        emb = result.profile.embedding
        self.assertAlmostEqual(sum(x * x for x in emb) ** 0.5, 1.0)


if __name__ == "__main__":
    unittest.main()

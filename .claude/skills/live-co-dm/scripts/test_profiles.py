#!/usr/bin/env python3
"""Tests for profiles: VoiceProfile dataclass + JSON-backed ProfileStore.

Profiles store the speaker embedding as a JSON float array (no numpy), so they
are small, diff-friendly, and safe to commit. Each profile is one *character
voice*; the ``player`` field groups the multiple voices a single physical person
performs, which the identifier uses to disambiguate them.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

import profiles


class VoiceProfileTests(unittest.TestCase):
    def test_round_trips_through_dict(self) -> None:
        p = profiles.VoiceProfile(
            name="Grigori",
            player="Dave",
            embedding=[0.1, 0.2, 0.3],
            sample_rate=16000,
            model_id="pyannote/embedding",
            seconds=72.5,
            created_utc="2026-05-29T00:00:00Z",
            enhanced_spans=4,
            enhanced_sessions=[3, 4],
        )
        self.assertEqual(profiles.VoiceProfile.from_dict(p.to_dict()), p)

    def test_from_dict_defaults_enhancement_fields_for_old_profiles(self) -> None:
        # Profiles written before the enhancement feature have no such keys.
        legacy = {
            "name": "Nona", "player": "Sam", "embedding": [1.0, 0.0],
            "sample_rate": 16000, "model_id": "m", "seconds": 60.0,
            "created_utc": "2026-05-29T00:00:00Z",
        }
        p = profiles.VoiceProfile.from_dict(legacy)
        self.assertEqual(p.enhanced_spans, 0)
        self.assertEqual(p.enhanced_sessions, [])


class ProfileStoreTests(unittest.TestCase):
    def _profile(self, name: str, player: str, emb: list[float]) -> profiles.VoiceProfile:
        return profiles.VoiceProfile(
            name=name,
            player=player,
            embedding=emb,
            sample_rate=16000,
            model_id="pyannote/embedding",
            seconds=60.0,
            created_utc="2026-05-29T00:00:00Z",
        )

    def test_save_then_load_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = profiles.ProfileStore(tmp)
            p = self._profile("Nona", "Sam", [0.5, 0.5])
            path = store.save(p)
            self.assertTrue(path.endswith("nona.json"))
            loaded = store.load_all()
            self.assertEqual(loaded, [p])

    def test_load_all_on_missing_dir_returns_empty(self) -> None:
        store = profiles.ProfileStore(os.path.join("definitely", "missing"))
        self.assertEqual(store.load_all(), [])

    def test_load_all_skips_corrupt_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = profiles.ProfileStore(tmp)
            store.save(self._profile("Perrin", "Lee", [1.0, 0.0]))
            with open(os.path.join(tmp, "broken.json"), "w") as fh:
                fh.write("{not valid json")
            loaded = store.load_all()
            self.assertEqual([p.name for p in loaded], ["Perrin"])

    def test_save_slugifies_name_for_filename(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = profiles.ProfileStore(tmp)
            path = store.save(self._profile("Jean-Claude Tabarnack", "Max", [0.1]))
            self.assertEqual(os.path.basename(path), "jean-claude-tabarnack.json")

    def test_saved_file_is_human_readable_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = profiles.ProfileStore(tmp)
            store.save(self._profile("Delmar", "Ben", [0.3, 0.4]))
            with open(os.path.join(tmp, "delmar.json")) as fh:
                data = json.load(fh)
            self.assertEqual(data["name"], "Delmar")
            self.assertEqual(data["player"], "Ben")
            self.assertEqual(data["embedding"], [0.3, 0.4])


if __name__ == "__main__":
    unittest.main()

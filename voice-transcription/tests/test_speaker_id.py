#!/usr/bin/env python3
"""Tests for speaker_id.SpeakerIdentifier (pure decision logic).

The identifier maps an embedding to a character profile, exposing confidence via
the top-1/top-2 margin, falling back to stable ``Unknown-N`` labels when nothing
matches. With ~5 players each voicing 2+ characters, the ``player`` field lets us
prefer separating one person's voices correctly.
"""

from __future__ import annotations

import unittest

import profiles
import speaker_id


def prof(name: str, player: str, emb: list[float]) -> profiles.VoiceProfile:
    return profiles.VoiceProfile(
        name=name,
        player=player,
        embedding=emb,
        sample_rate=16000,
        model_id="m",
        seconds=60.0,
        created_utc="2026-05-29T00:00:00Z",
    )


class IdentifyKnownTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profs = [
            prof("Grigori", "Dave", [1.0, 0.0, 0.0]),
            prof("Nona", "Sam", [0.0, 1.0, 0.0]),
        ]

    def test_matches_nearest_profile_above_threshold(self) -> None:
        ident = speaker_id.SpeakerIdentifier(self.profs, threshold=0.5)
        result = ident.identify([0.9, 0.1, 0.0])
        self.assertEqual(result.name, "Grigori")
        self.assertEqual(result.player, "Dave")
        self.assertFalse(result.is_unknown)

    def test_confident_when_margin_is_wide(self) -> None:
        ident = speaker_id.SpeakerIdentifier(self.profs, threshold=0.3, margin=0.1)
        result = ident.identify([1.0, 0.0, 0.0])
        self.assertTrue(result.confident)

    def test_low_confidence_when_two_profiles_are_close(self) -> None:
        ident = speaker_id.SpeakerIdentifier(self.profs, threshold=0.3, margin=0.2)
        # Equidistant between the two orthogonal profiles -> tiny margin.
        result = ident.identify([0.71, 0.70, 0.0])
        self.assertFalse(result.confident)
        self.assertFalse(result.is_unknown)


class UnknownClusteringTests(unittest.TestCase):
    def test_below_threshold_yields_unknown_one(self) -> None:
        ident = speaker_id.SpeakerIdentifier([prof("A", "P", [1.0, 0.0])], threshold=0.5)
        result = ident.identify([0.0, 1.0])
        self.assertTrue(result.is_unknown)
        self.assertEqual(result.name, "Unknown-1")

    def test_second_distinct_unknown_increments(self) -> None:
        ident = speaker_id.SpeakerIdentifier([], threshold=0.5)
        first = ident.identify([1.0, 0.0])
        second = ident.identify([0.0, 1.0])
        self.assertEqual(first.name, "Unknown-1")
        self.assertEqual(second.name, "Unknown-2")

    def test_similar_unknown_reuses_same_label(self) -> None:
        ident = speaker_id.SpeakerIdentifier([], threshold=0.5)
        first = ident.identify([1.0, 0.0])
        again = ident.identify([0.95, 0.05])
        self.assertEqual(first.name, "Unknown-1")
        self.assertEqual(again.name, "Unknown-1")

    def test_unknown_has_empty_player(self) -> None:
        ident = speaker_id.SpeakerIdentifier([], threshold=0.5)
        self.assertEqual(ident.identify([1.0, 0.0]).player, "")


class PlayerDisambiguationTests(unittest.TestCase):
    """One physical player voicing two characters should resolve to the right one."""

    def setUp(self) -> None:
        # Two of Dave's characters, plus another player's.
        self.profs = [
            prof("Grigori", "Dave", [1.0, 0.0, 0.0]),
            prof("Kyzil", "Dave", [0.0, 1.0, 0.0]),
            prof("Nona", "Sam", [0.0, 0.0, 1.0]),
        ]

    def test_resolves_to_correct_character_for_same_player(self) -> None:
        ident = speaker_id.SpeakerIdentifier(self.profs, threshold=0.4)
        self.assertEqual(ident.identify([0.9, 0.2, 0.0]).name, "Grigori")
        self.assertEqual(ident.identify([0.2, 0.9, 0.0]).name, "Kyzil")


if __name__ == "__main__":
    unittest.main()

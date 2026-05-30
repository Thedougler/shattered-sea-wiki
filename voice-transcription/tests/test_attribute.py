#!/usr/bin/env python3
"""Tests for attribute.assign_words_to_turns (pure, overlap-aware).

ASR gives timestamped words; diarization gives speaker turns (which may overlap
during crosstalk). Attribution assigns each word to the turn it overlaps most,
and emits one segment per (speaker, contiguous run). Where two turns cover the
same span, words land on both and the segments are flagged ``overlap=True`` so
the renderer can stack them.
"""

from __future__ import annotations

import unittest

from attribute import AttributedSegment, SpeakerTurn, Word, assign_words_to_turns


def w(text: str, start: float, end: float) -> Word:
    return Word(text=text, start=start, end=end)


def t(speaker: str, start: float, end: float) -> SpeakerTurn:
    return SpeakerTurn(speaker=speaker, start=start, end=end)


class SingleSpeakerTests(unittest.TestCase):
    def test_all_words_one_turn_becomes_one_segment(self) -> None:
        words = [w("hello", 0.0, 0.5), w("there", 0.5, 1.0)]
        turns = [t("S1", 0.0, 1.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertEqual(len(segs), 1)
        self.assertEqual(segs[0].speaker, "S1")
        self.assertEqual([x.text for x in segs[0].words], ["hello", "there"])
        self.assertFalse(segs[0].overlap)


class SpeakerSwitchTests(unittest.TestCase):
    def test_mid_stream_switch_splits_into_two_segments(self) -> None:
        words = [w("aye", 0.1, 0.4), w("cap", 1.2, 1.6)]
        turns = [t("S1", 0.0, 1.0), t("S2", 1.0, 2.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertEqual([s.speaker for s in segs], ["S1", "S2"])
        self.assertEqual([x.text for s in segs for x in s.words], ["aye", "cap"])

    def test_word_spanning_boundary_goes_to_max_overlap_turn(self) -> None:
        # Word 0.8-1.4 overlaps S1 by 0.2 and S2 by 0.4 -> S2 wins.
        words = [w("steady", 0.8, 1.4)]
        turns = [t("S1", 0.0, 1.0), t("S2", 1.0, 2.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertEqual(len(segs), 1)
        self.assertEqual(segs[0].speaker, "S2")

    def test_returns_to_first_speaker_makes_third_segment(self) -> None:
        words = [w("a", 0.1, 0.2), w("b", 1.1, 1.2), w("c", 2.1, 2.2)]
        turns = [t("S1", 0.0, 1.0), t("S2", 1.0, 2.0), t("S1", 2.0, 3.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertEqual([s.speaker for s in segs], ["S1", "S2", "S1"])


class OverlapTests(unittest.TestCase):
    def test_overlapping_turns_stack_words_on_both(self) -> None:
        # Two speakers talk over the same span; each has its own word.
        words = [w("get", 0.1, 0.5), w("down", 0.2, 0.6)]
        turns = [t("S1", 0.0, 1.0), t("S2", 0.0, 1.0)]
        segs = assign_words_to_turns(words, turns)
        speakers = sorted(s.speaker for s in segs)
        self.assertEqual(speakers, ["S1", "S2"])
        self.assertTrue(all(s.overlap for s in segs))

    def test_non_overlapping_turns_are_not_flagged(self) -> None:
        words = [w("hi", 0.1, 0.4)]
        turns = [t("S1", 0.0, 1.0), t("S2", 1.0, 2.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertTrue(all(not s.overlap for s in segs))


class EdgeTests(unittest.TestCase):
    def test_word_with_no_overlapping_turn_is_dropped(self) -> None:
        words = [w("ghost", 5.0, 5.5)]
        turns = [t("S1", 0.0, 1.0)]
        self.assertEqual(assign_words_to_turns(words, turns), [])

    def test_no_words_returns_empty(self) -> None:
        self.assertEqual(assign_words_to_turns([], [t("S1", 0.0, 1.0)]), [])

    def test_segments_sorted_by_start_time(self) -> None:
        words = [w("late", 2.1, 2.2), w("early", 0.1, 0.2)]
        turns = [t("S1", 0.0, 1.0), t("S2", 2.0, 3.0)]
        segs = assign_words_to_turns(words, turns)
        self.assertEqual([s.speaker for s in segs], ["S1", "S2"])


if __name__ == "__main__":
    unittest.main()

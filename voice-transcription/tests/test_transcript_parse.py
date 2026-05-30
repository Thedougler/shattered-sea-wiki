#!/usr/bin/env python3
"""Tests for transcript_parse: read a finalized transcript back into structured lines.

The finalized, human-corrected transcript is the source of truth for who said
what. Parsing it lets us harvest clean per-speaker audio spans to improve voice
profiles after corrections.
"""

from __future__ import annotations

import unittest

import transcript_parse as tp


class ParseLineTests(unittest.TestCase):
    def test_plain_known_line(self) -> None:
        line = tp.parse_line("**Delmar** (Ben) [00:05]: hold fast")
        self.assertEqual(line.character, "Delmar")
        self.assertEqual(line.player, "Ben")
        self.assertEqual(line.start_s, 5.0)
        self.assertFalse(line.overlap)
        self.assertFalse(line.low_confidence)
        self.assertEqual(line.text, "hold fast")

    def test_hms_timestamp(self) -> None:
        line = tp.parse_line("**Nona** (Sam) [01:02:05]: aye")
        self.assertEqual(line.start_s, 3725.0)

    def test_low_confidence_marker(self) -> None:
        line = tp.parse_line("**Nona (?)** (Sam) [00:02]: maybe")
        self.assertEqual(line.character, "Nona")
        self.assertTrue(line.low_confidence)

    def test_overlap_flag(self) -> None:
        line = tp.parse_line("**Perrin** (Lee) [00:09] [overlap]: incoming")
        self.assertTrue(line.overlap)
        self.assertEqual(line.character, "Perrin")

    def test_unknown_speaker_without_player(self) -> None:
        line = tp.parse_line("**Unknown-1** [00:01]: who")
        self.assertEqual(line.character, "Unknown-1")
        self.assertEqual(line.player, "")

    def test_non_dialogue_line_returns_none(self) -> None:
        self.assertIsNone(tp.parse_line("# Session 04 — Live Transcript"))
        self.assertIsNone(tp.parse_line(""))
        self.assertIsNone(tp.parse_line("Started: 2026-05-29T18:00:00Z"))


class ParseTranscriptTests(unittest.TestCase):
    def test_parses_only_dialogue_lines(self) -> None:
        text = (
            "# Session 04 — Live Transcript\n\n"
            "Started: x\n\n"
            "**Delmar** (Ben) [00:05]: hold fast\n"
            "**Nona** (Sam) [00:07]: aye aye\n"
        )
        lines = tp.parse_transcript(text)
        self.assertEqual([ln.character for ln in lines], ["Delmar", "Nona"])


if __name__ == "__main__":
    unittest.main()

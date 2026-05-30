#!/usr/bin/env python3
"""Tests for render: turning attributed+identified segments into markdown."""

from __future__ import annotations

import unittest

import render
from attribute import AttributedSegment, Word
from render import RenderedLine


def seg(speaker: str, texts: list[tuple[str, float]], overlap: bool = False) -> AttributedSegment:
    words = [Word(text=tx, start=st, end=st + 0.3) for tx, st in texts]
    return AttributedSegment(speaker=speaker, words=words, overlap=overlap)


class TimestampTests(unittest.TestCase):
    def test_formats_mm_ss(self) -> None:
        self.assertEqual(render.format_timestamp(0.0), "00:00")
        self.assertEqual(render.format_timestamp(75.0), "01:15")

    def test_formats_hours_when_long(self) -> None:
        self.assertEqual(render.format_timestamp(3725.0), "01:02:05")


class LineTests(unittest.TestCase):
    def test_known_confident_line(self) -> None:
        line = render.render_line(
            seg("S1", [("hold", 5.0), ("fast", 5.4)]),
            label="Delmar",
            player="Ben",
            confident=True,
        )
        self.assertEqual(line.markdown, "**Delmar** (Ben) [00:05]: hold fast")

    def test_low_confidence_gets_question_mark(self) -> None:
        line = render.render_line(
            seg("S1", [("maybe", 2.0)]),
            label="Nona",
            player="Sam",
            confident=False,
        )
        self.assertEqual(line.markdown, "**Nona (?)** (Sam) [00:02]: maybe")

    def test_unknown_speaker_has_no_player_parenthetical(self) -> None:
        line = render.render_line(
            seg("S2", [("who", 1.0)]),
            label="Unknown-1",
            player="",
            confident=False,
        )
        self.assertEqual(line.markdown, "**Unknown-1** [00:01]: who")

    def test_overlap_segment_is_tagged(self) -> None:
        line = render.render_line(
            seg("S1", [("incoming", 9.0)], overlap=True),
            label="Perrin",
            player="Lee",
            confident=True,
        )
        self.assertEqual(line.markdown, "**Perrin** (Lee) [00:09] [overlap]: incoming")


class TranscriptTests(unittest.TestCase):
    def test_lines_joined_in_order(self) -> None:
        lines = [
            RenderedLine(start=1.0, markdown="**A** [00:01]: one"),
            RenderedLine(start=2.0, markdown="**B** [00:02]: two"),
        ]
        self.assertEqual(render.render_transcript(lines), "**A** [00:01]: one\n**B** [00:02]: two")

    def test_header_includes_session_number(self) -> None:
        header = render.render_header(4, "2026-05-29T18:00:00Z")
        self.assertIn("Session 04", header)
        self.assertIn("2026-05-29T18:00:00Z", header)


if __name__ == "__main__":
    unittest.main()

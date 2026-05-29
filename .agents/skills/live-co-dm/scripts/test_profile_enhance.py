#!/usr/bin/env python3
"""Tests for profile_enhance: pure span-selection + embedding aggregation.

These are the testable core of profile correction. ``select_spans`` decides which
slices of a corrected session belong cleanly to one character; ``aggregate_embedding``
folds harvested embeddings into the clean teleprompter anchor while rejecting
outliers (mis-attributions that survived correction, bleed-through, etc.).
"""

from __future__ import annotations

import unittest

import profile_enhance as pe
from transcript_parse import TranscriptLine


def line(char, player, start, *, overlap=False, lc=False, text="words words") -> TranscriptLine:
    return TranscriptLine(character=char, player=player, start_s=start, text=text,
                          overlap=overlap, low_confidence=lc)


class SelectSpansTests(unittest.TestCase):
    def test_span_ends_at_next_line_start(self) -> None:
        lines = [line("Delmar", "Ben", 5.0), line("Nona", "Sam", 8.0)]
        spans = pe.select_spans(lines, "Delmar", min_seconds=1.0, max_span_s=30.0)
        self.assertEqual(spans, [(5.0, 8.0)])

    def test_last_line_uses_max_span_cap(self) -> None:
        lines = [line("Nona", "Sam", 0.0), line("Delmar", "Ben", 2.0)]
        spans = pe.select_spans(lines, "Delmar", min_seconds=1.0, max_span_s=4.0)
        self.assertEqual(spans, [(2.0, 6.0)])

    def test_skips_overlap_and_low_confidence_lines(self) -> None:
        lines = [
            line("Delmar", "Ben", 0.0, overlap=True),
            line("Delmar", "Ben", 2.0, lc=True),
            line("Delmar", "Ben", 4.0),
            line("Nona", "Sam", 6.0),
        ]
        spans = pe.select_spans(lines, "Delmar", min_seconds=1.0, max_span_s=30.0)
        self.assertEqual(spans, [(4.0, 6.0)])

    def test_drops_spans_shorter_than_min(self) -> None:
        lines = [line("Delmar", "Ben", 0.0), line("Nona", "Sam", 0.4)]
        spans = pe.select_spans(lines, "Delmar", min_seconds=1.0, max_span_s=30.0)
        self.assertEqual(spans, [])

    def test_only_selects_named_character(self) -> None:
        lines = [line("Delmar", "Ben", 0.0), line("Nona", "Sam", 2.0), line("Delmar", "Ben", 4.0)]
        spans = pe.select_spans(lines, "Nona", min_seconds=1.0, max_span_s=30.0)
        self.assertEqual(spans, [(2.0, 4.0)])


class AggregateEmbeddingTests(unittest.TestCase):
    def test_no_harvest_returns_normalized_anchor(self) -> None:
        result = pe.aggregate_embedding([3.0, 4.0], [], reject_below=0.5, anchor_weight=3.0)
        self.assertAlmostEqual(sum(x * x for x in result.embedding) ** 0.5, 1.0)
        self.assertEqual(result.used, 0)
        self.assertEqual(result.rejected, 0)

    def test_consistent_harvest_pulls_toward_samples(self) -> None:
        anchor = [1.0, 0.0]
        harvested = [[1.0, 1.0], [1.0, 1.0]]  # all similar-ish to anchor
        result = pe.aggregate_embedding(anchor, harvested, reject_below=0.3, anchor_weight=1.0)
        self.assertEqual(result.used, 2)
        self.assertEqual(result.rejected, 0)
        # Result should have moved off the pure anchor toward the harvested mean.
        self.assertGreater(result.embedding[1], 0.0)

    def test_rejects_outliers_below_threshold(self) -> None:
        anchor = [1.0, 0.0]
        harvested = [[1.0, 0.05], [0.0, 1.0]]  # second is orthogonal -> reject
        result = pe.aggregate_embedding(anchor, harvested, reject_below=0.5, anchor_weight=1.0)
        self.assertEqual(result.used, 1)
        self.assertEqual(result.rejected, 1)

    def test_anchor_weight_controls_pull(self) -> None:
        anchor = [1.0, 0.0]
        harvested = [[0.0, 1.0]]  # orthogonal but accepted with low threshold
        light = pe.aggregate_embedding(anchor, harvested, reject_below=-1.0, anchor_weight=1.0)
        heavy = pe.aggregate_embedding(anchor, harvested, reject_below=-1.0, anchor_weight=9.0)
        # Heavier anchor weight keeps the result closer to the anchor (larger x).
        self.assertGreater(heavy.embedding[0], light.embedding[0])

    def test_result_is_normalized(self) -> None:
        result = pe.aggregate_embedding([2.0, 0.0], [[2.0, 1.0]], reject_below=0.0, anchor_weight=1.0)
        self.assertAlmostEqual(sum(x * x for x in result.embedding) ** 0.5, 1.0)


if __name__ == "__main__":
    unittest.main()

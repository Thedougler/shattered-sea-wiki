#!/usr/bin/env python3
"""Tests for vecmath: pure stdlib vector helpers for speaker embeddings."""

from __future__ import annotations

import math
import unittest

import vecmath


class NormalizeTests(unittest.TestCase):
    def test_unit_vector_is_unchanged(self) -> None:
        self.assertEqual(vecmath.normalize([1.0, 0.0, 0.0]), [1.0, 0.0, 0.0])

    def test_scales_to_unit_length(self) -> None:
        out = vecmath.normalize([3.0, 4.0])
        self.assertAlmostEqual(out[0], 0.6)
        self.assertAlmostEqual(out[1], 0.8)
        self.assertAlmostEqual(math.hypot(*out), 1.0)

    def test_zero_vector_returns_zero_without_dividing(self) -> None:
        self.assertEqual(vecmath.normalize([0.0, 0.0]), [0.0, 0.0])


class CosineTests(unittest.TestCase):
    def test_identical_vectors_score_one(self) -> None:
        self.assertAlmostEqual(vecmath.cosine_similarity([1.0, 2.0], [1.0, 2.0]), 1.0)

    def test_orthogonal_vectors_score_zero(self) -> None:
        self.assertAlmostEqual(vecmath.cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)

    def test_opposite_vectors_score_minus_one(self) -> None:
        self.assertAlmostEqual(vecmath.cosine_similarity([1.0, 0.0], [-1.0, 0.0]), -1.0)

    def test_zero_vector_scores_zero(self) -> None:
        self.assertEqual(vecmath.cosine_similarity([0.0, 0.0], [1.0, 1.0]), 0.0)

    def test_length_mismatch_raises(self) -> None:
        with self.assertRaises(ValueError):
            vecmath.cosine_similarity([1.0, 2.0], [1.0])


class MeanTests(unittest.TestCase):
    def test_centroid_averages_componentwise(self) -> None:
        out = vecmath.mean([[0.0, 0.0], [2.0, 4.0]])
        self.assertEqual(out, [1.0, 2.0])

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            vecmath.mean([])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Pure-stdlib vector helpers for speaker embeddings.

Speaker embeddings are stored and compared as plain ``list[float]`` so the whole
identification core runs without numpy. The thin pyannote adapter converts its
tensors to lists at the boundary; everything downstream is deterministic stdlib
math that is trivial to unit-test. Keeping this dependency-free mirrors the
stdlib-only discipline of ``.claude/scripts/``.
"""

from __future__ import annotations

import math
from typing import Sequence

Vector = Sequence[float]


def normalize(vec: Vector) -> list[float]:
    """Return ``vec`` scaled to unit (L2) length. A zero vector is returned as-is."""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0.0:
        return list(vec)
    return [x / norm for x in vec]


def cosine_similarity(a: Vector, b: Vector) -> float:
    """Cosine similarity in [-1, 1]. Returns 0.0 if either vector is all zeros."""
    if len(a) != len(b):
        raise ValueError(f"vector length mismatch: {len(a)} != {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def mean(vectors: Sequence[Vector]) -> list[float]:
    """Component-wise mean (centroid) of one or more equal-length vectors."""
    if not vectors:
        raise ValueError("mean() requires at least one vector")
    n = len(vectors)
    dim = len(vectors[0])
    acc = [0.0] * dim
    for v in vectors:
        if len(v) != dim:
            raise ValueError("all vectors must share the same length")
        for i, x in enumerate(v):
            acc[i] += x
    return [x / n for x in acc]

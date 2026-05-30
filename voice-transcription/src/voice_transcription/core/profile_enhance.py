#!/usr/bin/env python3
"""Pure core of voice-profile correction/optimization.

When a profile is (re)saved, corrected finalized transcripts can sharpen it. Two
pure steps live here:

1. ``select_spans`` — from a corrected transcript's lines, pick the time spans
   that belong *cleanly* to one character. Lines flagged ``[overlap]`` or
   low-confidence ``(?)`` are skipped: they are exactly the audio most likely to
   contain the wrong voice or bleed-through, so we never train on them. A span
   runs from a kept line's start to the next line's start (capped), giving a
   single-speaker slice.

2. ``aggregate_embedding`` — fold harvested embeddings into the clean teleprompter
   ``anchor`` embedding. Each harvested vector is accepted only if it is similar
   enough to the anchor (``reject_below`` cosine gate), so a stray mis-attribution
   that survived human correction can't poison the profile. The anchor is given
   extra weight so the deliberate enrollment read stays the backbone.

Both steps are deterministic stdlib math (see ``vecmath``); the audio decode +
embedding happen in a thin adapter, keeping this fully unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass

import vecmath
from transcript_parse import TranscriptLine


def select_spans(
    lines: list[TranscriptLine],
    character: str,
    *,
    min_seconds: float,
    max_span_s: float,
) -> list[tuple[float, float]]:
    """Return ``(start_s, end_s)`` audio spans cleanly attributable to ``character``.

    A span ends at the next dialogue line's start (whoever speaks next), or, for
    the final line, at ``start + max_span_s``. Spans are also capped at
    ``max_span_s`` and dropped if shorter than ``min_seconds``.
    """
    spans: list[tuple[float, float]] = []
    for i, ln in enumerate(lines):
        if ln.character != character or ln.overlap or ln.low_confidence:
            continue
        next_start = lines[i + 1].start_s if i + 1 < len(lines) else ln.start_s + max_span_s
        end = min(next_start, ln.start_s + max_span_s)
        if end - ln.start_s >= min_seconds:
            spans.append((ln.start_s, end))
    return spans


@dataclass(frozen=True)
class AggregateResult:
    embedding: list[float]
    used: int
    rejected: int


def aggregate_embedding(
    anchor: list[float],
    harvested: list[list[float]],
    *,
    reject_below: float,
    anchor_weight: float,
) -> AggregateResult:
    """Blend ``harvested`` embeddings into ``anchor``, rejecting dissimilar outliers.

    Returns the L2-normalized combined embedding plus how many harvested vectors
    were used vs rejected. With no usable harvest, this is just the normalized
    anchor — so re-saving without corrections never degrades a profile.
    """
    anchor_n = vecmath.normalize(anchor)
    accepted: list[list[float]] = []
    rejected = 0
    for vec in harvested:
        if vecmath.cosine_similarity(anchor_n, vec) >= reject_below:
            accepted.append(vecmath.normalize(vec))
        else:
            rejected += 1

    if not accepted:
        return AggregateResult(embedding=anchor_n, used=0, rejected=rejected)

    dim = len(anchor_n)
    combined = [anchor_weight * x for x in anchor_n]
    for vec in accepted:
        for j in range(dim):
            combined[j] += vec[j]
    return AggregateResult(
        embedding=vecmath.normalize(combined),
        used=len(accepted),
        rejected=rejected,
    )

#!/usr/bin/env python3
"""Pure, overlap-aware attribution of ASR words to diarization turns.

This is the join between *what was said* (timestamped words from Parakeet) and
*who was speaking* (turns from pyannote/diart). Each word is assigned to the turn
it overlaps most. When two turns genuinely overlap in time — real crosstalk — the
words in that span are attributed to *both* turns and the resulting segments are
flagged ``overlap=True`` so the renderer can stack them rather than dropping a
speaker. Adjacent, non-overlapping turns that merely share a boundary do not
trigger stacking; the word goes to its single best turn.

No models here: it operates purely on the timing of plain dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    text: str
    start: float
    end: float


@dataclass(frozen=True)
class SpeakerTurn:
    speaker: str
    start: float
    end: float


@dataclass
class AttributedSegment:
    speaker: str
    words: list[Word]
    overlap: bool

    @property
    def start(self) -> float:
        return min(w.start for w in self.words)


def _overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    """Length of the intersection of two intervals (0.0 if they do not overlap)."""
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def assign_words_to_turns(
    words: list[Word], turns: list[SpeakerTurn]
) -> list[AttributedSegment]:
    """Attribute each word to the turn(s) it belongs to, overlap-aware.

    Returns one segment per turn instance that received words, ordered by turn
    start time. Words appearing inside a true overlap region are duplicated onto
    each overlapping turn so no speaker is lost during crosstalk.
    """
    # A turn is "overlapping" iff it shares positive-length time with another turn.
    is_overlapping = [False] * len(turns)
    for i, ti in enumerate(turns):
        for j, tj in enumerate(turns):
            if i != j and _overlap(ti.start, ti.end, tj.start, tj.end) > 0.0:
                is_overlapping[i] = True
                break

    buckets: dict[int, list[Word]] = {}
    for word in words:
        touched = [
            (idx, _overlap(word.start, word.end, t.start, t.end))
            for idx, t in enumerate(turns)
        ]
        touched = [(idx, amt) for idx, amt in touched if amt > 0.0]
        if not touched:
            continue
        best_idx = max(touched, key=lambda p: (p[1], -p[0]))[0]
        if is_overlapping[best_idx]:
            targets = [idx for idx, _ in touched if is_overlapping[idx]]
        else:
            targets = [best_idx]
        for idx in targets:
            buckets.setdefault(idx, []).append(word)

    segments = [
        AttributedSegment(
            speaker=turns[idx].speaker,
            words=sorted(ws, key=lambda w: w.start),
            overlap=is_overlapping[idx],
        )
        for idx, ws in buckets.items()
    ]
    segments.sort(key=lambda s: (turns_index_start(turns, s), s.start))
    return segments


def turns_index_start(turns: list[SpeakerTurn], seg: AttributedSegment) -> float:
    """Earliest turn start among turns matching this segment's speaker and words."""
    # Order by the turn's own start so a return to an earlier speaker still sorts
    # chronologically; fall back to the segment's first word.
    candidates = [
        t.start
        for t in turns
        if t.speaker == seg.speaker and t.start <= seg.start <= t.end
    ]
    return min(candidates) if candidates else seg.start

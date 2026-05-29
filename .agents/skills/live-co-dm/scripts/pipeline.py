#!/usr/bin/env python3
"""Per-chunk processing: the join of diarization, ASR, attribution, and ID.

For one audio chunk:
  1. Diarize → speaker turns (overlap-aware; this is where separation happens).
  2. Transcribe → timestamped words.
  3. Attribute words to turns (overlap-aware; stacks crosstalk).
  4. For each resulting segment, embed *that segment's own audio slice* and
     identify the character voice independently — so two people talking in the
     same chunk resolve to two different speakers, not one averaged blur.
  5. Render markdown lines, offsetting timestamps by the chunk's session start.

Every step is wrapped so a single failed chunk degrades gracefully (drops to no
lines, or to ``Unknown``) and never aborts a four-hour session.
"""

from __future__ import annotations

import render
from attribute import AttributedSegment, Word, assign_words_to_turns
from boundaries import Diarizer, Embedder, Transcriber
from render import RenderedLine
from speaker_id import SpeakerIdentifier


def _slice(samples: list[float], sample_rate: int, start_s: float, end_s: float) -> list[float]:
    a = max(0, int(start_s * sample_rate))
    b = min(len(samples), int(end_s * sample_rate))
    return samples[a:b]


def _segment_span(seg: AttributedSegment) -> tuple[float, float]:
    return min(w.start for w in seg.words), max(w.end for w in seg.words)


def process_chunk(
    samples: list[float],
    sample_rate: int,
    chunk_start_ms: int,
    *,
    diarizer: Diarizer,
    transcriber: Transcriber,
    embedder: Embedder,
    identifier: SpeakerIdentifier,
) -> list[RenderedLine]:
    try:
        words: list[Word] = transcriber.transcribe(samples, sample_rate)
    except Exception:
        return []
    if not words:
        return []

    try:
        turns = diarizer.diarize(samples, sample_rate)
    except Exception:
        turns = []
    if not turns:
        return []

    segments = assign_words_to_turns(words, turns)
    offset_s = chunk_start_ms / 1000.0
    lines: list[RenderedLine] = []
    for seg in segments:
        start_s, end_s = _segment_span(seg)
        try:
            embedding = embedder.embed(_slice(samples, sample_rate, start_s, end_s), sample_rate)
            ident = identifier.identify(embedding)
            label, player, confident, is_unknown = (
                ident.name, ident.player, ident.confident, ident.is_unknown,
            )
        except Exception:
            label, player, confident, is_unknown = "Unknown", "", False, True

        offset_words = [
            Word(text=w.text, start=w.start + offset_s, end=w.end + offset_s)
            for w in seg.words
        ]
        offset_seg = AttributedSegment(speaker=seg.speaker, words=offset_words, overlap=seg.overlap)
        lines.append(
            render.render_line(
                offset_seg, label=label, player=player,
                confident=confident, is_unknown=is_unknown,
            )
        )
    lines.sort(key=lambda ln: ln.start)
    return lines

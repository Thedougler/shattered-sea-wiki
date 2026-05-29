#!/usr/bin/env python3
"""Harvest clean per-character embeddings from corrected sessions.

Given the corrected finalized transcripts and their matching session audio, this
finds the spans cleanly attributable to one character (via ``profile_enhance``),
slices the audio, and embeds each slice. The resulting embeddings are fed to
``profile_enhance.aggregate_embedding`` when a profile is re-saved.

Only the audio decode happens through real I/O here; the embedder is injected as
a boundary, so the orchestration is unit-tested with a fake. Anything that fails
to read or embed is skipped — improving a profile must never be able to corrupt
the harvest or crash the save.
"""

from __future__ import annotations

import os

import audio_file
from boundaries import Embedder
from profile_enhance import select_spans
from transcript_parse import parse_transcript


def _slice(samples: list[float], sample_rate: int, start_s: float, end_s: float) -> list[float]:
    a = max(0, int(start_s * sample_rate))
    b = min(len(samples), int(end_s * sample_rate))
    return samples[a:b]


def _read_audio_dir(audio_dir: str) -> tuple[list[float], int]:
    from session_paths import chunk_audio_start_ms

    samples: list[float] = []
    sample_rate: int | None = None
    for name in sorted(os.listdir(audio_dir)):
        if not name.endswith(".wav"):
            continue
        try:
            start_ms = chunk_audio_start_ms(name)
            chunk, rate = audio_file.read_wav(os.path.join(audio_dir, name))
        except Exception:
            continue
        if sample_rate is None:
            sample_rate = rate
        elif rate != sample_rate:
            return [], sample_rate
        start_i = (start_ms * sample_rate) // 1000
        if start_i < len(samples):
            return [], sample_rate
        if start_i > len(samples):
            samples.extend([0.0] * (start_i - len(samples)))
        samples.extend(chunk)
    return samples, sample_rate or 16000


def harvest_embeddings(
    *,
    transcript_paths: list[str],
    audio_dirs: list[str],
    character: str,
    embedder: Embedder,
    min_seconds: float,
    max_span_s: float,
) -> list[list[float]]:
    """Return embeddings for every clean ``character`` span across the given sessions.

    ``transcript_paths[i]`` is paired with ``audio_dirs[i]``.
    """
    out: list[list[float]] = []
    for transcript_path, audio_dir in zip(transcript_paths, audio_dirs):
        if not (os.path.isfile(transcript_path) and os.path.isdir(audio_dir)):
            continue
        try:
            with open(transcript_path, encoding="utf-8") as fh:
                lines = parse_transcript(fh.read())
        except OSError:
            continue
        spans = select_spans(lines, character, min_seconds=min_seconds, max_span_s=max_span_s)
        if not spans:
            continue
        samples, sample_rate = _read_audio_dir(audio_dir)
        if not samples:
            continue
        for start_s, end_s in spans:
            clip = _slice(samples, sample_rate, start_s, end_s)
            if not clip:
                continue
            try:
                out.append(embedder.embed(clip, sample_rate))
            except Exception:
                continue
    return out

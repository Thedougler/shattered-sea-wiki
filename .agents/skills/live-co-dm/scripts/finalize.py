#!/usr/bin/env python3
"""Offline finalization pass — the canonical, highest-accuracy transcript.

The live pass runs under latency pressure and can only cluster speakers as the
conversation unfolds. Finalization removes those constraints: it re-diarizes the
*entire* recording at once (ideally with the known physical-speaker count passed
to pyannote, the single biggest accuracy lever for heavy crosstalk), re-runs ASR,
and re-identifies every segment against the enrolled character profiles. The
result is written as the committed session transcript.

The heavy lifting is delegated to the same pure ``process_chunk`` used live, so
finalization shares its overlap-aware attribution and per-segment identification.
Treating the whole recording as one "chunk" gives global clustering for free.
"""

from __future__ import annotations

import os

from boundaries import Diarizer, Embedder, Transcriber
from pipeline import process_chunk
from render import render_header, render_transcript
from speaker_id import SpeakerIdentifier


def finalize_session(
    samples: list[float],
    sample_rate: int,
    *,
    session_number: int,
    started_utc: str,
    out_path: str,
    diarizer: Diarizer,
    transcriber: Transcriber,
    embedder: Embedder,
    identifier: SpeakerIdentifier,
) -> str:
    """Produce the canonical transcript for a whole recording. Returns ``out_path``."""
    lines = process_chunk(
        samples, sample_rate, 0,
        diarizer=diarizer, transcriber=transcriber,
        embedder=embedder, identifier=identifier,
    )
    body = render_transcript(lines)
    document = render_header(session_number, started_utc) + "\n" + body + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(document)
    return out_path

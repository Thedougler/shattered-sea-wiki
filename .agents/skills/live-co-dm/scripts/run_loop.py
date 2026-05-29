#!/usr/bin/env python3
"""The long-running live-capture orchestration loop.

Pulls frames from an ``AudioSource``, splits them into utterance-sized chunks
with the ``SilenceChunker``, and for each chunk: saves the audio first (so
nothing is ever lost), runs the diarize→transcribe→attribute→identify pipeline,
and appends the resulting lines to the durable transcript.

Designed to run 4h+: memory is bounded (the chunker buffers only the current
utterance), each transcript line is fsync'd, and a failure inside one chunk is
contained to that chunk. ``stop`` lets a signal handler (or a test) end cleanly.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Callable

import audio_file
from boundaries import AudioSource, Diarizer, Embedder, Transcriber
from pipeline import process_chunk
from session_paths import chunk_audio_filename
from silence_chunker import AudioChunk, SilenceChunker
from speaker_id import SpeakerIdentifier
from transcript_writer import TranscriptWriter


@dataclass
class LoopDeps:
    source: AudioSource
    chunker: SilenceChunker
    diarizer: Diarizer
    transcriber: Transcriber
    embedder: Embedder
    identifier: SpeakerIdentifier
    writer: TranscriptWriter
    audio_dir: str
    sample_rate: int
    on_status: Callable[[str], None] = field(default=lambda msg: None)


def _handle_chunk(chunk: AudioChunk, index: int, deps: LoopDeps) -> int:
    """Save audio, run the pipeline, append lines. Returns lines written."""
    fname = chunk_audio_filename(index, chunk.start_ms)
    try:
        audio_file.write_wav(os.path.join(deps.audio_dir, fname), chunk.samples, deps.sample_rate)
    except Exception as exc:  # audio save must never kill the session
        deps.on_status(f"chunk {index}: audio save failed: {exc}")
    lines = process_chunk(
        chunk.samples, deps.sample_rate, chunk.start_ms,
        diarizer=deps.diarizer, transcriber=deps.transcriber,
        embedder=deps.embedder, identifier=deps.identifier,
    )
    for line in lines:
        deps.writer.append_line(line.markdown)
    return len(lines)


def run_loop(
    deps: LoopDeps,
    *,
    stop: Callable[[], bool] = lambda: False,
    max_chunks: int | None = None,
) -> int:
    """Run until the source is exhausted, ``stop()`` returns True, or max_chunks.

    Returns the total number of transcript lines written.
    """
    written = 0
    index = 0
    try:
        for frame in deps.source.frames():
            if stop():
                break
            for chunk in deps.chunker.push(frame):
                written += _handle_chunk(chunk, index, deps)
                index += 1
                if max_chunks is not None and index >= max_chunks:
                    return written
        tail = deps.chunker.flush()
        if tail is not None:
            written += _handle_chunk(tail, index, deps)
    finally:
        deps.source.close()
    return written


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - thin CLI wiring
    """CLI entry point. Real model/mic wiring lives in ``adapters.py``."""
    import argparse

    parser = argparse.ArgumentParser(description="Live session transcriber (Parakeet + pyannote).")
    parser.add_argument("--session", type=int, default=None, help="Session number (auto if omitted).")
    parser.add_argument("--speakers", type=int, default=None, help="Known physical speaker count.")
    parser.add_argument("--wiki", default="wiki", help="Wiki root directory.")
    parser.add_argument("--profiles-dir", default=None, help="Voice profiles directory.")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args(argv)
    try:
        from adapters import build_live_deps  # imported lazily; needs ML stack
    except ImportError as exc:
        sys.stderr.write(
            f"Live capture needs the ML stack. Install requirements.txt first ({exc}).\n"
        )
        return 1
    deps, banner = build_live_deps(args)
    sys.stderr.write(banner + "\n")
    run_loop(deps)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

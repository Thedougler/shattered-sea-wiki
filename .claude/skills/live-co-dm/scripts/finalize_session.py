#!/usr/bin/env python3
"""CLI: produce the canonical transcript for a recorded session (offline re-pass).

Reads the silence-chunked wavs from a live session's audio dir, concatenates them
in order, runs the high-accuracy offline diarization + ASR pass (with the known
physical-speaker count), and writes the committed
``wiki/sessions/session-NN-transcript.md``.

Usage:
    python3 finalize_session.py --session 4 --speakers 5 [--wiki wiki]

The audio-reading + ML wiring is thin and untested (needs the ML stack); the
finalization logic itself is covered by ``test_finalize.py`` with fakes.
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys


def _read_wavs_concatenated(audio_dir: str) -> tuple[list[float], int]:  # pragma: no cover
    """Concatenate every wav in ``audio_dir`` (sorted) into one float list."""
    from audio_file import read_wav

    samples: list[float] = []
    sample_rate = 16000
    for name in sorted(os.listdir(audio_dir)):
        if not name.endswith(".wav"):
            continue
        chunk, sample_rate = read_wav(os.path.join(audio_dir, name))
        samples.extend(chunk)
    return samples, sample_rate


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI/ML wiring
    parser = argparse.ArgumentParser(description="Finalize a session transcript (offline re-pass).")
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--speakers", type=int, default=None, help="Known physical speaker count.")
    parser.add_argument("--wiki", default="wiki")
    parser.add_argument("--profiles-dir", default=None)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args(argv)

    sessions_dir = os.path.join(args.wiki, "sessions")
    live_dir = os.path.join(sessions_dir, ".live")

    from session_paths import session_paths_for

    paths = session_paths_for(live_dir, args.session)
    if not os.path.isdir(paths.audio_dir):
        sys.stderr.write(f"No audio for session {args.session:02d} at {paths.audio_dir}\n")
        return 1

    try:
        from adapters import PyannoteDiarizer, PyannoteEmbedder, ParakeetTranscriber
        from finalize import finalize_session
        from profiles import ProfileStore
        from speaker_id import SpeakerIdentifier
    except ImportError as exc:
        sys.stderr.write(f"Finalization needs the ML stack (install requirements.txt): {exc}\n")
        return 1

    samples, sample_rate = _read_wavs_concatenated(paths.audio_dir)
    profiles_dir = args.profiles_dir or os.path.join(os.path.dirname(__file__), os.pardir, "profiles")
    enrolled = ProfileStore(profiles_dir).load_all()
    auth = os.environ.get("HF_TOKEN")
    out_path = os.path.join(sessions_dir, f"session-{args.session:02d}-transcript.md")
    started = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    finalize_session(
        samples, sample_rate, session_number=args.session, started_utc=started,
        out_path=out_path,
        diarizer=PyannoteDiarizer(num_speakers=args.speakers, auth_token=auth),
        transcriber=ParakeetTranscriber(),
        embedder=PyannoteEmbedder(auth_token=auth),
        identifier=SpeakerIdentifier(enrolled, threshold=args.threshold),
    )
    sys.stderr.write(f"Canonical transcript written -> {out_path}\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

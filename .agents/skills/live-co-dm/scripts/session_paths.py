#!/usr/bin/env python3
"""Pure path + numbering logic for live-session artifacts.

Canonical session notes live at ``wiki/sessions/session-NN.md``; live capture
scratch lives at ``wiki/sessions/.live/session-NN/`` (gitignored). The next
session number is one past the highest seen in *either* place, so a re-run never
clobbers an existing session's scratch.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

_SESSION_MD = re.compile(r"^session-(\d+)\.md$")
_SESSION_DIR = re.compile(r"^session-(\d+)$")


@dataclass(frozen=True)
class SessionPaths:
    session_number: int
    root: str
    audio_dir: str
    transcript_md: str
    meta_json: str


def chunk_audio_filename(index: int, start_ms: int) -> str:
    """Sortable, human-readable wav name: ``0007_00h12m03s.wav``."""
    total = int(start_ms // 1000)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{index:04d}_{h:02d}h{m:02d}m{s:02d}s.wav"


def _max_match(directory: str, pattern: re.Pattern) -> int:
    if not os.path.isdir(directory):
        return 0
    best = 0
    for entry in os.listdir(directory):
        m = pattern.match(entry)
        if m:
            best = max(best, int(m.group(1)))
    return best


def next_session_number(sessions_dir: str, live_dir: str) -> int:
    canonical = _max_match(sessions_dir, _SESSION_MD)
    live = _max_match(live_dir, _SESSION_DIR)
    return max(canonical, live) + 1


def session_paths_for(live_dir: str, n: int) -> SessionPaths:
    root = os.path.join(live_dir, f"session-{n:02d}")
    return SessionPaths(
        session_number=n,
        root=root,
        audio_dir=os.path.join(root, "audio"),
        transcript_md=os.path.join(root, "live_transcript.md"),
        meta_json=os.path.join(root, "session.json"),
    )

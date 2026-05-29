#!/usr/bin/env python3
"""Durable, incremental markdown transcript writer.

Every append is flushed and ``fsync``'d so a crash at hour three of a session
still leaves a complete transcript up to the last written line. Append-only —
the file is never truncated mid-session — so an external reader (the co-DM
agent) can safely tail it while capture continues.
"""

from __future__ import annotations

import os

from render import render_header


class TranscriptWriter:
    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    def _append(self, text: str) -> None:
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())

    def write_header(self, session_number: int, started_utc: str) -> None:
        self._append(render_header(session_number, started_utc) + "\n")

    def append_line(self, markdown: str) -> None:
        self._append(markdown.rstrip("\n") + "\n")

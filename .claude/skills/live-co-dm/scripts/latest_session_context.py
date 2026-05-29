#!/usr/bin/env python3
"""Compact mid-session context loader for the co-DM agent.

During play, latency matters more than completeness. Instead of the full wiki
startup (init/lint/audit), the agent runs this once to get a small bundle: the
tail of the live transcript (what just happened), the current world state from
``hot.md`` (faction clocks, live threads), and a pointer to the canonical session
note. Everything else is fetched on demand via ``ttrpg-wiki-query``.

Usage:
    latest_session_context.py [--wiki wiki] [--tail 80]
Prints the bundle to stdout; status to stderr.
"""

from __future__ import annotations

import os
import re
import sys

_SESSION_DIR = re.compile(r"^session-(\d+)$")

SKIP_NOTICE = (
    "NOTE: Mid-session mode. SKIP ttrpg-llm-wiki-init, lint, index regen, and all "
    "routine maintenance. Answer fast and concise from the context below; use "
    "ttrpg-wiki-query only on demand for a specific fact."
)


def find_latest_live(live_dir: str) -> tuple[int, str] | None:
    if not os.path.isdir(live_dir):
        return None
    best_n, best_path = -1, None
    for entry in os.listdir(live_dir):
        m = _SESSION_DIR.match(entry)
        if not m:
            continue
        n = int(m.group(1))
        candidate = os.path.join(live_dir, entry, "live_transcript.md")
        if n > best_n and os.path.isfile(candidate):
            best_n, best_path = n, candidate
    if best_path is None:
        return None
    return best_n, best_path


def find_canonical(sessions_dir: str, n: int) -> str | None:
    path = os.path.join(sessions_dir, f"session-{n:02d}.md")
    return path if os.path.isfile(path) else None


def tail_lines(path: str, n: int) -> str:
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    return "\n".join(lines[-n:])


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def build_bundle(wiki_dir: str, tail: int = 80) -> str:
    sessions_dir = os.path.join(wiki_dir, "sessions")
    live_dir = os.path.join(sessions_dir, ".live")
    hot_path = os.path.join(wiki_dir, "hot.md")

    parts: list[str] = [SKIP_NOTICE, ""]

    live = find_latest_live(live_dir)
    if live is None:
        parts.append("== LIVE TRANSCRIPT ==")
        parts.append("(no live transcript found — is transcribe_session running?)")
    else:
        n, path = live
        parts.append(f"== LIVE TRANSCRIPT (session {n:02d}, last {tail} lines) ==")
        parts.append(tail_lines(path, tail))
        canonical = find_canonical(sessions_dir, n - 1)
        if canonical:
            parts.append("")
            parts.append(f"== PREVIOUS SESSION NOTE == {canonical}")

    parts.append("")
    parts.append("== CURRENT WORLD STATE (hot.md) ==")
    parts.append(_read(hot_path) if os.path.isfile(hot_path) else "(hot.md not found)")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Compact mid-session context for the co-DM agent.")
    parser.add_argument("--wiki", default="wiki", help="Wiki root directory.")
    parser.add_argument("--tail", type=int, default=80, help="Lines of live transcript to include.")
    args = parser.parse_args(argv)
    sys.stdout.write(build_bundle(args.wiki, tail=args.tail) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

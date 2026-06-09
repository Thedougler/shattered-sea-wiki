#!/usr/bin/env python3
"""Archive a fully-ingested source out of Inbox/ into .raw/<type>/.

After a source has been decomposed into the wiki, it stops being an intake
item and becomes a permanent raw record. This `git mv`s it into the matching
.raw/ subdirectory. The move is also the completion signal for check_ingest.py:
once the file lives in .raw/, its content hash is present there and it drops off
the pending queue. The source content is never altered — only relocated.

Usage:
    archive_source.py Inbox/Foo.md --type faction-source [--dry-run]

For session/transcript sources, pass --session NN to nest the file under a
per-session packet (.raw/sessions/session-NN/notes/<filename>) instead of the
flat .raw/sessions/<filename> default:

    archive_source.py Inbox/sessions/foo.md --type session --session 07
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

from wiki_common import REPO_ROOT, rel

# Source type (from triage) -> .raw subdirectory.
TYPE_TO_SUBDIR = [
    ("session", "sessions"),
    ("transcript", "sessions"),
    ("entity-source", "characters"),
    ("crew-source", "characters"),
    ("deity-source", "characters"),
    ("rules-or-homebrew", "homebrew"),
    ("homebrew", "homebrew"),
    ("character-sheet", "characters"),
    ("asset", "assets"),
]
DEFAULT_SUBDIR = (
    "reference"  # factions, situations, locations, lore, species, research, handouts
)


def find_pdf_sidecar(md_path: str) -> str | None:
    """If md_path has a pdf_sidecar frontmatter field, return the PDF's absolute path."""
    try:
        with open(md_path, "r", errors="replace") as fh:
            in_fm = False
            for line in fh:
                stripped = line.strip()
                if stripped == "---" and not in_fm:
                    in_fm = True
                    continue
                if stripped == "---" and in_fm:
                    break
                if in_fm and stripped.startswith("pdf_sidecar:"):
                    val = stripped.split(":", 1)[1].strip().strip("\"'")
                    if val:
                        candidate = os.path.join(os.path.dirname(md_path), val)
                        if os.path.isfile(candidate):
                            return os.path.abspath(candidate)
    except Exception:
        pass
    return None


def subdir_for(type_str: str) -> str:
    t = (type_str or "").lower()
    for needle, sub in TYPE_TO_SUBDIR:
        if needle in t:
            return sub
    return DEFAULT_SUBDIR


def is_session_type(type_str: str) -> bool:
    """True when the source is session-scoped (session note or transcript)."""
    t = (type_str or "").lower()
    return "session" in t or "transcript" in t


def dest_subdir(type_str: str, session: str | None) -> str:
    """Return the .raw subdir path (relative to .raw/) for a source.

    With --session set on a session/transcript source, nest the file in a
    per-session packet: sessions/session-NN/notes. Otherwise fall back to the
    flat type-derived subdir (back-compat).
    """
    subdir = subdir_for(type_str)
    if session and is_session_type(type_str):
        return f"{subdir}/session-{int(session):02d}/notes"
    return subdir


def git(*args, check=True):
    return subprocess.run(
        ["git", "-C", REPO_ROOT, *args], check=check, capture_output=True, text=True
    )


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--type", default=None)
    ap.add_argument(
        "--session",
        default=None,
        help="2-digit session number; nests session/transcript sources under "
        ".raw/sessions/session-NN/notes/ instead of the flat .raw/sessions/.",
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    src_abs = os.path.abspath(args.source)
    if not os.path.exists(src_abs):
        sys.stderr.write(f"archive_source: not found — {args.source}\n")
        return 1
    src_rel = rel(src_abs)

    type_str = args.type or ""
    if args.session and is_session_type(type_str) and not args.session.isdigit():
        sys.stderr.write(
            f"archive_source: --session must be numeric — got {args.session!r}\n"
        )
        return 2
    subdir = dest_subdir(type_str, args.session)
    if not type_str:
        sys.stderr.write(
            f"archive_source: no --type given; defaulting to .raw/{subdir}/. "
            "Pass --type <triage-type> to place it correctly.\n"
        )
    if args.session and not is_session_type(type_str):
        sys.stderr.write(
            "archive_source: --session ignored for non-session/transcript type "
            f"{type_str!r}; archiving to .raw/{subdir}/.\n"
        )
    dest_rel = f".raw/{subdir}/{os.path.basename(src_abs)}"
    dest_abs = os.path.join(REPO_ROOT, dest_rel)

    if os.path.exists(dest_abs):
        sys.stderr.write(f"archive_source: destination exists — {dest_rel}\n")
        return 1

    sidecar = find_pdf_sidecar(src_abs)
    sidecar_rel = None
    sidecar_dest_rel = None
    if sidecar:
        sidecar_rel = rel(sidecar)
        sidecar_dest_rel = f".raw/{subdir}/{os.path.basename(sidecar)}"

    if args.dry_run:
        print(f"would move {src_rel} -> {dest_rel} (type={type_str or 'default'})")
        if sidecar_rel and sidecar_dest_rel:
            print(f"would move {sidecar_rel} -> {sidecar_dest_rel} (pdf sidecar)")
        return 0

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    r = git("mv", src_rel, dest_rel, check=False)
    if r.returncode != 0:
        os.rename(src_abs, dest_abs)
        git("add", src_rel, dest_rel, check=False)

    print(f"archived {src_rel} -> {dest_rel}")

    if sidecar_rel and sidecar_dest_rel:
        sidecar_dest_abs = os.path.join(REPO_ROOT, sidecar_dest_rel)
        os.makedirs(os.path.dirname(sidecar_dest_abs), exist_ok=True)
        r = git("mv", sidecar_rel, sidecar_dest_rel, check=False)
        if r.returncode != 0:
            os.rename(sidecar, sidecar_dest_abs)
            git("add", sidecar_rel, sidecar_dest_rel, check=False)
        print(f"archived {sidecar_rel} -> {sidecar_dest_rel} (pdf sidecar)")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

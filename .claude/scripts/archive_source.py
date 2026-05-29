#!/usr/bin/env python3
"""Archive a fully-ingested source out of Inbox/ into .raw/<type>/.

After a source has been decomposed into the wiki, it stops being an intake
item and becomes a permanent raw record. This `git mv`s it into the matching
.raw/ subdirectory. The move is also the completion signal for check_ingest.py:
once the file lives in .raw/, its content hash is present there and it drops off
the pending queue. The source content is never altered — only relocated.

Usage:
    archive_source.py Inbox/Foo.md --type faction-source [--dry-run]
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
    ("asset", "assets"),
]
DEFAULT_SUBDIR = "reference"  # factions, situations, locations, lore, species, research, handouts


def subdir_for(type_str: str) -> str:
    t = (type_str or "").lower()
    for needle, sub in TYPE_TO_SUBDIR:
        if needle in t:
            return sub
    return DEFAULT_SUBDIR


def git(*args, check=True):
    return subprocess.run(["git", "-C", REPO_ROOT, *args], check=check,
                          capture_output=True, text=True)


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--type", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    src_abs = os.path.abspath(args.source)
    if not os.path.exists(src_abs):
        sys.stderr.write(f"archive_source: not found — {args.source}\n")
        return 1
    src_rel = rel(src_abs)

    type_str = args.type or ""
    subdir = subdir_for(type_str)
    if not type_str:
        sys.stderr.write(
            f"archive_source: no --type given; defaulting to .raw/{subdir}/. "
            "Pass --type <triage-type> to place it correctly.\n"
        )
    dest_rel = f".raw/{subdir}/{os.path.basename(src_abs)}"
    dest_abs = os.path.join(REPO_ROOT, dest_rel)

    if os.path.exists(dest_abs):
        sys.stderr.write(f"archive_source: destination exists — {dest_rel}\n")
        return 1

    if args.dry_run:
        print(f"would move {src_rel} -> {dest_rel} (type={type_str or 'default'})")
        return 0

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    r = git("mv", src_rel, dest_rel, check=False)
    if r.returncode != 0:
        os.rename(src_abs, dest_abs)
        git("add", src_rel, dest_rel, check=False)

    print(f"archived {src_rel} -> {dest_rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

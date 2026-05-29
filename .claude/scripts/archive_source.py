#!/usr/bin/env python3
"""Archive a fully-ingested source out of Inbox/ into .raw/<type>/.

After a source has been decomposed into the wiki, it stops being an intake
item and becomes a permanent raw record. This `git mv`s it into the matching
.raw/ subdirectory and rewrites its row in wiki/ingest-registry.md so the
File path stays accurate. The source content is never altered — only relocated.

Usage:
    archive_source.py Inbox/Foo.md [--type faction-source] [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

from wiki_common import REPO_ROOT, rel

REGISTRY = os.path.join(REPO_ROOT, "wiki", "ingest-registry.md")

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


def registry_type(inbox_relpath: str) -> str | None:
    if not os.path.exists(REGISTRY):
        return None
    with open(REGISTRY, encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("|") and inbox_relpath in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 2:
                    return cells[1]
    return None


def rewrite_registry(old_rel: str, new_rel: str) -> bool:
    if not os.path.exists(REGISTRY):
        return False
    with open(REGISTRY, encoding="utf-8") as fh:
        text = fh.read()
    # Only touch the File column occurrence (start of a table row).
    pattern = re.compile(r"(^\|\s*)" + re.escape(old_rel) + r"(\s*\|)", re.MULTILINE)
    new_text, n = pattern.subn(lambda m: m.group(1) + new_rel + m.group(2), text)
    if n:
        with open(REGISTRY, "w", encoding="utf-8") as fh:
            fh.write(new_text)
    return bool(n)


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

    type_str = args.type or registry_type(src_rel) or ""
    subdir = subdir_for(type_str)
    dest_rel = f".raw/{subdir}/{os.path.basename(src_abs)}"
    dest_abs = os.path.join(REPO_ROOT, dest_rel)

    if os.path.exists(dest_abs):
        sys.stderr.write(f"archive_source: destination exists — {dest_rel}\n")
        return 1

    if args.dry_run:
        print(f"would move {src_rel} -> {dest_rel} (type={type_str or 'inferred'})")
        return 0

    os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
    r = git("mv", src_rel, dest_rel, check=False)
    if r.returncode != 0:
        os.rename(src_abs, dest_abs)
        git("add", src_rel, dest_rel, check=False)

    changed = rewrite_registry(src_rel, dest_rel)
    print(f"archived {src_rel} -> {dest_rel}"
          + ("" if changed else "  (no registry row matched — check manually)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

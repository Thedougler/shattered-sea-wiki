#!/usr/bin/env python3
"""Reconcile the ingest registry against what is actually on disk.

Reports sources present in Inbox/ or .raw/ that have no registry row
(`unregistered`) and registry rows whose File path no longer exists
(`missing`). With --diff <git-range>, lists the wiki/ files touched in that
range — useful for filling a row's "Wiki Outputs" column from real changes
instead of from memory.

Usage:
    sync_registry.py
    sync_registry.py --diff HEAD~1..HEAD
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

from wiki_common import REPO_ROOT

REGISTRY = os.path.join(REPO_ROOT, "wiki", "ingest-registry.md")
SCAN_DIRS = ["Inbox", ".raw"]
IGNORE = {"AGENTS.md", "CLAUDE.md", "README.md"}


def registry_paths() -> set[str]:
    paths = set()
    if not os.path.exists(REGISTRY):
        return paths
    with open(REGISTRY, encoding="utf-8") as fh:
        for line in fh:
            s = line.lstrip()
            if s.startswith("|") and not s.startswith("|---") and "File" not in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if cells and "/" in cells[0]:
                    paths.add(cells[0].strip("`"))
    return paths


def disk_sources() -> list[str]:
    found = []
    for base in SCAN_DIRS:
        root = os.path.join(REPO_ROOT, base)
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if name in IGNORE or name.startswith("."):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, name), REPO_ROOT)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)


def git_diff_outputs(rng: str) -> list[str]:
    r = subprocess.run(
        ["git", "-C", REPO_ROOT, "diff", "--name-only", rng, "--", "wiki/"],
        capture_output=True, text=True, check=False,
    )
    return sorted(p for p in r.stdout.splitlines() if p.strip())


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", default=None)
    args = ap.parse_args(argv)

    reg = registry_paths()
    disk = disk_sources()

    unregistered = [p for p in disk if p not in reg]
    missing = sorted(p for p in reg if not os.path.exists(os.path.join(REPO_ROOT, p)))

    print(f"Registry rows: {len(reg)}  |  Disk sources: {len(disk)}")
    print(f"\nUnregistered ({len(unregistered)}):")
    for p in unregistered:
        print(f"  {p}")
    print(f"\nMissing from disk ({len(missing)}):")
    for p in missing:
        print(f"  {p}")

    if args.diff:
        print(f"\nwiki/ outputs in {args.diff}:")
        for p in git_diff_outputs(args.diff):
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

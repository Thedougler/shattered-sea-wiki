#!/usr/bin/env python3
"""Mirror the canonical skill tree (.claude/skills) into .agents/skills.

.claude/skills is the single source of truth. Other runtimes read .agents/skills,
so it is regenerated from .claude/skills rather than hand-edited. Run this only
when a skill itself changes.

Usage:
    sync_skills.py            # report drift, make no changes
    sync_skills.py --apply    # overwrite .agents/skills to match .claude/skills
"""

from __future__ import annotations

import filecmp
import os
import shutil
import sys

from wiki_common import REPO_ROOT

SRC = os.path.join(REPO_ROOT, ".claude", "skills")
DST = os.path.join(REPO_ROOT, ".agents", "skills")


def drift(src, dst):
    """Yield human-readable differences between two trees."""
    cmp = filecmp.dircmp(src, dst)
    for name in cmp.left_only:
        yield f"+ {os.path.relpath(os.path.join(src, name), SRC)} (missing in .agents)"
    for name in cmp.right_only:
        yield f"- {os.path.relpath(os.path.join(dst, name), DST)} (stale in .agents)"
    for name in cmp.diff_files:
        yield f"~ {os.path.relpath(os.path.join(src, name), SRC)} (differs)"
    for sub in cmp.common_dirs:
        yield from drift(os.path.join(src, sub), os.path.join(dst, sub))


def main(argv) -> int:
    if not os.path.isdir(SRC):
        sys.stderr.write("sync_skills: .claude/skills not found\n")
        return 1

    diffs = list(drift(SRC, DST)) if os.path.isdir(DST) else ["(.agents/skills absent)"]
    if not diffs:
        print("sync_skills: .agents/skills already in sync")
        return 0

    print(f"sync_skills: {len(diffs)} difference(s):")
    for d in diffs:
        print(f"  {d}")

    if "--apply" in argv:
        if os.path.isdir(DST):
            shutil.rmtree(DST)
        shutil.copytree(SRC, DST)
        print("sync_skills: regenerated .agents/skills from .claude/skills")
    else:
        print("sync_skills: run with --apply to regenerate .agents/skills")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

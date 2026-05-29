#!/usr/bin/env python3
"""List Inbox/ sources not yet present in .raw/ — the ingest work queue.

A source leaves the queue by being archived from Inbox/ into .raw/ (see
archive_source.py, which `git mv`s it). Once its content lives under .raw/, its
hash is present there and it stops being printed. There is no state file to keep
in sync; the filesystem is the source of truth, so an interrupted run resumes by
running this again.

Read-only by default — safe to run any time, including just to see what's
pending. Pass --prune to also remove Inbox/ files whose content already exists
in .raw/ (stray duplicates the normal `git mv` archive flow wouldn't leave);
every removal is reported, and tracked files are removed with `git rm` so the
index stays consistent.

stdout is intentionally machine-friendly: one repo-relative path per pending
source, sorted, with no headers — safe to pipe or read line by line. A one-line
status ("N source(s) pending" / "queue clear") goes to stderr so it shows up in a
terminal or an agent's tool output without polluting stdout; pass --quiet to
suppress it. Use --count to print just the number of pending sources to stdout.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import os
import subprocess
import sys

from wiki_common import REPO_ROOT, rel

DEFAULT_INBOX = "Inbox"
DEFAULT_RAW = ".raw"


def resolve_path(path: str) -> str:
    if os.path.isabs(path):
        return os.path.abspath(path)
    return os.path.abspath(os.path.join(REPO_ROOT, path))


def display_path(path: str) -> str:
    path = os.path.abspath(path)
    if os.path.commonpath([REPO_ROOT, path]) == REPO_ROOT:
        return rel(path)
    return path


def iter_files(root_path: str) -> list[tuple[str, int]]:
    root_abs = resolve_path(root_path)
    if not os.path.isdir(root_abs):
        return []

    paths: list[tuple[str, int]] = []
    for dirpath, dirnames, filenames in os.walk(root_abs):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                paths.append((path, os.path.getsize(path)))
    return paths


def file_hash(path: str, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_inbox(
    inbox_path: str, raw_path: str, algorithm: str
) -> tuple[list[str], list[str]]:
    """Split Inbox files into (pending, duplicates) as sorted absolute paths.

    pending    — content is NOT yet in .raw/; these still need ingest.
    duplicates — content already exists byte-for-byte in .raw/; safe to prune.

    Hashing is lazy: an Inbox file is only hashed when .raw/ holds a same-size
    file, and each .raw/ size bucket is hashed at most once.
    """
    raw_by_size: dict[int, list[str]] = defaultdict(list)
    for path, size in iter_files(raw_path):
        raw_by_size[size].append(path)

    raw_hashes_by_size: dict[int, set[str]] = {}
    pending: list[str] = []
    duplicates: list[str] = []

    for path, size in iter_files(inbox_path):
        if size not in raw_by_size:
            pending.append(path)
            continue

        if size not in raw_hashes_by_size:
            raw_hashes_by_size[size] = {
                file_hash(p, algorithm) for p in raw_by_size[size]
            }

        if file_hash(path, algorithm) in raw_hashes_by_size[size]:
            duplicates.append(path)
        else:
            pending.append(path)

    pending.sort(key=display_path)
    duplicates.sort(key=display_path)
    return pending, duplicates


def remove_file(path: str) -> None:
    """Delete an Inbox file, preferring `git rm` so tracked files stay staged."""
    r = subprocess.run(
        ["git", "-C", REPO_ROOT, "rm", "-q", "--", rel(path)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:  # untracked file — git won't remove it
        os.remove(path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List Inbox/ sources not yet present in .raw/ (the ingest queue). "
        "Read-only by default; --prune also removes Inbox duplicates."
    )
    parser.add_argument("--inbox", default=DEFAULT_INBOX, help="Inbox directory relative to repo root")
    parser.add_argument("--raw", default=DEFAULT_RAW, help=".raw directory relative to repo root")
    parser.add_argument("--algorithm", default="sha256", help="hashlib algorithm to use")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="remove Inbox/ files whose content already exists in .raw/ (each removal reported)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="with --prune, report what would be removed without deleting",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="print only the number of pending sources to stdout",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="suppress the stderr status line",
    )
    args = parser.parse_args(argv)

    try:
        hashlib.new(args.algorithm)
    except ValueError:
        sys.stderr.write(f"check_ingest: unknown hash algorithm: {args.algorithm}\n")
        return 2

    if not os.path.isdir(resolve_path(args.inbox)):
        sys.stderr.write(f"check_ingest: inbox not found — {args.inbox}\n")
        if args.count:
            print(0)
        return 0

    pending, duplicates = classify_inbox(args.inbox, args.raw, args.algorithm)

    if args.prune:
        for path in duplicates:
            action = "would prune" if args.dry_run else "pruned"
            sys.stderr.write(f"check_ingest: {action} (already in .raw): {display_path(path)}\n")
            if not args.dry_run:
                remove_file(path)
    elif duplicates and not args.quiet:
        sys.stderr.write(
            f"check_ingest: {len(duplicates)} Inbox file(s) already in .raw — "
            "run with --prune to remove\n"
        )

    if args.count:
        print(len(pending))
        return 0

    for path in pending:
        print(display_path(path))

    if not args.quiet:
        if pending:
            sys.stderr.write(f"check_ingest: {len(pending)} source(s) pending\n")
        else:
            sys.stderr.write("check_ingest: queue clear (0 pending)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

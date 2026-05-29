#!/usr/bin/env python3
"""List Inbox/ sources not yet present in .raw/ — the ingest work queue.

A source leaves the queue by being archived from Inbox/ into .raw/ (see
archive_source.py, which `git mv`s it). Once its content lives under .raw/, its
hash is present there and it stops being printed. There is no state file to keep
in sync; the filesystem is the source of truth, so an interrupted run resumes by
running this again.

Safe to run any time, including just to see what's pending. By default it also
deduplicates Inbox/: files already archived in .raw/ are removed, and duplicate
Inbox copies keep one deterministic pending source while pruning the extras.
Only exact byte-for-byte duplicates are removed. Every removal is reported, and
tracked files are removed with `git rm` so the index stays consistent.

stdout is intentionally machine-friendly: one repo-relative path per pending
source, sorted, with no headers — safe to pipe or read line by line. A one-line
status ("N source(s) pending" / "queue clear") goes to stderr so it shows up in a
terminal or an agent's tool output without polluting stdout; pass --quiet to
suppress it. Use --count to print just the number of pending sources to stdout.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import filecmp
import hashlib
import os
import subprocess
import sys

from wiki_common import REPO_ROOT, rel

DEFAULT_INBOX = "Inbox"
DEFAULT_RAW = ".raw"


@dataclass(frozen=True)
class Duplicate:
    path: str
    duplicate_of: str
    kind: str


@dataclass(frozen=True)
class Classification:
    pending: list[str]
    raw_duplicates: list[Duplicate]
    inbox_duplicates: list[Duplicate]

    @property
    def duplicates(self) -> list[Duplicate]:
        return self.raw_duplicates + self.inbox_duplicates


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


def canonical_inbox_key(path: str) -> tuple[int, int, int, str]:
    """Prefer the most source-like filename when duplicate Inbox copies exist."""
    display = display_path(path)
    basename = os.path.basename(path).lower()
    duplicate_markers = (
        " copy",
        "-copy",
        "_copy",
        "duplicate",
        "dupe",
        "conflict",
        "untitled",
    )
    marker_penalty = sum(marker in basename for marker in duplicate_markers)
    numbered_copy_penalty = (
        1 if any(token in basename for token in ("(1)", "(2)", "(3)")) else 0
    )
    return (
        marker_penalty + numbered_copy_penalty,
        display.count("/"),
        len(display),
        display,
    )


def split_exact_file_groups(paths: list[str]) -> list[list[str]]:
    """Split same-size, same-hash files into confirmed byte-identical groups."""
    groups: list[list[str]] = []
    for path in paths:
        for group in groups:
            if filecmp.cmp(path, group[0], shallow=False):
                group.append(path)
                break
        else:
            groups.append([path])
    return groups


def classify_inbox(inbox_path: str, raw_path: str, algorithm: str) -> Classification:
    """Classify Inbox files by ingest state and exact duplicate status.

    pending    — content is NOT yet in .raw/; these still need ingest.
    duplicates — content already exists byte-for-byte elsewhere; safe to prune.

    Inbox-vs-.raw duplicates are removed entirely because they were already
    archived. Inbox-vs-Inbox duplicates keep one canonical pending path so a
    source cannot disappear before it is ingested.
    """
    raw_by_size: dict[int, list[str]] = defaultdict(list)
    for path, size in iter_files(raw_path):
        raw_by_size[size].append(path)

    raw_hashes_by_size: dict[int, dict[str, list[str]]] = {}
    pending_by_content: dict[tuple[int, str], list[str]] = defaultdict(list)
    raw_duplicates: list[Duplicate] = []

    def raw_hashes(size: int) -> dict[str, list[str]]:
        if size not in raw_hashes_by_size:
            hashes: dict[str, list[str]] = defaultdict(list)
            for raw_path_abs in raw_by_size[size]:
                hashes[file_hash(raw_path_abs, algorithm)].append(raw_path_abs)
            raw_hashes_by_size[size] = dict(hashes)
        return raw_hashes_by_size[size]

    for path, size in iter_files(inbox_path):
        digest = file_hash(path, algorithm)
        raw_hash_matches = (
            raw_hashes(size).get(digest, []) if size in raw_by_size else []
        )
        raw_matches = [
            raw_path_abs
            for raw_path_abs in raw_hash_matches
            if filecmp.cmp(path, raw_path_abs, shallow=False)
        ]

        if raw_matches:
            raw_duplicates.append(
                Duplicate(path=path, duplicate_of=raw_matches[0], kind="raw")
            )
        else:
            pending_by_content[(size, digest)].append(path)

    pending: list[str] = []
    inbox_duplicates: list[Duplicate] = []
    for paths in pending_by_content.values():
        for group in split_exact_file_groups(paths):
            if len(group) == 1:
                pending.append(group[0])
                continue

            keeper = min(group, key=canonical_inbox_key)
            pending.append(keeper)
            for path in group:
                if path != keeper:
                    inbox_duplicates.append(
                        Duplicate(path=path, duplicate_of=keeper, kind="inbox")
                    )

    raw_duplicates.sort(key=lambda d: display_path(d.path))
    inbox_duplicates.sort(key=lambda d: display_path(d.path))
    pending.sort(key=display_path)
    return Classification(
        pending=pending,
        raw_duplicates=raw_duplicates,
        inbox_duplicates=inbox_duplicates,
    )


def is_inside(path: str, root: str) -> bool:
    path_abs = os.path.abspath(path)
    root_abs = os.path.abspath(root)
    try:
        return os.path.commonpath([root_abs, path_abs]) == root_abs
    except ValueError:
        return False


def is_tracked(path: str) -> bool:
    if not is_inside(path, REPO_ROOT):
        return False
    r = subprocess.run(
        ["git", "-C", REPO_ROOT, "ls-files", "--error-unmatch", "--", rel(path)],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def remove_file(path: str, inbox_root: str) -> None:
    """Delete an Inbox file, preferring `git rm` so tracked files stay staged."""
    if not is_inside(path, inbox_root):
        raise RuntimeError(
            f"refusing to remove file outside inbox: {display_path(path)}"
        )

    if is_tracked(path):
        r = subprocess.run(
            ["git", "-C", REPO_ROOT, "rm", "-q", "--", rel(path)],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            raise RuntimeError(
                r.stderr.strip() or f"git rm failed: {display_path(path)}"
            )
    else:
        os.remove(path)


def describe_duplicate(duplicate: Duplicate) -> str:
    if duplicate.kind == "raw":
        return (
            f"{display_path(duplicate.path)} "
            f"(already archived as {display_path(duplicate.duplicate_of)})"
        )
    return (
        f"{display_path(duplicate.path)} "
        f"(duplicate of pending {display_path(duplicate.duplicate_of)})"
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List Inbox/ sources not yet present in .raw/ (the ingest queue). "
        "Deduplicates exact Inbox duplicates by default."
    )
    parser.add_argument(
        "--inbox", default=DEFAULT_INBOX, help="Inbox directory relative to repo root"
    )
    parser.add_argument(
        "--raw", default=DEFAULT_RAW, help=".raw directory relative to repo root"
    )
    parser.add_argument(
        "--algorithm", default="sha256", help="hashlib algorithm to use"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="deprecated; exact duplicate pruning is now enabled by default",
    )
    parser.add_argument(
        "--no-dedupe",
        action="store_true",
        help="do not remove duplicate Inbox files; only report them",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report duplicate removals without deleting files",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="print only the number of pending sources to stdout",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="print only the first N pending paths (one wave). Dedupe still runs over the "
        "whole Inbox; only the printed list is truncated.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="suppress the stderr status line",
    )
    args = parser.parse_args(argv)

    if args.prune and args.no_dedupe:
        parser.error("--prune and --no-dedupe cannot be used together")

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

    classification = classify_inbox(args.inbox, args.raw, args.algorithm)
    pending = classification.pending
    duplicates = classification.duplicates
    dedupe_enabled = not args.no_dedupe

    if duplicates and dedupe_enabled:
        inbox_root = resolve_path(args.inbox)
        for duplicate in duplicates:
            action = "would prune" if args.dry_run else "pruned"
            sys.stderr.write(
                f"check_ingest: {action}: {describe_duplicate(duplicate)}\n"
            )
            if not args.dry_run:
                try:
                    remove_file(duplicate.path, inbox_root)
                except OSError as exc:
                    sys.stderr.write(
                        "check_ingest: failed to prune "
                        f"{display_path(duplicate.path)}: {exc}\n"
                    )
                    return 1
                except RuntimeError as exc:
                    sys.stderr.write(f"check_ingest: failed to prune: {exc}\n")
                    return 1
    elif duplicates and not args.quiet:
        sys.stderr.write(
            f"check_ingest: {len(duplicates)} exact duplicate Inbox file(s) found — "
            "run without --no-dedupe to remove\n"
        )

    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be >= 0")

    if args.count:
        print(len(pending))
        return 0

    shown = pending if args.limit is None else pending[: args.limit]
    for path in shown:
        print(display_path(path))

    if not args.quiet:
        if not pending:
            sys.stderr.write("check_ingest: queue clear (0 pending)\n")
        elif args.limit is not None and len(shown) < len(pending):
            sys.stderr.write(
                f"check_ingest: showing {len(shown)} of {len(pending)} pending "
                "(--limit; run again after this wave)\n"
            )
        else:
            sys.stderr.write(f"check_ingest: {len(pending)} source(s) pending\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

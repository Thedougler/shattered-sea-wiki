#!/usr/bin/env python3
"""Scan Shattered Sea source folders for files not yet ingested."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


SOURCE_EXTENSIONS = {
    ".md",
    ".markdown",
    ".txt",
    ".rtf",
    ".pdf",
    ".doc",
    ".docx",
    ".json",
    ".csv",
    ".tsv",
    ".xls",
    ".xlsx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".mp3",
    ".m4a",
    ".wav",
    ".flac",
    ".mp4",
    ".mov",
}

DONE_STATUSES = {"ingested", "skipped", "superseded", "source-only"}
ACTIVE_STATUSES = {"pending", "triaged", "in-progress", "blocked", "partial"}
IGNORE_TOP_LEVEL = {"AGENTS.md", "CLAUDE.md", "README.md"}


@dataclass
class RegistryEntry:
    file: str
    type: str
    status: str
    date: str
    outputs: str


@dataclass
class SourceItem:
    file: str
    type: str
    status: str
    priority: int
    reason: str
    registry_outputs: str = ""


def repo_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def clean_cell(value: str) -> str:
    value = value.strip()
    value = value.strip("`")
    return value.strip()


def normalize_registry_path(value: str) -> str:
    value = clean_cell(value)
    return value.replace("\\ ", " ")


def parse_registry(registry_path: Path) -> dict[str, RegistryEntry]:
    if not registry_path.exists():
        return {}

    entries: dict[str, RegistryEntry] = {}
    for line in registry_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0].lower() in {"file", "---"} or set(cells[0]) <= {"-"}:
            continue
        file_path = normalize_registry_path(cells[0])
        if not file_path or file_path == "(none yet)":
            continue
        entries[file_path] = RegistryEntry(
            file=file_path,
            type=clean_cell(cells[1]),
            status=clean_cell(cells[2]).lower(),
            date=clean_cell(cells[3]),
            outputs=clean_cell(cells[4]),
        )
    return entries


def iter_sources(root: Path, include_root_docs: bool) -> Iterable[Path]:
    for base_name in (".raw", "Inbox"):
        base = root / base_name
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if is_source_file(path):
                yield path

    if include_root_docs:
        for path in root.iterdir():
            if path.is_file() and path.name not in IGNORE_TOP_LEVEL and is_source_file(path):
                yield path


def is_source_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name.startswith("."):
        return False
    return path.suffix.lower() in SOURCE_EXTENSIONS


def infer_type(rel_path: str) -> str:
    lower = rel_path.lower()
    name = Path(rel_path).name.lower()
    suffix = Path(rel_path).suffix.lower()

    if "session" in lower or "transcript" in lower:
        if "transcript" in lower or suffix in {".mp3", ".m4a", ".wav", ".flac"}:
            return "transcript"
        return "session"
    if "/characters/" in lower or "character" in lower or "sheet" in lower:
        return "entity-source"
    if "faction" in lower:
        return "faction-source"
    if "location" in lower or "place" in lower or "island" in lower or "dungeon" in lower:
        return "location-source"
    if "homebrew" in lower or "rule" in lower or "ruling" in lower:
        return "rules-or-homebrew"
    if "handout" in lower or "player" in lower:
        return "handout-or-player-facing"
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp3", ".m4a", ".wav", ".flac", ".mp4", ".mov"}:
        return "asset"
    if "research" in lower or "guidance" in lower or "writing" in name:
        return "research-or-guidance"
    if rel_path.startswith("Inbox/"):
        return "inbox"
    return "source"


def priority_for(source_type: str, status: str) -> int:
    if status == "in-progress":
        return 0
    if status in {"blocked", "partial"}:
        return 1
    base = {
        "transcript": 10,
        "session": 20,
        "rules-or-homebrew": 30,
        "entity-source": 40,
        "location-source": 40,
        "faction-source": 40,
        "handout-or-player-facing": 45,
        "inbox": 50,
        "source": 60,
        "asset": 80,
        "research-or-guidance": 90,
    }.get(source_type, 60)
    if status == "unregistered":
        return base + 1
    return base


def build_items(root: Path, include_root_docs: bool) -> tuple[list[SourceItem], dict[str, RegistryEntry]]:
    registry = parse_registry(root / "wiki" / "ingest-registry.md")
    discovered = {repo_path(path, root): path for path in iter_sources(root, include_root_docs)}
    items: list[SourceItem] = []

    for rel_path in sorted(discovered):
        entry = registry.get(rel_path)
        source_type = infer_type(rel_path)
        if entry is None:
            status = "unregistered"
            reason = "source file has no registry row"
            outputs = ""
        else:
            status = entry.status or "pending"
            reason = "registry status requires action" if status in ACTIVE_STATUSES else "registry status is closed"
            outputs = entry.outputs
            if entry.type and entry.type != "—":
                source_type = entry.type
        if status in DONE_STATUSES:
            continue
        items.append(
            SourceItem(
                file=rel_path,
                type=source_type,
                status=status,
                priority=priority_for(source_type, status),
                reason=reason,
                registry_outputs=outputs,
            )
        )

    for rel_path, entry in registry.items():
        if entry.status in DONE_STATUSES:
            continue
        if rel_path in discovered:
            continue
        items.append(
            SourceItem(
                file=rel_path,
                type=entry.type or "source",
                status=entry.status or "pending",
                priority=priority_for(entry.type or "source", entry.status or "pending") + 5,
                reason="registry row is active but source file was not found",
                registry_outputs=entry.outputs,
            )
        )

    items.sort(key=lambda item: (item.priority, item.file))
    return items, registry


def print_markdown(items: list[SourceItem], registry: dict[str, RegistryEntry], root: Path, limit: int) -> None:
    unregistered = sum(1 for item in items if item.status == "unregistered")
    active = len(items)
    print("# Pending Ingest Scan")
    print()
    print(f"Root: `{root}`")
    print(f"Registry entries: {len(registry)}")
    print(f"Actionable sources: {active}")
    print(f"Unregistered sources: {unregistered}")
    print()

    if not items:
        print("No pending source files found.")
        return

    print("| Priority | File | Type | Status | Reason |")
    print("|---:|---|---|---|---|")
    for item in items[:limit]:
        print(
            f"| {item.priority} | `{item.file}` | {item.type} | {item.status} | {item.reason} |"
        )

    remaining = len(items) - limit
    if remaining > 0:
        print()
        print(f"... {remaining} additional actionable source(s) omitted. Re-run with `--limit {len(items)}` to show all.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root; defaults to current directory.")
    parser.add_argument("--include-root-docs", action="store_true", help="Also scan top-level source documents.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum rows to print in Markdown output.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / "wiki").exists():
        raise SystemExit(f"wiki/ not found under {root}")

    items, registry = build_items(root, args.include_root_docs)
    if args.json:
        payload = {
            "root": str(root),
            "registry_entries": len(registry),
            "actionable_sources": len(items),
            "unregistered_sources": sum(1 for item in items if item.status == "unregistered"),
            "items": [asdict(item) for item in items],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_markdown(items, registry, root, max(args.limit, 0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

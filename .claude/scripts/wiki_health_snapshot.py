#!/usr/bin/env python3
"""Capture an objective, machine-readable snapshot of wiki health.

Used by the continuous-self-improvement skill to measure impact before and
after a fix.  Pure stdlib — no external dependencies.

Usage:
    python3 .claude/scripts/wiki_health_snapshot.py              # JSON to stdout
    python3 .claude/scripts/wiki_health_snapshot.py --save       # append to log
    python3 .claude/scripts/wiki_health_snapshot.py --diff <a> <b>  # compare two snapshots
    python3 .claude/scripts/wiki_health_snapshot.py --history    # table of saved snapshots

Metrics collected:
    file_count          total .md files in wiki/
    total_tokens        estimated token count across all files (chars / 4)
    lint_errors         wiki_lint.py error count
    lint_warnings       wiki_lint.py warning count
    lint_quality        wiki_lint.py quality-note count
    lint_by_category    breakdown of lint issues by category
    orphan_count        pages with no inbound links
    deadend_count       pages with no outbound links
    stub_summaries      files whose summary matches stub patterns
    pending_ingest      sources waiting in Inbox/
    hook_count          PostToolUse hooks registered
    script_test_count   test files in .claude/scripts/
    mean_file_tokens    average tokens per wiki file
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WIKI_DIR = os.path.join(REPO_ROOT, "wiki")
SCRIPTS_DIR = os.path.join(REPO_ROOT, ".claude", "scripts")
SNAPSHOT_LOG = os.path.join(REPO_ROOT, ".claude", "health-snapshots.jsonl")

STUB_PATTERNS = [
    re.compile(r"^stub", re.IGNORECASE),
    re.compile(r"^no summary", re.IGNORECASE),
    re.compile(r"^tbd", re.IGNORECASE),
    re.compile(r"^placeholder", re.IGNORECASE),
    re.compile(
        r"^an?\s+(npc|location|faction|item|creature)\s+in\s+the\s+campaign",
        re.IGNORECASE,
    ),
]


def count_wiki_files() -> tuple[int, int, int]:
    """Return (file_count, total_chars, stub_count)."""
    count = 0
    chars = 0
    stubs = 0
    for dirpath, _, filenames in os.walk(WIKI_DIR):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            count += 1
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            chars += len(text)
            summary = _extract_summary(text)
            if summary and any(p.match(summary) for p in STUB_PATTERNS):
                stubs += 1
    return count, chars, stubs


def _extract_summary(text: str) -> str | None:
    in_fm = False
    for line in text.splitlines():
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            break
        if in_fm:
            m = re.match(r'^summary:\s*["\']?(.+?)["\']?\s*$', line)
            if m:
                return m.group(1)
    return None


def run_lint() -> dict:
    """Parse wiki_lint.py output into structured counts."""
    result = {"errors": 0, "warnings": 0, "quality": 0, "by_category": {}}
    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "wiki_lint.py")],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=REPO_ROOT,
        )
        output = proc.stdout + proc.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return result

    summary_m = re.search(
        r"(\d+)\s+errors?\s+·\s+(\d+)\s+warnings?\s+·\s+(\d+)\s+quality",
        output,
    )
    if summary_m:
        result["errors"] = int(summary_m.group(1))
        result["warnings"] = int(summary_m.group(2))
        result["quality"] = int(summary_m.group(3))

    for line in output.splitlines():
        m = re.match(r"^\s+wiki/\S+\s+(\S+)\s+", line)
        if m:
            cat = m.group(1)
            result["by_category"][cat] = result["by_category"].get(cat, 0) + 1

    return result


def count_pending_ingest() -> int:
    try:
        proc = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS_DIR, "check_ingest.py"), "--count"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT,
        )
        for line in proc.stdout.strip().splitlines():
            try:
                return int(line.strip())
            except ValueError:
                continue
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return -1


def count_hooks() -> int:
    settings_path = os.path.join(REPO_ROOT, ".claude", "settings.json")
    try:
        data = json.load(open(settings_path))
        hooks = data.get("hooks", {}).get("PostToolUse", [])
        return sum(len(entry.get("hooks", [])) for entry in hooks)
    except (OSError, json.JSONDecodeError):
        return 0


def count_script_tests() -> int:
    count = 0
    for name in os.listdir(SCRIPTS_DIR):
        if name.startswith("test_") and name.endswith(".py"):
            count += 1
    return count


def take_snapshot(label: str = "") -> dict:
    file_count, total_chars, stub_count = count_wiki_files()
    lint = run_lint()
    pending = count_pending_ingest()
    hooks = count_hooks()
    tests = count_script_tests()
    total_tokens = total_chars // 4

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "label": label,
        "file_count": file_count,
        "total_tokens": total_tokens,
        "mean_file_tokens": total_tokens // file_count if file_count else 0,
        "lint_errors": lint["errors"],
        "lint_warnings": lint["warnings"],
        "lint_quality": lint["quality"],
        "lint_total": lint["errors"] + lint["warnings"] + lint["quality"],
        "lint_by_category": lint["by_category"],
        "orphan_count": lint["by_category"].get("orphan", 0),
        "deadend_count": lint["by_category"].get("deadend", 0),
        "stub_summaries": stub_count,
        "pending_ingest": pending,
        "hook_count": hooks,
        "script_test_count": tests,
    }


def save_snapshot(snapshot: dict) -> None:
    with open(SNAPSHOT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, separators=(",", ":")) + "\n")


def load_snapshots() -> list[dict]:
    if not os.path.exists(SNAPSHOT_LOG):
        return []
    snapshots = []
    with open(SNAPSHOT_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                snapshots.append(json.loads(line))
    return snapshots


def diff_snapshots(a: dict, b: dict) -> dict:
    """Compare two snapshots, return deltas (positive = increased)."""
    keys = [
        "file_count",
        "total_tokens",
        "mean_file_tokens",
        "lint_errors",
        "lint_warnings",
        "lint_quality",
        "lint_total",
        "orphan_count",
        "deadend_count",
        "stub_summaries",
        "pending_ingest",
        "hook_count",
        "script_test_count",
    ]
    deltas = {}
    for k in keys:
        va = a.get(k, 0)
        vb = b.get(k, 0)
        if isinstance(va, int) and isinstance(vb, int):
            delta = vb - va
            if delta != 0:
                deltas[k] = {"before": va, "after": vb, "delta": delta}
    return deltas


def format_diff(deltas: dict) -> str:
    if not deltas:
        return "No measurable change."
    lines = []
    for key, info in sorted(deltas.items()):
        d = info["delta"]
        direction = "+" if d > 0 else ""
        lines.append(f"  {key}: {info['before']} -> {info['after']} ({direction}{d})")
    return "\n".join(lines)


def format_history(snapshots: list[dict]) -> str:
    if not snapshots:
        return "No snapshots recorded yet."
    header = f"{'Date':<22} {'Label':<30} {'Files':>6} {'Lint':>6} {'Err':>4} {'Warn':>5} {'Orphn':>5} {'Stubs':>5}"
    lines = [header, "-" * len(header)]
    for s in snapshots[-20:]:
        ts = s["timestamp"][:19].replace("T", " ")
        label = (s.get("label", "") or "")[:30]
        lines.append(
            f"{ts:<22} {label:<30} {s['file_count']:>6} "
            f"{s['lint_total']:>6} {s['lint_errors']:>4} {s['lint_warnings']:>5} "
            f"{s['orphan_count']:>5} {s['stub_summaries']:>5}"
        )
    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    if "--history" in args:
        print(format_history(load_snapshots()))
        return

    if "--diff" in args:
        idx = args.index("--diff")
        if idx + 2 >= len(args):
            snapshots = load_snapshots()
            if len(snapshots) < 2:
                print("Need at least 2 saved snapshots for --diff without arguments.")
                sys.exit(1)
            a, b = snapshots[-2], snapshots[-1]
        else:
            a = json.loads(open(args[idx + 1]).read())
            b = json.loads(open(args[idx + 2]).read())
        print(format_diff(diff_snapshots(a, b)))
        return

    label = ""
    for i, arg in enumerate(args):
        if arg == "--label" and i + 1 < len(args):
            label = args[i + 1]
            break

    snapshot = take_snapshot(label)

    if "--save" in args:
        save_snapshot(snapshot)
        print(
            f"Snapshot saved ({snapshot['lint_total']} lint issues, {snapshot['file_count']} files)"
        )
    else:
        print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Assemble and manage session transcript parts.

Subcommands:
    assemble  Concatenate parts with continuous timestamps, write assembled.csv
    status    Report session state: parts available, checkpoint progress
    resolve   Apply speaker-map.md to assembled.csv → resolved.csv

Usage:
    python3 .claude/scripts/assemble_transcript.py assemble <session_number>
    python3 .claude/scripts/assemble_transcript.py status <session_number>
    python3 .claude/scripts/assemble_transcript.py resolve <session_number>

    # Legacy (no subcommand) — defaults to assemble:
    python3 .claude/scripts/assemble_transcript.py <session_number>
"""

import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIO_DIR = REPO_ROOT / "audio" / "sessions"


def parse_timestamp(ts: str) -> int:
    parts = ts.strip().split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0


def format_timestamp(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}:{m:02d}:{s:02d}"


def get_session_dir(session: str) -> Path:
    return AUDIO_DIR / f"session{session}"


def get_part_files(session: str) -> list:
    return sorted(AUDIO_DIR.glob(f"session{session}-part*.m4a.csv"))


def cmd_assemble(session: str):
    part_files = get_part_files(session)
    if not part_files:
        print(f"No transcript CSVs found for session {session}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(part_files)} parts for session {session}", file=sys.stderr)

    out_dir = get_session_dir(session)
    out_dir.mkdir(exist_ok=True)

    all_rows = []
    time_offset = 0

    for part_file in part_files:
        with open(part_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            part_rows = list(reader)

        max_end = 0
        for row in part_rows:
            start_s = parse_timestamp(row["Start"]) + time_offset
            end_s = parse_timestamp(row["End"]) + time_offset
            max_end = max(max_end, end_s)

            all_rows.append(
                {
                    "ID": len(all_rows) + 1,
                    "Start": format_timestamp(start_s),
                    "End": format_timestamp(end_s),
                    "Speaker": row["Speaker"],
                    "Text": row["Text"],
                    "Source": part_file.name,
                }
            )

        time_offset = max_end + 1
        print(
            f"  {part_file.name}: {len(part_rows)} lines, cumulative {format_timestamp(time_offset)}",
            file=sys.stderr,
        )

    out_path = out_dir / "assembled.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["ID", "Start", "End", "Speaker", "Text", "Source"]
        )
        writer.writeheader()
        writer.writerows(all_rows)

    manifest_path = out_dir / "parts.txt"
    with open(manifest_path, "w") as f:
        for pf in part_files:
            f.write(f"{pf.name}\n")

    print(f"\nAssembled {len(all_rows)} lines -> {out_path}", file=sys.stderr)

    speakers = Counter(r["Speaker"] for r in all_rows)
    print("\nSpeaker distribution:", file=sys.stderr)
    for speaker, count in speakers.most_common():
        pct = 100 * count / len(all_rows)
        print(f"  {speaker}: {count} ({pct:.0f}%)", file=sys.stderr)

    unresolved = [s for s in speakers if s.startswith("Speaker") or s == "Unknown"]
    if unresolved:
        total = sum(speakers[s] for s in unresolved)
        print(
            f"\n** {total} lines need speaker resolution: {', '.join(unresolved)} **",
            file=sys.stderr,
        )


def cmd_status(session: str):
    part_files = get_part_files(session)
    out_dir = get_session_dir(session)

    print(f"Session {session} transcript status:")
    print(f"  Parts available: {len(part_files)}")
    for pf in part_files:
        with open(pf, newline="", encoding="utf-8") as f:
            lines = sum(1 for _ in f) - 1
        print(f"    {pf.name}: {lines} lines")

    total_source_lines = 0
    for pf in part_files:
        with open(pf, newline="", encoding="utf-8") as f:
            total_source_lines += sum(1 for _ in f) - 1

    assembled = out_dir / "assembled.csv"
    manifest = out_dir / "parts.txt"
    speaker_map = out_dir / "speaker-map.md"
    resolved = out_dir / "resolved.csv"
    extracts = out_dir / "extracts.md"
    flags = out_dir / "flags.md"

    print("\n  Checkpoints:")

    # Pass 1
    if assembled.exists():
        with open(assembled, newline="", encoding="utf-8") as f:
            assembled_lines = sum(1 for _ in f) - 1
        stale = False
        if manifest.exists():
            known_parts = set(manifest.read_text().strip().splitlines())
            current_parts = {pf.name for pf in part_files}
            if known_parts != current_parts:
                stale = True
        print(
            f"    Pass 1 (assembled.csv): {assembled_lines} lines"
            + (" ** STALE — new parts available, re-run assemble **" if stale else "")
        )
    else:
        print("    Pass 1 (assembled.csv): not started")

    # Pass 2
    if speaker_map.exists() and resolved.exists():
        with open(resolved, newline="", encoding="utf-8") as f:
            resolved_lines = sum(1 for _ in f) - 1
        print(f"    Pass 2 (resolved.csv): {resolved_lines} lines")
    elif speaker_map.exists():
        print("    Pass 2 (speaker-map.md): map written, resolved.csv not yet produced")
    else:
        print("    Pass 2 (speaker resolution): not started")

    # Pass 3
    progress = out_dir / "progress.txt"
    recap = out_dir / "recap.md"
    if extracts.exists() or recap.exists():
        if progress.exists():
            chunks_done = len(
                [ln for ln in progress.read_text().strip().splitlines() if ln.strip()]
            )
            print(f"    Pass 3 (extract & recap): {chunks_done} chunk(s) processed")
            last_line = (
                progress.read_text().strip().splitlines()[-1] if chunks_done else ""
            )
            print(f"      Last: {last_line}")
        else:
            print("    Pass 3 (extract & recap): files present (no progress.txt)")
        has_recap = "yes" if recap.exists() else "no"
        has_extracts = "yes" if extracts.exists() else "no"
        print(f"      recap.md: {has_recap} | extracts.md: {has_extracts}")
        if flags.exists():
            flag_text = flags.read_text()
            unresolved_count = flag_text.count("- [ ]")
            resolved_count = flag_text.count("- [x]")
            print(
                f"      Flags: {unresolved_count} unresolved, {resolved_count} resolved"
            )
    elif progress.exists():
        chunks_done = len(
            [ln for ln in progress.read_text().strip().splitlines() if ln.strip()]
        )
        print(f"    Pass 3: {chunks_done} chunk(s) in progress.txt but no output files")
    else:
        print("    Pass 3 (extract & recap): not started")

    # Pass 4
    session_note = REPO_ROOT / "wiki" / "sessions" / f"session-{session}.md"
    if session_note.exists():
        print("    Pass 4 (wiki integration): session note exists")
    elif recap.exists() and extracts.exists():
        print("    Pass 4 (wiki integration): ready (recap + extracts available)")
    else:
        print("    Pass 4 (wiki integration): blocked (needs Pass 3 completion)")


def parse_speaker_map(map_path: Path) -> dict:
    """Parse speaker-map.md and return {original_label: resolved_label}."""
    mapping = {}
    text = map_path.read_text()
    in_table = False
    for line in text.splitlines():
        if line.startswith("| Label"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 3:
                label = cells[0]
                resolved_to = cells[1]
                confidence = cells[2].lower()
                if confidence == "unknown":
                    continue
                if confidence == "low":
                    mapping[label] = f"?{resolved_to}"
                else:
                    mapping[label] = resolved_to
        elif in_table and not line.strip().startswith("|"):
            in_table = False
    return mapping


def cmd_resolve(session: str):
    out_dir = get_session_dir(session)
    assembled = out_dir / "assembled.csv"
    speaker_map = out_dir / "speaker-map.md"

    if not assembled.exists():
        print("No assembled.csv — run assemble first", file=sys.stderr)
        sys.exit(1)
    if not speaker_map.exists():
        print(
            "No speaker-map.md — run Pass 2 (speaker resolution) first", file=sys.stderr
        )
        sys.exit(1)

    mapping = parse_speaker_map(speaker_map)
    if not mapping:
        print("No resolutions found in speaker-map.md", file=sys.stderr)
        sys.exit(1)

    print("Speaker map loaded:", file=sys.stderr)
    for orig, resolved in mapping.items():
        print(f"  {orig} -> {resolved}", file=sys.stderr)

    rows = []
    changed = 0
    with open(assembled, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["Speaker"] in mapping:
                row["Speaker"] = mapping[row["Speaker"]]
                changed += 1
            rows.append(row)

    resolved_path = out_dir / "resolved.csv"
    with open(resolved_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"\nResolved {changed} lines -> {resolved_path}",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # Detect subcommand vs legacy (bare session number)
    if sys.argv[1] in ("assemble", "status", "resolve"):
        subcmd = sys.argv[1]
        if len(sys.argv) < 3:
            print(
                f"Usage: assemble_transcript.py {subcmd} <session_number>",
                file=sys.stderr,
            )
            sys.exit(1)
        session = sys.argv[2].zfill(2)
    else:
        subcmd = "assemble"
        session = sys.argv[1].zfill(2)

    if subcmd == "assemble":
        cmd_assemble(session)
    elif subcmd == "status":
        cmd_status(session)
    elif subcmd == "resolve":
        cmd_resolve(session)


if __name__ == "__main__":
    main()

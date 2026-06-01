#!/usr/bin/env python3
"""Assemble session transcript parts into a single CSV with dictionary corrections.

Usage:
    python3 .claude/scripts/assemble_transcript.py <session_number>
    python3 .claude/scripts/assemble_transcript.py 04

Finds all session{NN}-part*.m4a.csv files in audio/sessions/, applies the
shattered-sea-dictionary.csv corrections, concatenates with continuous IDs and
cumulative timestamps, and writes audio/sessions/session{NN}/assembled.csv.

Re-running after new parts arrive appends them. Existing assembled.csv is
overwritten (the source CSVs are the durable artifacts).
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIO_DIR = REPO_ROOT / "audio" / "sessions"

SPEAKER_NORMALIZE = {
    "Crissdalyn": "Crissdalyn",
}


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
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def load_dictionary(dict_path: Path) -> list:
    subs = []
    with open(dict_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Enabled", "1") != "1":
                continue
            source = row["Source"]
            target = row["Target"]
            if source == target:
                continue
            case_sensitive = row.get("Case Sensitive", "0") == "1"
            subs.append((source, target, case_sensitive))
    subs.sort(key=lambda x: len(x[0]), reverse=True)
    return subs


def apply_dictionary(text: str, subs: list) -> str:
    for source, target, case_sensitive in subs:
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = r"\b" + re.escape(source) + r"\b"
        text = re.sub(pattern, target, text, flags=flags)
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: assemble_transcript.py <session_number>", file=sys.stderr)
        print("  e.g.: assemble_transcript.py 04", file=sys.stderr)
        sys.exit(1)

    session = sys.argv[1].zfill(2)

    part_files = sorted(AUDIO_DIR.glob(f"session{session}-part*.m4a.csv"))
    if not part_files:
        print(f"No transcript CSVs found for session {session}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(part_files)} parts for session {session}", file=sys.stderr)

    dict_path = AUDIO_DIR / "shattered-sea-dictionary.csv"
    subs = []
    if dict_path.exists():
        subs = load_dictionary(dict_path)
        print(f"Loaded {len(subs)} dictionary substitutions", file=sys.stderr)

    out_dir = AUDIO_DIR / f"session{session}"
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

            text = apply_dictionary(row["Text"], subs) if subs else row["Text"]
            speaker = SPEAKER_NORMALIZE.get(row["Speaker"], row["Speaker"])

            all_rows.append(
                {
                    "ID": len(all_rows) + 1,
                    "Start": format_timestamp(start_s),
                    "End": format_timestamp(end_s),
                    "Speaker": speaker,
                    "Text": text,
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
        print(
            f"\n** {sum(speakers[s] for s in unresolved)} lines need speaker resolution: {', '.join(unresolved)} **",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()

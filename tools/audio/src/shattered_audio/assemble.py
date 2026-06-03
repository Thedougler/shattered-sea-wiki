"""Assemble transcript parts into a single continuous transcript.

Ported from .claude/scripts/assemble_transcript.py — handles the CSV-based
transcript parts produced by NotebookLM or manual chunking.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TranscriptRow:
    id: int
    start: str
    end: str
    speaker: str
    text: str
    source: str


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


def find_part_files(audio_dir: Path, session: str) -> list[Path]:
    return sorted(audio_dir.glob(f"session{session}-part*.m4a.csv"))


def assemble(audio_dir: Path, session: str) -> list[TranscriptRow]:
    """Concatenate transcript parts with continuous timestamps."""
    part_files = find_part_files(audio_dir, session)
    if not part_files:
        raise FileNotFoundError(f"No transcript CSVs found for session {session}")

    all_rows: list[TranscriptRow] = []
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
                TranscriptRow(
                    id=len(all_rows) + 1,
                    start=format_timestamp(start_s),
                    end=format_timestamp(end_s),
                    speaker=row["Speaker"],
                    text=row["Text"],
                    source=part_file.name,
                )
            )

        time_offset = max_end + 1

    return all_rows


def write_assembled_csv(rows: list[TranscriptRow], out_path: Path) -> None:
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Start", "End", "Speaker", "Text", "Source"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "ID": row.id,
                    "Start": row.start,
                    "End": row.end,
                    "Speaker": row.speaker,
                    "Text": row.text,
                    "Source": row.source,
                }
            )


def speaker_distribution(rows: list[TranscriptRow]) -> Counter:
    return Counter(r.speaker for r in rows)

"""Format transcription output as wiki-compatible markdown."""

from __future__ import annotations

from datetime import date

from .transcribe import Segment


def format_timestamp(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def format_wiki_transcript(
    segments: list[Segment],
    *,
    session_number: int,
    session_date: str | None = None,
    model: str = "whisper-large-v3",
    diarization_model: str | None = None,
    speaker_confidence: float | None = None,
) -> str:
    """Generate a wiki-formatted raw transcript markdown file."""
    if session_date is None:
        session_date = date.today().isoformat()

    speakers_detected = sorted(set(s.speaker for s in segments if s.speaker))
    if not speakers_detected:
        speakers_detected = ["Unknown"]

    duration = format_timestamp(max(s.end for s in segments)) if segments else "00:00:00"

    lines = [
        "---",
        "type: raw",
        "subtype: raw-session",
        f"session_number: {session_number}",
        f'session_date: "{session_date}"',
        f'recording_duration: "{duration}"',
        f"speakers_detected: {speakers_detected}",
    ]

    if speaker_confidence is not None:
        lines.append(f"speaker_confidence: {speaker_confidence}")

    lines.extend(
        [
            f'model: "{model}"',
        ]
    )

    if diarization_model:
        lines.append(f'diarization_model: "{diarization_model}"')

    lines.extend(
        [
            "ingest_status: pending",
            "---",
            "",
            f"# Session {session_number} — Raw Transcript",
            "",
        ]
    )

    current_segment_start = 0.0
    segment_interval = 15 * 60
    segment_num = 1

    for seg in segments:
        if seg.start >= current_segment_start + segment_interval or seg == segments[0]:
            ts = format_timestamp(seg.start)
            lines.append(f"## Segment {segment_num} — {ts}")
            lines.append("")
            current_segment_start = seg.start
            segment_num += 1

        speaker = seg.speaker or "Unknown"
        lines.append(f"**{speaker}:** {seg.text}")
        lines.append("")

    return "\n".join(lines)

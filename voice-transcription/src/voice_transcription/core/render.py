#!/usr/bin/env python3
"""Pure rendering of attributed/identified speech into a markdown transcript.

Line format:  ``**Character (?)** (Player) [mm:ss] [overlap]: text``
  - ``(?)`` marks a low-confidence character attribution (small top-1/top-2 margin).
  - ``(Player)`` is omitted for unknown speakers (no player known).
  - ``[overlap]`` marks lines that came from a true crosstalk region; both
    speakers' lines are emitted so neither is lost.

Kept pure so the exact transcript text is asserted deterministically in tests.
"""

from __future__ import annotations

from dataclasses import dataclass

from attribute import AttributedSegment


@dataclass(frozen=True)
class RenderedLine:
    start: float
    markdown: str


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def render_line(
    segment: AttributedSegment,
    *,
    label: str,
    player: str,
    confident: bool,
    is_unknown: bool | None = None,
) -> RenderedLine:
    text = " ".join(w.text for w in segment.words)
    # Unknown speakers carry an already-uncertain label, so they never also get
    # a "(?)" marker; that marker is reserved for shaky *known* attributions.
    if is_unknown is None:
        is_unknown = not player
    name = label if (confident or is_unknown) else f"{label} (?)"
    speaker_md = f"**{name}**"
    if player:
        speaker_md += f" ({player})"
    stamp = f"[{format_timestamp(segment.start)}]"
    overlap_tag = " [overlap]" if segment.overlap else ""
    markdown = f"{speaker_md} {stamp}{overlap_tag}: {text}"
    return RenderedLine(start=segment.start, markdown=markdown)


def render_transcript(lines: list[RenderedLine]) -> str:
    return "\n".join(line.markdown for line in lines)


def render_header(session_number: int, started_utc: str) -> str:
    return (
        f"# Session {session_number:02d} — Live Transcript\n\n"
        f"Started: {started_utc}\n"
    )

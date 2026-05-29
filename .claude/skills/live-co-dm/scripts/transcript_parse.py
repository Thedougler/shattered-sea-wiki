#!/usr/bin/env python3
"""Parse a finalized transcript back into structured, timestamped lines.

The committed ``session-NN-transcript.md`` is the human-corrected record of who
said what. To feed corrections back into voice profiles we read it back into
``TranscriptLine`` records, mirroring the format produced by ``render.render_line``:

    **Character** (Player) [mm:ss] [overlap]: text
    **Character (?)** (Player) [mm:ss]: text
    **Unknown-1** [mm:ss]: who

Pure stdlib regex parsing — no models, fully unit-tested.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# **Name [(?)]** [(Player)] [mm:ss|hh:mm:ss] [[overlap]]: text
_LINE = re.compile(
    r"^\*\*(?P<name>[^*]+?)(?P<lc>\s*\(\?\))?\*\*"   # **Name** or **Name (?)**
    r"(?:\s+\((?P<player>[^)]*)\))?"                  # optional (Player)
    r"\s+\[(?P<ts>\d{1,2}:\d{2}(?::\d{2})?)\]"        # [mm:ss] or [hh:mm:ss]
    r"(?P<overlap>\s+\[overlap\])?"                   # optional [overlap]
    r":\s?(?P<text>.*)$"
)


@dataclass(frozen=True)
class TranscriptLine:
    character: str
    player: str
    start_s: float
    text: str
    overlap: bool
    low_confidence: bool


def _ts_to_seconds(ts: str) -> float:
    parts = [int(p) for p in ts.split(":")]
    if len(parts) == 3:
        h, m, s = parts
    else:
        h, (m, s) = 0, parts
    return float(h * 3600 + m * 60 + s)


def parse_line(line: str) -> TranscriptLine | None:
    m = _LINE.match(line.strip())
    if not m:
        return None
    return TranscriptLine(
        character=m.group("name").strip(),
        player=(m.group("player") or "").strip(),
        start_s=_ts_to_seconds(m.group("ts")),
        text=m.group("text").strip(),
        overlap=bool(m.group("overlap")),
        low_confidence=bool(m.group("lc")),
    )


def parse_transcript(text: str) -> list[TranscriptLine]:
    out: list[TranscriptLine] = []
    for raw in text.splitlines():
        parsed = parse_line(raw)
        if parsed is not None:
            out.append(parsed)
    return out

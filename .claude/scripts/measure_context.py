#!/usr/bin/env python3
"""Measure the per-session context footprint of skill descriptions + CLAUDE.md.

Counts real tokens with tiktoken (o200k_base, the GPT-4o encoding) as a close
proxy for Claude's tokenizer. Falls back to a labeled chars/4 estimate only if
tiktoken is unavailable.
"""

import json
import math
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")  # mute urllib3/LibreSSL noise from tiktoken deps

ROOT = Path(__file__).resolve().parents[2]  # repo root
SKILLS = ROOT / ".claude/skills"

try:
    import tiktoken

    _ENC = tiktoken.get_encoding("o200k_base")
    TOKENIZER = "tiktoken:o200k_base"

    def toks(s: str) -> int:
        return len(_ENC.encode(s))

except Exception:  # pragma: no cover - fallback path
    _ENC = None
    TOKENIZER = "estimate:chars/4"

    def toks(s: str) -> int:
        return math.ceil(len(s) / 4)


def extract_description(text: str) -> str:
    # Grab the frontmatter block between the first two '---' lines.
    m = re.search(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else text
    # Folded/literal: 'description: >' or '|' then indented lines until next top-level key.
    m = re.search(r"^description:\s*[>|]\s*\n((?:[ \t]+.*\n?)+)", fm, re.M)
    if m:
        return " ".join(line.strip() for line in m.group(1).splitlines())
    # Inline: 'description: ...'
    m = re.search(r"^description:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else ""


def main() -> None:
    rows = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        desc = extract_description(skill_md.read_text(encoding="utf-8"))
        rows.append(
            {"skill": skill_md.parent.name, "chars": len(desc), "tokens": toks(desc)}
        )
    claude_md = ROOT / "CLAUDE.md"
    cmd_text = claude_md.read_text(encoding="utf-8") if claude_md.exists() else ""
    out = {
        "tokenizer": TOKENIZER,
        "skills": rows,
        "skill_total_chars": sum(r["chars"] for r in rows),
        "skill_total_tokens": sum(r["tokens"] for r in rows),
        "skill_count": len(rows),
        "claude_md_chars": len(cmd_text),
        "claude_md_tokens": toks(cmd_text),
    }
    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()

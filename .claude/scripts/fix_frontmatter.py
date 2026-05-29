#!/usr/bin/env python3
"""Deterministically complete a wiki file's frontmatter.

Adds any missing universal/type-specific fields with path-inferred defaults
and sets `updated:` to today. It never overwrites a value that is already
present (except `updated:`), so it is safe to run on every write and is
idempotent: a second run on a complete, freshly-updated file changes nothing.

Usage:
    fix_frontmatter.py <file> [<file> ...]

Mechanical additions are reported on stderr prefixed `fixed:`. Things that
need human judgment (a still-default summary) are surfaced as `FLAG:`.
Always exits 0 so it is safe as an advisory hook.
"""

from __future__ import annotations

import sys

from wiki_common import (
    TYPE_EXTRA_FIELDS,
    UNIVERSAL_FIELDS,
    infer_subtype,
    infer_type,
    parse_fields,
    rel,
    split_frontmatter,
    today,
)

STUB_SUMMARY = "Stub — no summary yet."


def default_value(field: str, relpath: str) -> str:
    t = infer_type(relpath)
    st = infer_subtype(relpath)
    defaults = {
        "type": t,
        "subtype": st,
        "campaign": "shattered-sea",
        "status": "unknown",
        "audience": "dm",
        "publish": "false",
        "summary": f'"{STUB_SUMMARY}"',
        "created": today(),
        "updated": today(),
        "tags": "[]",
        "sources": '["Unknown"]',
        "confidence_level": "medium",
        "lifecycle": "dormant",
        "island": "null",
        "portable": "false",
        "entry_points": "[]",
        "contains_situations": "[]",
        "session_number": "0",
        "session_date": '"unknown"',
        "system_role": '"unknown"',
        "token_profile": "on-demand",
        "mandatory_for": "[]",
        "update_trigger": '""',
    }
    return defaults.get(field, '""')


def required_fields(relpath: str):
    t = infer_type(relpath)
    return UNIVERSAL_FIELDS + TYPE_EXTRA_FIELDS.get(t, [])


def process(path: str) -> bool:
    relpath = rel(path)
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    fm_lines, body, had = split_frontmatter(text)
    if not had:
        # Synthesize a full block — wiki files must carry frontmatter.
        fm_lines = []
        fields = {}
    else:
        fields = parse_fields(fm_lines)

    changed = []
    new_lines = list(fm_lines)

    # 1. Append any missing required fields, in canonical order.
    for field in required_fields(relpath):
        if field not in fields:
            new_lines.append(f"{field}: {default_value(field, relpath)}")
            fields[field] = default_value(field, relpath)
            changed.append(field)

    # 2. Force `updated:` to today.
    stamped = False
    for i, line in enumerate(new_lines):
        if line.startswith("updated:"):
            want = f"updated: {today()}"
            if line.strip() != want:
                new_lines[i] = want
                if "updated" not in changed:
                    changed.append("updated")
            stamped = True
            break
    if not stamped:
        new_lines.append(f"updated: {today()}")
        changed.append("updated")

    if not changed and had:
        # Nothing to do.
        _judgment_flags(relpath, fields)
        return False

    rebuilt = "---\n" + "\n".join(new_lines) + "\n---\n"
    if had:
        new_text = rebuilt + body if body.startswith("\n") else rebuilt + "\n" + body
    else:
        new_text = rebuilt + ("\n" + text if text.strip() else "")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_text)

    if changed:
        sys.stderr.write(f"fixed: [{', '.join(changed)}] — {relpath}\n")
    _judgment_flags(relpath, fields)
    return True


def _judgment_flags(relpath: str, fields: dict) -> None:
    summary = fields.get("summary", "").strip().strip('"').strip("'")
    if not summary or summary == STUB_SUMMARY:
        sys.stderr.write(f"FLAG: summary-stale — {relpath}\n")


def main(argv) -> int:
    for path in argv:
        try:
            process(path)
        except Exception as exc:  # never break the hook
            sys.stderr.write(f"fix_frontmatter error on {path}: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

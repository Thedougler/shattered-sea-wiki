"""Shared helpers for Shattered Sea wiki automation scripts.

Pure stdlib. No external YAML dependency — frontmatter here is simple
`key: value` blocks, so we parse line-by-line and never reformat values
we don't own.
"""

from __future__ import annotations

import datetime
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WIKI_DIR = os.path.join(REPO_ROOT, "wiki")


def today() -> str:
    return datetime.date.today().isoformat()


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def split_frontmatter(text: str):
    """Return (frontmatter_lines, body_text, had_frontmatter).

    frontmatter_lines excludes the surrounding `---` delimiters.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            body = "\n".join(lines[i + 1:])
            return fm, body, True
    # No closing delimiter — treat as no frontmatter to avoid corrupting.
    return [], text, False


def parse_fields(fm_lines):
    """Map top-level `key:` -> raw value string (value may be empty)."""
    fields = {}
    for line in fm_lines:
        m = re.match(r"^([A-Za-z0-9_]+):(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def get_summary(fields) -> str:
    raw = fields.get("summary", "")
    return raw.strip().strip('"').strip("'")


def first_h1(body: str) -> str | None:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            # Strip a trailing "— Stub" style suffix for display.
            return re.sub(r"\s+[—-]\s+Stub\s*$", "", m.group(1)).strip()
    return None


# ---------------------------------------------------------------------------
# Path inference (mirrors references/frontmatter-defaults.md)
# ---------------------------------------------------------------------------

def rel(path: str) -> str:
    return os.path.relpath(os.path.abspath(path), REPO_ROOT).replace(os.sep, "/")


def infer_type(relpath: str) -> str:
    table = [
        ("wiki/entities/", "entity"),
        ("wiki/situations/", "situation"),
        ("wiki/islands/", "island"),
        ("wiki/sessions/", "session"),
        ("wiki/system/", "system"),
        ("wiki/lore/", "lore"),
        ("wiki/rules/", "rules"),
        ("wiki/dm/", "dm-intelligence"),
        (".raw/", "raw"),
    ]
    for prefix, value in table:
        if relpath.startswith(prefix):
            return value
    if "/" not in relpath:
        return "governance"
    return "unknown"


def infer_subtype(relpath: str) -> str:
    table = [
        ("wiki/entities/characters/pcs/", "pc"),
        ("wiki/entities/characters/npcs/", "npc"),
        ("wiki/entities/characters/crew/", "crew"),
        ("wiki/entities/characters/minor/", "minor-npc"),
        ("wiki/entities/places/regions/", "region"),
        ("wiki/entities/places/islands/", "island-place"),
        ("wiki/entities/places/settlements/", "settlement"),
        ("wiki/entities/places/buildings/", "building"),
        ("wiki/entities/places/dungeons/", "dungeon"),
        ("wiki/entities/places/planes/", "plane"),
        ("wiki/entities/places/", "place"),
        ("wiki/entities/factions/", "faction"),
        ("wiki/entities/deities/", "deity"),
        ("wiki/entities/items/", "item"),
        ("wiki/entities/vehicles/", "vehicle"),
        ("wiki/situations/active/", "active-situation"),
        ("wiki/situations/dormant/", "dormant-situation"),
        ("wiki/situations/resolved/", "resolved-situation"),
        ("wiki/islands/", "island"),
        ("wiki/lore/species/", "species"),
        ("wiki/lore/creatures/", "creature"),
        ("wiki/lore/history/", "history"),
        ("wiki/lore/geography/", "geography"),
        ("wiki/lore/cultures/", "culture"),
        ("wiki/lore/religions/", "religion"),
        ("wiki/lore/magic/", "magic"),
        ("wiki/lore/languages/", "language"),
        ("wiki/lore/", "lore-page"),
        ("wiki/rules/core/", "core-rule"),
        ("wiki/rules/subsystems/", "subsystem"),
        ("wiki/rules/", "rule"),
        ("wiki/sessions/", "session-note"),
        ("wiki/system/players/", "pc-sheet"),
        ("wiki/system/", "system-file"),
        ("wiki/dm/", "dm-file"),
        (".raw/sessions/", "raw-session"),
        (".raw/characters/", "raw-character"),
        (".raw/homebrew/", "raw-homebrew"),
        (".raw/reference/", "raw-reference"),
        (".raw/assets/", "raw-asset"),
    ]
    for prefix, value in table:
        if relpath.startswith(prefix):
            return value
    return "unknown"


# Required fields beyond the universal set, keyed by inferred type.
TYPE_EXTRA_FIELDS = {
    "entity": ["confidence_level", "relationships"],
    "situation": ["lifecycle", "island"],
    "island": ["portable", "entry_points", "contains_situations"],
    "session": ["session_number", "session_date"],
    "system": ["system_role", "token_profile", "mandatory_for", "update_trigger"],
}

UNIVERSAL_FIELDS = [
    "type", "subtype", "campaign", "status", "audience", "publish",
    "summary", "created", "updated", "tags", "sources",
]


def iter_wiki_files():
    for dirpath, dirnames, filenames in os.walk(WIKI_DIR):
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)

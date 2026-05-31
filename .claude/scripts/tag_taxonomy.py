"""
Controlled tag vocabulary for the Shattered Sea wiki.

This module is the machine-readable source of truth. The human-readable
source of truth is wiki/system/taxonomy.md — keep both in sync when adding
or removing tags.
"""

from __future__ import annotations

CANONICAL: frozenset[str] = frozenset(
    {
        # faction
        "dravosi",
        "tessarine",
        "passage",
        "waveservants",
        "sunken-crown",
        "drowned-maw",
        "fisk-fleet",
        "five-blades",
        # theme/domain
        "umberlee",
        "undead",
        "antheri",
        "rattkin",
        "grung",
        "moucheron",
        # narrative
        "maritime",
        "mystery",
        "salvage",
        # content type
        "homebrew",
        "late-game",
        # prep/workflow
        "needs-detail",
        "encounter-ready",
        "read-aloud",
        "player-resource",
        "dm-prep",
        "recurring",
        "combat",
    }
)

# Keys are lowercase; values are the canonical form to use instead.
ALIASES: dict[str, str] = {
    "dravosi-crown": "dravosi",
    "crown": "dravosi",
    "tessarine-concordat": "tessarine",
    "the-passage": "passage",
    "maw": "drowned-maw",
    "waveservant": "waveservants",
    "fisks-fleet": "fisk-fleet",
    "homebrew": "homebrew",  # catches capitalised variant "Homebrew"
    "late_game": "late-game",
    "dm-craft": "dm-prep",
    "dm-notes": "dm-prep",
    "dm-reference": "dm-prep",
    "prep": "dm-prep",
    "player-facing": "player-resource",
    "primer": "player-resource",
    "lich": "undead",
    "antheri-adjacent": "antheri",
}

# Tags that duplicate a frontmatter field (type/subtype/status/audience).
DEPRECATED_FRONTMATTER: frozenset[str] = frozenset(
    {
        "situation",
        "session",
        "rules",
        "lore",
        "system",
        "index",
        "narrative-island",
        "reference",
        "entity",
        "item",
        "place",
        "npc",
        "creature",
        "subclass",
        "scene",
        "faction",
        "ship",
        "vehicle",
        "species",
        "deity",
        "thread",
        "run-guide",
        "equipment",
        "encounter",
        "conflict",
        "obligation",
        "question",
        "secret",
        "pursuit",
        "event",
        "active",
        "dormant",
        "resolved",
        "dead",
        "destroyed",
        "dm-only",
        "players",
    }
)

# Tags that name entities — should be wikilinks in the body instead.
DEPRECATED_ENTITY_NAMES: frozenset[str] = frozenset(
    {
        "perrin",
        "delmar",
        "jean-claude",
        "crissdalynn",
        "nona",
        "grigori",
        "kyzil",
        "hollowell",
        "calveno",
        "warren",
        "port-tidefall",
        "kalowe",
        "midchain",
        "crown-islands",
        "verdant-teeth",
        "calders-tooth",
        "fort-crestwall",
        "cape-solitude",
        "aruhe",
        "takowan",
        "surety",
        "saltwright",
    }
)

# Tags that are source citations — belong in sources: frontmatter field.
DEPRECATED_SOURCE: frozenset[str] = frozenset(
    {
        "bestiary",
        "xmm",
        "xphb",
        "phb",
        "dmg",
    }
)

# System/process tags — not content tags.
DEPRECATED_SYSTEM: frozenset[str] = frozenset(
    {
        "current-state",
        "work-queue",
        "lint",
        "review",
        "log",
        "discrepancy",
    }
)

TAG_LIMIT = 5


def classify(tag: str) -> tuple[str, str | None]:
    """Classify a tag against the taxonomy.

    Returns (category, canonical_form_or_None):
      "canonical"           — tag is already in the controlled vocabulary
      "alias"               — tag is an alias; canonical_form is the target
      "deprecated-fm"       — frontmatter duplicate; should be removed
      "deprecated-entity"   — entity name; should be a wikilink
      "deprecated-source"   — source citation; should be in sources: field
      "deprecated-system"   — system/process tag; should be removed
      "unknown"             — not in any known list
      "visibility"          — visibility/ reserved group; leave untouched
    """
    if tag.startswith("visibility/"):
        return ("visibility", None)

    t = tag.lower()

    if t in {c.lower() for c in CANONICAL}:
        return ("canonical", tag)

    if t in ALIASES:
        canon = ALIASES[t]
        # Aliases that map to themselves are a normalisation alias (e.g. case variants)
        return ("alias", canon)

    if t in DEPRECATED_FRONTMATTER:
        return ("deprecated-fm", None)

    if t in DEPRECATED_ENTITY_NAMES:
        return ("deprecated-entity", None)

    if t in DEPRECATED_SOURCE:
        return ("deprecated-source", None)

    if t in DEPRECATED_SYSTEM:
        return ("deprecated-system", None)

    return ("unknown", None)

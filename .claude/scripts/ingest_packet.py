#!/usr/bin/env python3
"""Compile a compact context packet for ingesting one source.

A subagent ingesting a source starts with an empty context window. Every token
it spends rediscovering the wiki is a token not spent reasoning about the source.
This script does the cross-link lookup once, in the parent, so the subagent can be
handed a small packet instead of being told to read the whole index.

Given a source file, it scans for the names the source references — explicit
`[[wikilinks]]`, frontmatter targets (aliases, relationships, parent_location),
and capitalized multi-word proper nouns in the body — and matches them against
wiki/index.md's page set. It prints two short lists:

    EXISTING PAGES   slug — summary   (link these by slug; don't open the page)
    CANDIDATE STUBS  name             (no page yet; report if a durable object)

The packet is advisory. The subagent still decides what is a durable link versus
a passing mention; this just saves it from rebuilding the map every time.

Usage:
    ingest_packet.py Inbox/Foo.md
    ingest_packet.py Inbox/Foo.md Inbox/Bar.md   # one packet per source
"""

from __future__ import annotations

import argparse
import os
import re
import sys

from wiki_common import (
    first_h1,
    get_summary,
    iter_wiki_files,
    parse_fields,
    rel,
    split_frontmatter,
)

# Frontmatter keys whose values name other entities worth resolving.
LINK_FIELDS = (
    "parent_location",
    "region",
    "governance",
)
LIST_LINK_FIELDS = (
    "aliases",
    "relationships",
)

# Common words that start a sentence and would otherwise look like proper nouns.
STOPWORDS = {
    "The", "A", "An", "This", "That", "These", "Those", "He", "She", "It",
    "They", "We", "You", "I", "His", "Her", "Its", "Their", "Our", "Not",
    "No", "When", "Where", "What", "Who", "Why", "How", "If", "And", "But",
    "Or", "So", "For", "Of", "In", "On", "At", "To", "From", "With", "By",
    "DM", "PC", "NPC", "Stub",
}


def slugify(name: str) -> str:
    name = name.strip().strip("\"'")
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "-", name)
    return name.lower().strip("-")


def build_index() -> tuple[dict, dict]:
    """Return (slug -> summary) and (lowercased title -> slug) for all wiki pages."""
    by_slug: dict[str, str] = {}
    title_to_slug: dict[str, str] = {}
    for path in iter_wiki_files():
        slug = os.path.splitext(os.path.basename(path))[0]
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        fm_lines, body, _ = split_frontmatter(text)
        fields = parse_fields(fm_lines)
        summary = get_summary(fields)
        title = first_h1(body) or slug.replace("-", " ")
        by_slug[slug] = summary
        title_to_slug.setdefault(title.lower(), slug)
        title_to_slug.setdefault(slug.replace("-", " "), slug)
    return by_slug, title_to_slug


def wikilink_targets(text: str) -> list[str]:
    out = []
    for m in re.finditer(r"\[\[([^\]]+)\]\]", text):
        target = m.group(1).split("|", 1)[0].split("#", 1)[0].strip()
        # Path-style links ([[content/.../giant-frog]]) resolve by basename.
        if "/" in target:
            target = target.rstrip("/").rsplit("/", 1)[-1]
        if target:
            out.append(target)
    return out


def frontmatter_targets(fm_lines: list[str]) -> list[str]:
    out: list[str] = []
    fields = parse_fields(fm_lines)
    for key in LINK_FIELDS:
        val = fields.get(key, "")
        out.extend(wikilink_targets(val))
        bare = val.strip().strip("\"'")
        if bare and "[[" not in val and not bare.lower().startswith(("ungoverned", "none")):
            out.append(bare)
    # List fields span multiple indented lines; scan the raw block for links + bare items.
    raw = "\n".join(fm_lines)
    for key in LIST_LINK_FIELDS:
        block = re.search(rf"^{key}:\s*\n((?:[ \t]+[-].*\n?)+)", raw, re.MULTILINE)
        if block:
            for line in block.group(1).splitlines():
                item = line.strip().lstrip("-").strip()
                out.extend(wikilink_targets(item))
                m = re.search(r"target:\s*(.+)$", item)
                if m:
                    out.extend(wikilink_targets(m.group(1)) or [m.group(1).strip().strip("\"'")])
                elif item and "[[" not in item and ":" not in item:
                    out.append(item.strip("\"'"))
    return out


def body_proper_nouns(body: str) -> list[str]:
    # Drop wikilinks (handled separately) and code spans before scanning prose.
    cleaned = re.sub(r"\[\[[^\]]+\]\]", " ", body)
    cleaned = re.sub(r"`[^`]*`", " ", cleaned)
    names: list[str] = []
    # Capitalized runs of 2+ words: "Black-Jaw Run", "The Low Lamp".
    for m in re.finditer(r"\b([A-Z][\w'’-]+(?:\s+[A-Z][\w'’-]+){1,3})\b", cleaned):
        phrase = m.group(1)
        # Trim a leading stopword like "The" so "The Low Lamp" can match "Low Lamp" too.
        words = phrase.split()
        if words[0] in STOPWORDS and len(words) > 1:
            names.append(" ".join(words[1:]))
        names.append(phrase)
    return names


def resolve(name: str, by_slug: dict, title_to_slug: dict) -> str | None:
    slug = slugify(name)
    if slug in by_slug:
        return slug
    low = name.strip().strip("\"'").lower()
    if low in title_to_slug:
        return title_to_slug[low]
    return None


def packet_for(source: str, by_slug: dict, title_to_slug: dict) -> str:
    with open(source, "r", encoding="utf-8") as fh:
        text = fh.read()
    fm_lines, body, _ = split_frontmatter(text)

    explicit = wikilink_targets(text) + frontmatter_targets(fm_lines)
    explicit_set = {n.strip() for n in explicit if n.strip()}
    body_names = body_proper_nouns(body)

    existing: dict[str, str] = {}
    candidate_stubs: list[str] = []
    seen_candidates: set[str] = set()

    # Explicit references: resolve, and surface unresolved ones as candidate stubs.
    for name in sorted(explicit_set):
        slug = resolve(name, by_slug, title_to_slug)
        if slug:
            existing[slug] = by_slug.get(slug, "")
        else:
            key = name.lower()
            if key not in seen_candidates:
                seen_candidates.add(key)
                candidate_stubs.append(name)

    # Body proper nouns: only surface if they resolve to a real page (low false-positive).
    for name in body_names:
        slug = resolve(name, by_slug, title_to_slug)
        if slug and slug not in existing:
            existing[slug] = by_slug.get(slug, "")

    lines = [f"# Context packet for {rel(source)}", ""]
    lines.append("EXISTING PAGES (link by slug; don't open unless you must edit):")
    if existing:
        for slug in sorted(existing):
            summary = existing[slug] or "(no summary)"
            lines.append(f"- {slug} — {summary}")
    else:
        lines.append("- (none detected)")
    lines.append("")
    lines.append("CANDIDATE STUBS (no page yet; report if a durable campaign object):")
    if candidate_stubs:
        for name in candidate_stubs:
            lines.append(f"- {name}")
    else:
        lines.append("- (none detected)")
    return "\n".join(lines)


def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="source file(s) to build packets for")
    args = ap.parse_args(argv)

    missing = [s for s in args.sources if not os.path.isfile(s)]
    if missing:
        for s in missing:
            sys.stderr.write(f"ingest_packet: not found — {s}\n")
        return 1

    by_slug, title_to_slug = build_index()
    out = []
    for source in args.sources:
        out.append(packet_for(source, by_slug, title_to_slug))
    print("\n\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

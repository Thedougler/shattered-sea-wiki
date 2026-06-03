#!/usr/bin/env python3
"""Verify the tag taxonomy's two sources of truth stay in sync.

`tag_taxonomy.py` is the machine-readable source of truth; `wiki/system/taxonomy.md`
is the human-readable one. They can drift silently when a tag is added to one but not
the other. This script parses the markdown and compares it against the module, reporting
any mismatch and exiting non-zero on drift (so it can gate a commit or a lint run).

Checks:
  - CANONICAL: exact bidirectional match against the "## Canonical Tags" section.
  - ALIASES: every module alias key appears in the "## Alias Map" section (py ⊆ md).
  - DEPRECATED_*: every module deprecated tag appears in the "## Deprecated Tags" section.

Usage:
    check_taxonomy_sync.py            # report drift; exit 1 if any
    check_taxonomy_sync.py --quiet    # only print on drift
"""

from __future__ import annotations

import os
import re
import sys

import tag_taxonomy
from wiki_common import REPO_ROOT

TAXONOMY_MD = os.path.join(REPO_ROOT, "wiki", "system", "taxonomy.md")

_BACKTICK = re.compile(r"`([^`]+)`")


def split_sections(text: str) -> dict[str, str]:
    """Split markdown into {h2_title: body} by '## ' headers (ignoring deeper headers)."""
    sections: dict[str, str] = {}
    current = "_preamble"
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("###"):
            sections[current] = "\n".join(buf)
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf)
    return sections


def _first_backtick_tokens(section: str) -> set[str]:
    """First backticked token of each markdown table data row in the section."""
    tokens: set[str] = set()
    for line in section.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if set(s) <= set("|-: "):  # table divider row
            continue
        m = _BACKTICK.search(s)
        if m:
            tokens.add(m.group(1).strip().lower())
    return tokens


def _all_backtick_tokens(section: str) -> set[str]:
    """Every backticked token in the section, lowercased."""
    return {t.strip().lower() for t in _BACKTICK.findall(section)}


def parse_markdown(text: str) -> dict[str, set[str]]:
    sections = split_sections(text)
    canonical = _first_backtick_tokens(sections.get("Canonical Tags", ""))
    aliases = _all_backtick_tokens(sections.get("Alias Map", ""))
    deprecated = _all_backtick_tokens(sections.get("Deprecated Tags", ""))
    return {"canonical": canonical, "aliases": aliases, "deprecated": deprecated}


def check(module=tag_taxonomy, md_text: str | None = None) -> list[str]:
    """Return a list of drift messages. Empty list means in sync."""
    if md_text is None:
        with open(TAXONOMY_MD, encoding="utf-8") as fh:
            md_text = fh.read()
    md = parse_markdown(md_text)
    problems: list[str] = []

    py_canon = {c.lower() for c in module.CANONICAL}
    missing_in_md = py_canon - md["canonical"]
    extra_in_md = md["canonical"] - py_canon
    if missing_in_md:
        problems.append(
            f"canonical: in tag_taxonomy.py but not taxonomy.md: {sorted(missing_in_md)}"
        )
    if extra_in_md:
        problems.append(
            f"canonical: in taxonomy.md but not tag_taxonomy.py: {sorted(extra_in_md)}"
        )

    py_alias_keys = {a.lower() for a in module.ALIASES}
    alias_missing = py_alias_keys - md["aliases"]
    if alias_missing:
        problems.append(
            f"aliases: in tag_taxonomy.py but not documented in taxonomy.md: {sorted(alias_missing)}"
        )

    py_deprecated = {
        t.lower()
        for grp in (
            module.DEPRECATED_FRONTMATTER,
            module.DEPRECATED_ENTITY_NAMES,
            module.DEPRECATED_SOURCE,
            module.DEPRECATED_SYSTEM,
        )
        for t in grp
    }
    dep_missing = py_deprecated - md["deprecated"]
    if dep_missing:
        problems.append(
            f"deprecated: in tag_taxonomy.py but not listed in taxonomy.md: {sorted(dep_missing)}"
        )

    return problems


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    problems = check()
    if problems:
        print(
            "check_taxonomy_sync: DRIFT detected between tag_taxonomy.py and taxonomy.md"
        )
        for p in problems:
            print(f"  - {p}")
        return 1
    if not quiet:
        print(
            "check_taxonomy_sync: tag_taxonomy.py and wiki/system/taxonomy.md are in sync"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

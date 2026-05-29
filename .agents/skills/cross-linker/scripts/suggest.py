#!/usr/bin/env python3
"""Suggest related pages for an orphaned wiki/raw markdown file via QMD semantic search.

Usage (from vault root):
    python .claude/skills/cross-linker/scripts/suggest.py <vault-relative-path>

For content/ orphans → searches the raw QMD collection (find source material).
For raw/ orphans     → searches the wiki QMD collection (find related wiki pages).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import frontmatter

# Maps collection name → relative path prefix for results returned by that collection.
_COLLECTION_PREFIXES: dict[str, str] = {
    "shattered_sea_wiki": "content/shattered-sea/",
    "shattered_sea_raw": "raw/",
}


# ---------------------------------------------------------------------------
# Public helpers (testable without subprocess)
# ---------------------------------------------------------------------------


def get_collection(
    orphan_path: str,
    wiki_col: str,
    raw_col: str,
) -> tuple[str, str]:
    """Return (collection_name, result_path_prefix) for the given vault-relative orphan path.

    content/ orphans → search raw collection (find source material to link from).
    raw/ orphans     → search wiki collection (find wiki pages it relates to).
    """
    if orphan_path.startswith("content/"):
        return raw_col, _COLLECTION_PREFIXES.get(raw_col, "raw/")
    if orphan_path.startswith("raw/"):
        return wiki_col, _COLLECTION_PREFIXES.get(wiki_col, "content/shattered-sea/")
    raise ValueError(f"Unrecognised path prefix for orphan: {orphan_path!r}")


def build_query(title: str, tags: list[str], summary: str) -> str:
    """Build a QMD keyword search string from frontmatter fields."""
    parts: list[str] = [title]
    if tags:
        parts.append(" ".join(tags[:4]))
    if summary:
        words = summary.split()[:15]
        parts.append(" ".join(words))
    raw = " ".join(parts)
    # Strip non-ASCII characters (em dashes, curly quotes, etc.) that break qmd search
    return re.sub(r"[^\x00-\x7F]+", " ", raw).strip()


def parse_results(output: str, path_prefix: str) -> list[tuple[str, str]]:
    """Parse ``qmd search``/``vsearch`` stdout into (full_vault_relative_path, score) pairs."""
    results: list[tuple[str, str]] = []
    current_path: str | None = None

    for line in output.splitlines():
        # Path line — two formats:
        #   search:  "some/path.md:22 #abc123"
        #   vsearch: "qmd://collection-name/some/path.md:22 #abc123"
        path_match = re.match(r"^(?:qmd://[^/]+/)?(\S+\.md)(?::\d+)?\s+#\w+", line)
        if path_match:
            current_path = path_prefix + path_match.group(1)
            continue

        # Score line looks like: "Score:  96%"
        score_match = re.match(r"^Score:\s+(\d+%)", line)
        if score_match and current_path is not None:
            results.append((current_path, score_match.group(1)))
            current_path = None

    return results


def run_search(query: str, collection: str, limit: int = 3, cmd: str = "vsearch") -> str:
    """Run a qmd search command and return its stdout.

    ``cmd`` selects the search mode:
    - ``"search"``  — BM25 keyword search; fast and precise for short title-only queries.
    - ``"vsearch"`` — vector similarity; better for multi-keyword semantic queries.
    """
    result = subprocess.run(
        ["qmd", cmd, query, "--collection", collection, "--limit", str(limit)],
        capture_output=True,
        text=True,
    )
    return result.stdout


def _load_env(vault_root: Path | None = None) -> dict[str, str]:
    root = vault_root or Path.cwd()
    env_path = root / ".env"
    env: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def suggest(
    vault_relative_path: str,
    vault_root: Path | None = None,
    limit: int = 3,
) -> list[str]:
    """Return formatted suggestion lines for a vault-relative orphan path."""
    root = vault_root or Path.cwd()
    env = _load_env(root)
    wiki_col = env.get("QMD_WIKI_COLLECTION", "shattered_sea_wiki")
    raw_col = env.get("QMD_RAW_COLLECTION", "shattered_sea_raw")

    collection, prefix = get_collection(vault_relative_path, wiki_col, raw_col)

    filepath = root / vault_relative_path
    if not filepath.exists():
        return []

    post = frontmatter.load(str(filepath))
    title = str(post.get("title", filepath.stem.replace("-", " ")))
    tags = list(post.get("tags", []))
    summary = str(post.get("summary", ""))

    # Step 1: BM25 with title only — fast and precise for exact entity names.
    # Long compound queries break BM25; title alone is the most reliable signal.
    output = run_search(title, collection, limit, cmd="search")
    pairs = parse_results(output, prefix)

    if not pairs:
        # Step 2: Vector similarity with title + tags — handles semantic matches
        # when BM25 finds nothing (e.g. entity not mentioned by exact name in sources).
        vsearch_query = " ".join(filter(None, [title] + tags[:4]))
        output = run_search(vsearch_query, collection, limit, cmd="vsearch")
        pairs = parse_results(output, prefix)

    return [f"  → {path} ({score})" for path, score in pairs]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: suggest.py <vault-relative-path>", file=sys.stderr)
        sys.exit(1)
    for line in suggest(sys.argv[1]):
        print(line)


if __name__ == "__main__":
    main()

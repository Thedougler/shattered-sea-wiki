#!/usr/bin/env bash
# orphans-clean — wrapper for 'obsidian orphans' that strips non-wiki noise
#
# Usage: orphans-clean.sh [-limit N] [-suggest]
#
#   -limit N    Cap number of orphan results returned
#   -suggest    For each orphan, print top 3 related pages via QMD semantic search
#               (content/ orphans search the raw collection; raw/ orphans search wiki)
#
# Removes:
#   raw/assets/**              — binary assets (images, maps)
#   templates/**               — page templates
#   tests/**                   — test fixtures and pycache
#   CLAUDE.md, GEMINI.md,
#   AGENTS.md, hot.md,
#   log.md, README.md          — system/meta files (at any depth)
#   non-.md files              — PDFs, images, config, compiled files

limit=""
suggest=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -limit)   limit="$2"; shift 2 ;;
    -suggest) suggest=1; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

results=$(obsidian orphans | grep -E '^(raw|content)/' | grep -vE \
  '^raw/assets/' | grep -vE \
  '(^|/)CLAUDE\.md$|(^|/)GEMINI\.md$|(^|/)AGENTS\.md$' | grep -vE \
  '(^|/)hot\.md$|(^|/)log\.md$|(^|/)README\.md$' | grep -E \
  '\.md$')

if [[ -n "$limit" ]]; then
  results=$(echo "$results" | head -n "$limit")
fi

if [[ "$suggest" -eq 1 ]]; then
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    echo "$line"
    python3 "$SCRIPT_DIR/suggest.py" "$line"
  done <<< "$results"
else
  echo "$results"
fi


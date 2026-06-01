#!/usr/bin/env bash
# PostToolUse hook: warn on unresolved [[wikilinks]] in edited wiki markdown files.
# Runs after Write|Edit on wiki/**/*.md files only.

set -euo pipefail

FILE="$(echo "$CLAUDE_TOOL_INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('file_path',''))" 2>/dev/null || true)"

# Only check wiki markdown files
case "$FILE" in
  */wiki/*.md) ;;
  *) exit 0 ;;
esac

[ -f "$FILE" ] || exit 0

WIKI_DIR="$(cd "$(dirname "$FILE")" && while [ ! -d "wiki" ] && [ "$PWD" != "/" ]; do cd ..; done; echo "$PWD/wiki")"
[ -d "$WIKI_DIR" ] || exit 0

# Extract [[wikilink]] targets (strip display text after |, strip heading after #)
LINKS="$(grep -oE '\[\[[^]]+\]\]' "$FILE" 2>/dev/null | sed 's/\[\[//;s/\]\]//;s/|.*//;s/#.*//' | sort -u || true)"

[ -z "$LINKS" ] && exit 0

MISSING=""
while IFS= read -r link; do
  [ -z "$link" ] && continue
  # Skip asset embeds (image/audio/video links with known extensions)
  case "$link" in
    *.webp|*.png|*.jpg|*.jpeg|*.gif|*.svg|*.mp3|*.m4a|*.wav|*.mp4|*.pdf) continue ;;
  esac
  # Normalize: lowercase, spaces to hyphens
  slug="$(echo "$link" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
  # Search for matching .md file anywhere in wiki/
  found="$(find "$WIKI_DIR" -type f -iname "${slug}.md" 2>/dev/null | head -1)"
  if [ -z "$found" ]; then
    MISSING="${MISSING}\n  [[${link}]]"
  fi
done <<< "$LINKS"

if [ -n "$MISSING" ]; then
  echo "Unresolved wikilinks in $(basename "$FILE"):${MISSING}"
  echo "(These may resolve after creating the target file.)"
fi

exit 0

#!/usr/bin/env bash
# PostToolUse hook: validate-frontmatter.sh
# Fires after every Write or Edit tool call.
# Checks that wiki markdown files have valid frontmatter and a current updated: date.
# Always exits 0 — advisory output only, never blocks the tool call.

set -euo pipefail

# Extract file_path from CLAUDE_TOOL_INPUT env var (JSON object)
FILE=$(python3 -c "
import sys, json, os
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    d = json.loads(raw)
    print(d.get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

# Only process markdown files inside the wiki/ directory
[[ "$FILE" == *.md ]] || exit 0
[[ "$FILE" == */wiki/* ]] || exit 0
[[ -f "$FILE" ]] || exit 0

# Require YAML frontmatter block (file must start with ---)
if ! head -1 "$FILE" | grep -q "^---$"; then
  echo "HOOK: missing frontmatter — $FILE" >&2
  exit 0
fi

# Extract frontmatter (lines between first and second --- delimiters)
FRONTMATTER=$(awk 'NR==1{next} /^---$/{exit} {print}' "$FILE")

# Required universal fields per CLAUDE.md
REQUIRED_FIELDS=("type" "subtype" "campaign" "status" "audience" "publish" "summary" "created" "updated" "tags" "sources")

MISSING=()
for field in "${REQUIRED_FIELDS[@]}"; do
  if ! echo "$FRONTMATTER" | grep -q "^${field}:"; then
    MISSING+=("$field")
  fi
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "HOOK: missing fields [${MISSING[*]}] — $FILE" >&2
fi

# Check updated: date matches today
TODAY=$(date +%Y-%m-%d)
UPDATED=$(echo "$FRONTMATTER" | grep "^updated:" | awk '{print $2}' | tr -d '"' | head -1)
if [[ -n "$UPDATED" && "$UPDATED" != "$TODAY" ]]; then
  echo "HOOK: updated: is $UPDATED, should be $TODAY — $FILE" >&2
fi

exit 0

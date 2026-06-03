#!/usr/bin/env bash
# PostToolUse hook: validate-frontmatter.sh
# Fires after every Write or Edit tool call.
# Auto-completes frontmatter on wiki markdown files (adds missing required
# fields with path-inferred defaults, stamps `updated:` to today) by delegating
# to .claude/scripts/fix_frontmatter.py. The model no longer has to do this by
# hand — the "automatic behaviors on every write" are now genuinely automatic.
# Only judgment items (a still-default summary) are surfaced. Always exits 0.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

FILE=$(python3 -c "
import sys, json, os
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    print(json.loads(raw).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

# Only process markdown files inside the wiki/ directory.
[[ "$FILE" == *.md ]] || exit 0
[[ "$FILE" == */wiki/* ]] || exit 0
[[ -f "$FILE" ]] || exit 0

SEA="$REPO_ROOT/packages/cli/dist/cli.js"
if [[ -f "$SEA" ]]; then
  node "$SEA" fix "$FILE" --vault "$REPO_ROOT/wiki" || true
else
  python3 "$REPO_ROOT/.claude/scripts/fix_frontmatter.py" "$FILE" || true
fi
exit 0

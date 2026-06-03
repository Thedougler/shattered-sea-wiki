#!/usr/bin/env bash
# PostToolUse hook: regen-index.sh
# Fires after every Write or Edit. When a markdown file under wiki/ changed, regenerate
# wiki/index.md from frontmatter so the in-context index stays current — WITHOUT making the
# agent wait. A full regen scans the whole vault, so this detaches into the background and
# uses a lockfile so a burst of edits coalesces into a single trailing run.
# Loop-guard: skips when the edited file IS wiki/index.md (regen rewrites that file and would
# otherwise retrigger itself). Always exits 0 — index regen must never block or fail a write.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOCK="/tmp/regen-index-shattered-sea.lock"
LOG="/tmp/regen-index-shattered-sea.log"

FILE=$(python3 -c "
import os, json
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    print(json.loads(raw).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

# Only react to markdown inside the vault.
[[ "$FILE" == *.md ]] || exit 0
[[ "$FILE" == */wiki/* ]] || exit 0

# Loop-guard: never react to index.md itself.
[[ "$(basename "$FILE")" == "index.md" ]] && exit 0

# Skip if a regen is already queued/running (lockfile held by a live process).
if [[ -f "$LOCK" ]] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi

# Detach: brief settle delay (let an edit burst finish), then regenerate. Fully backgrounded.
(
  echo $$ > "$LOCK"
  trap 'rm -f "$LOCK"' EXIT
  sleep 3
  cd "$REPO_ROOT"
  SEA="$REPO_ROOT/packages/cli/dist/cli.js"
  if [[ -f "$SEA" ]]; then
    node "$SEA" index --write --vault "$REPO_ROOT/wiki" >>"$LOG" 2>&1 || true
  else
    python3 .claude/scripts/regen_index.py --write >>"$LOG" 2>&1 || true
  fi
) >/dev/null 2>&1 &

disown 2>/dev/null || true
exit 0

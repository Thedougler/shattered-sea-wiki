#!/usr/bin/env bash
# PostToolUse hook: qmd-reindex.sh
# Fires after every Write or Edit. When a markdown file under wiki/ or .raw/ changed,
# refresh the qmd index so ttrpg-wiki-query's search stays current — WITHOUT making the
# agent wait. Re-indexing (and especially embedding) is slow, so this detaches into the
# background and uses a lockfile so overlapping writes don't stack runs. A single trailing
# run after a burst of edits is enough: it picks up everything changed since last time.
# Always exits 0 — a search-index refresh must never block or fail a wiki write.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOCK="/tmp/qmd-reindex-shattered-sea.lock"
LOG="/tmp/qmd-reindex-shattered-sea.log"

FILE=$(python3 -c "
import os, json
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    print(json.loads(raw).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

# Only react to markdown inside the two indexed collections.
[[ "$FILE" == *.md ]] || exit 0
[[ "$FILE" == */wiki/* || "$FILE" == */.raw/* ]] || exit 0

command -v qmd >/dev/null 2>&1 || exit 0

# Skip if a refresh is already queued/running (lockfile held by a live process).
if [[ -f "$LOCK" ]] && kill -0 "$(cat "$LOCK" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi

# Detach: brief settle delay (let an edit burst finish), then incremental re-index and a
# background embed pass for semantic freshness. Fully backgrounded so the agent never waits.
(
  echo $$ > "$LOCK"
  trap 'rm -f "$LOCK"' EXIT
  sleep 3
  cd "$REPO_ROOT"
  qmd update >>"$LOG" 2>&1 || true
  qmd embed  >>"$LOG" 2>&1 || true
) >/dev/null 2>&1 &

disown 2>/dev/null || true
exit 0

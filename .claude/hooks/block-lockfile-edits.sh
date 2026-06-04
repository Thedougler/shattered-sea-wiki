#!/usr/bin/env bash
# PreToolUse hook: block-lockfile-edits.sh
# Fires before Write or Edit. Blocks direct edits to pnpm-lock.yaml —
# lockfile changes must go through pnpm install/add/remove.

set -euo pipefail

FILE=$(python3 -c "
import os, json
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    print(json.loads(raw).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

case "$FILE" in
  *pnpm-lock.yaml|*package-lock.json|*yarn.lock)
    echo "BLOCKED: refusing to edit $FILE directly — use pnpm install/add/remove instead."
    exit 1
    ;;
esac

exit 0

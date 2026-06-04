#!/usr/bin/env bash
# PostToolUse hook: biome-fix.sh
# Fires after Write|Edit on .ts/.tsx files. Runs biome check --fix on the changed file.
# Always exits 0 — formatting should not block edits.

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
  *.ts|*.tsx) ;;
  *) exit 0 ;;
esac

[[ -f "$FILE" ]] || exit 0

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
npx --prefix "$REPO_ROOT" @biomejs/biome check --fix "$FILE" 2>/dev/null || true
exit 0

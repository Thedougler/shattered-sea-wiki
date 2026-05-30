#!/usr/bin/env bash
# PostToolUse hook: format-python.sh
# Fires after Write|Edit on .py files. Runs ruff format on the changed file.
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

[[ "$FILE" == *.py ]] || exit 0
[[ -f "$FILE" ]] || exit 0

ruff format "$FILE" 2>&1 || true
exit 0

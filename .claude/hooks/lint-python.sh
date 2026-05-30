#!/usr/bin/env bash
# PostToolUse hook: lint-python.sh
# Fires after Write|Edit on .py files. Runs ruff check on the changed file.
# Non-zero exit blocks the tool call, surfacing the error to the agent.

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

ruff check "$FILE" 2>&1

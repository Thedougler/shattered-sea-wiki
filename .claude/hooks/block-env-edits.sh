#!/usr/bin/env bash
# PreToolUse hook: block-env-edits.sh
# Fires before Write or Edit. Blocks edits to .env files to prevent
# accidental exposure of HF_TOKEN and other secrets. Non-zero exit blocks
# the tool call.

set -euo pipefail

FILE=$(python3 -c "
import os, json
raw = os.environ.get('CLAUDE_TOOL_INPUT', '{}') or '{}'
try:
    print(json.loads(raw).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null || true)

if [[ "$FILE" == *.env || "$FILE" == */.env.* ]]; then
  echo "BLOCKED: refusing to edit $FILE — .env files may contain secrets."
  exit 1
fi

exit 0

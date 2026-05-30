#!/usr/bin/env bash
# Live session transcription (Pass 1). Start at session open, leave running, Ctrl-C to stop.
#
#   ./transcribe_session.sh --session 4 --speakers 5
#
# Writes a growing speaker-attributed transcript + silence-chunked audio under
# wiki/sessions/.live/session-NN/ (gitignored scratch). After the game, run
# ./finalize_session.sh to produce the canonical transcript.
#
# All flags are passed straight through to transcribe_session.py:
#   --session N    session number (auto-picks next if omitted)
#   --speakers N   physical people at the table — always set it; biggest accuracy win
#   --threshold F  voice-ID cosine cutoff (default 0.5)

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/.claude/skills/live-co-dm/scripts/_bootstrap.sh"

cd "$REPO_ROOT"   # script writes to wiki/sessions/.live relative to cwd
exec "$VENV_PY" "$SCRIPT_DIR/transcribe_session.py" "$@"

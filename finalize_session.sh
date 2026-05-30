#!/usr/bin/env bash
# Finalize a session transcript (Pass 2 — offline, high-accuracy re-pass).
#
#   ./finalize_session.sh --session 4 --speakers 5
#
# Re-diarizes the whole recording at once with the known speaker count and writes
# the committed wiki/sessions/session-NN-transcript.md. Needs the session's
# .live/session-NN/audio/ directory (gitignored scratch) to still be present.
#
# All flags are passed straight through:
#   --session N    session number (required)
#   --speakers N   known physical speaker count
#   --threshold F  voice-ID cosine cutoff (default 0.5)

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/voice-transcription/_bootstrap.sh"

cd "$REPO_ROOT"
exec "$VENV_PY" -m voice_transcription.cli.finalize "$@"

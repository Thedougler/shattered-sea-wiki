#!/usr/bin/env bash
# Save / improve a character voice profile.
#
#   ./save_voice.sh --name "Grigori" --player "Dave"
#
# Then open the printed URL, read the teleprompter aloud in character, Stop & Save.
# Re-running with the same --name overwrites that profile (and folds in corrected
# audio from finalized transcripts — see voice-transcription/references/voice-profiler.md).
#
# All flags are passed straight through:
#   --name        character voice (required)   --player  performing person (required)
#   --script-file custom teleprompter text      --port    web port (default 8080)

set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/voice-transcription/_bootstrap.sh"

exec "$VENV_PY" -m voice_transcription.cli.save_voice "$@"

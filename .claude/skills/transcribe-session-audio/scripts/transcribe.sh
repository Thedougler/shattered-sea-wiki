#!/usr/bin/env bash
# Transcribe a recorded session into per-part speaker CSVs.
#
# Thin wrapper over `shattered-audio transcribe-session` — reads the per-mic
# m4a tracks under audio/sessions/sessionNN/ and writes sessionNN-partMM.m4a.csv
# (ID,Start,End,Speaker,Text), the format the session-ingest skill consumes.
# Voice profiles are auto-loaded by default.
#
# Usage:
#   transcribe.sh --session 7
#   transcribe.sh --session 7 --no-profiles
#   transcribe.sh --session 7 --save-profile "Nick" --from-mic mic01
#   transcribe.sh --session 7 --save-profile "Grigori" --from-mic mic01 --actor Nick
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"   # scripts → skill → skills → .claude → repo root
SA="$REPO/tools/audio/.venv/bin/shattered-audio"

if [[ ! -x "$SA" ]]; then
  echo "shattered-audio not installed. Set it up with:" >&2
  echo "  cd $REPO/tools/audio && python3 -m venv .venv && .venv/bin/pip install -e '.[all]'" >&2
  exit 1
fi

cd "$REPO"
exec "$SA" transcribe-session "$@"

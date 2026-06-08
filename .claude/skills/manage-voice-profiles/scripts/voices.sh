#!/usr/bin/env bash
# Convenience wrapper for voice profile management.
#
# Usage:
#   voices.sh profiles                          # list all actors + personas
#   voices.sh profiles "Nick"                   # detail for one actor
#   voices.sh enroll "Nick" --record 30         # enroll actor (natural voice)
#   voices.sh enroll "Nick" --record 30 --dm    # enroll as DM
#   voices.sh enroll "Crissdalyn" --actor "Nick" --record 30  # enroll persona
#   voices.sh delete "Nick"                     # delete actor + all personas
#   voices.sh delete "Crissdalyn" --actor "Nick"  # delete one persona
#   voices.sh watch                             # live speaker-ID TUI
#   voices.sh devices                           # list mic device indices
#
# All arguments are passed through to `shattered-audio`.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"   # scripts → skill → skills → .claude → repo root
SA="$REPO/tools/audio/.venv/bin/shattered-audio"

if [[ ! -x "$SA" ]]; then
  echo "shattered-audio not installed. Run:" >&2
  echo "  cd $REPO/tools/audio && python3 -m venv .venv && .venv/bin/pip install -e '.[all]'" >&2
  exit 1
fi

cd "$REPO"
exec "$SA" "$@"

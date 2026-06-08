#!/usr/bin/env bash
# Fire-and-wait multi-mic session recorder.
#
# Thin wrapper over `shattered-audio record` — records every available mic to
# its own isolated, chunked m4a track under audio/sessions/sessionNN/. Built to
# run for 4+ hours and stop cleanly on SIGTERM/SIGINT (finalizing the current
# chunk), so the controlling agent can end the session on command.
#
# Run it with the Bash tool's run_in_background:true, then STOP and wait. Do not
# poll it. To end recording, kill the background shell — ffmpeg shuts down
# gracefully.
#
# Usage: record.sh --session 7 [--segment-minutes 15] [--mics 0,1]
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"   # scripts → skill → skills → .claude → repo root
SA="$REPO/tools/audio/.venv/bin/shattered-audio"

if [[ ! -x "$SA" ]]; then
  echo "shattered-audio not installed. Set it up with:" >&2
  echo "  cd $REPO/tools/audio && python3 -m venv .venv && .venv/bin/pip install -e '.[all]'" >&2
  exit 1
fi

cd "$REPO"   # so the default --audio-dir audio/sessions resolves to the repo
exec "$SA" record "$@"

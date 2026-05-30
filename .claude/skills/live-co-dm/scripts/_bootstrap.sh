#!/usr/bin/env bash
# Shared bootstrap for the human-facing live-co-dm wrappers
# (save_voice.sh / transcribe_session.sh / finalize_session.sh).
#
# Ensures the venv + dependencies exist, loads HF_TOKEN from .env, and leaves the
# venv active. Source this, then call the target script via "$VENV_PY".
#
# Resolves paths from this file's own location, so the wrappers work regardless of
# the caller's working directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"          # .../live-co-dm/scripts
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"                            # .../live-co-dm
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"                       # repo root
VENV_DIR="$SKILL_DIR/.venv"
REQUIREMENTS="$SKILL_DIR/requirements.txt"
DEPS_STAMP="$VENV_DIR/.deps-installed"
VENV_PY="$VENV_DIR/bin/python3"

log() { printf '\033[1;36m[live-co-dm]\033[0m %s\n' "$*" >&2; }
die() { printf '\033[1;31m[live-co-dm] error:\033[0m %s\n' "$*" >&2; exit 1; }

# --- 1. Python -------------------------------------------------------------
# parakeet-mlx (and the rest of the ML stack) needs Python >= 3.11. The bare
# `python3` on this machine is often an older pyenv/system shim (e.g. 3.9), so
# pick the first interpreter that actually meets the floor instead of trusting
# whatever `python3` happens to resolve to.
MIN_MAJOR=3
MIN_MINOR=11

py_ok() {  # $1 = interpreter; succeeds if it exists, imports venv, and is new enough
  local py="$1"
  command -v "$py" >/dev/null 2>&1 || return 1
  "$py" - "$MIN_MAJOR" "$MIN_MINOR" <<'PY' >/dev/null 2>&1 || return 1
import sys
need = (int(sys.argv[1]), int(sys.argv[2]))
import venv  # noqa: F401  (ensure the venv module is available)
sys.exit(0 if sys.version_info[:2] >= need else 1)
PY
}

PYTHON=""
for cand in \
  python3.11 python3.12 python3.13 python3.14 python3 \
  /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3.12 \
  /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.14; do
  if py_ok "$cand"; then PYTHON="$cand"; break; fi
done

[[ -n "$PYTHON" ]] || die "No Python >= ${MIN_MAJOR}.${MIN_MINOR} found (required by parakeet-mlx). Install one, e.g. 'brew install python@3.11', then re-run. See .claude/skills/live-co-dm/references/setup.md."

# --- 2. Virtualenv ---------------------------------------------------------
# Rebuild the venv when it is missing, broken, or was created with a too-old
# interpreter (the common failure: a stale 3.9 venv from before this fix).
venv_too_old() {
  [[ -x "$VENV_PY" ]] || return 0   # missing/broken -> needs (re)build
  ! "$VENV_PY" - "$MIN_MAJOR" "$MIN_MINOR" <<'PY' >/dev/null 2>&1
import sys
sys.exit(0 if sys.version_info[:2] >= (int(sys.argv[1]), int(sys.argv[2])) else 1)
PY
}

if venv_too_old; then
  if [[ -e "$VENV_DIR" ]]; then
    log "Existing virtualenv uses an unsupported Python; rebuilding at $VENV_DIR ..."
    rm -rf "$VENV_DIR"
    rm -f "$DEPS_STAMP"
  fi
  log "Creating virtualenv at $VENV_DIR using $("$PYTHON" -c 'import sys;print("%d.%d.%d"%sys.version_info[:3])') ($PYTHON) ..."
  "$PYTHON" -m venv "$VENV_DIR"
fi

# --- 3. Dependencies (reinstall only when requirements.txt changes) --------
if [[ ! -f "$DEPS_STAMP" || "$REQUIREMENTS" -nt "$DEPS_STAMP" ]]; then
  log "Installing dependencies from requirements.txt (first run downloads model weights later) ..."
  "$VENV_PY" -m pip install --quiet --upgrade pip
  "$VENV_PY" -m pip install --quiet -r "$REQUIREMENTS"
  touch "$DEPS_STAMP"
fi

# --- 4. HF_TOKEN from .env (if not already set) ----------------------------
if [[ -z "${HF_TOKEN:-}" && -f "$REPO_ROOT/.env" ]]; then
  HF_TOKEN="$(grep -E '^[[:space:]]*HF_TOKEN=' "$REPO_ROOT/.env" | tail -n1 | cut -d= -f2- | tr -d '"'\''' )"
  export HF_TOKEN
fi

if [[ -z "${HF_TOKEN:-}" || "${HF_TOKEN}" == "..." ]]; then
  die "HF_TOKEN is not set. Add 'HF_TOKEN=hf_...' to $REPO_ROOT/.env (a free Hugging Face read token), or export it in your shell. See .claude/skills/live-co-dm/references/setup.md."
fi

export VENV_PY SCRIPT_DIR SKILL_DIR REPO_ROOT

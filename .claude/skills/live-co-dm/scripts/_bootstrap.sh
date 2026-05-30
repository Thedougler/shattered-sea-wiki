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
command -v python3 >/dev/null 2>&1 || die "python3 not found on PATH."

# --- 2. Virtualenv ---------------------------------------------------------
if [[ ! -x "$VENV_PY" ]]; then
  log "Creating virtualenv at $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
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

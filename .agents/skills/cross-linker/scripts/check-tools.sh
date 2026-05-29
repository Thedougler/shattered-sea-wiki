#!/usr/bin/env bash
# cross-linker: check required tools
set -euo pipefail

ok()   { printf "  %-16s %s\n" "$1" "ok"; }
warn() { printf "  %-16s %s\n" "$1" "MISSING — $2"; FAILED=1; }

FAILED=0

echo "cross-linker tool check"
echo "---"

# obsidian CLI — primary; skill requires Obsidian to be open
if obsidian help &>/dev/null; then
    ok "obsidian"
else
    warn "obsidian" "install from https://github.com/obsidianmd/obsidian-cli or open Obsidian"
fi

# git — used for 'git log --oneline -5' in Before You Start
if command -v git &>/dev/null; then
    ok "git"
else
    warn "git" "install git"
fi

# python3 — used if wiki-lint scripts are invoked post-link
if command -v python3 &>/dev/null; then
    ok "python3"
else
    warn "python3" "install python3"
fi

echo "---"
if [[ $FAILED -eq 0 ]]; then
    echo "all tools available"
else
    echo "one or more tools missing — see above"
    exit 1
fi

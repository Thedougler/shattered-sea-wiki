#!/usr/bin/env bash
set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

info()    { echo -e "${BOLD}==> $*${RESET}"; }
success() { echo -e "${GREEN}✓  $*${RESET}"; }
warn()    { echo -e "${YELLOW}!  $*${RESET}"; }

info "Checking pnpm..."
if command -v pnpm &>/dev/null; then
  success "pnpm $(pnpm --version)"
else
  info "Installing pnpm via corepack..."
  corepack enable
  corepack prepare pnpm@latest --activate
  success "pnpm installed"
fi

info "Installing dependencies..."
pnpm install
success "Dependencies installed"

info "Building packages..."
pnpm build
success "Build complete"

info "Checking Python tools..."
if [ -d tools/audio ]; then
  if [ ! -d tools/audio/.venv ]; then
    info "Creating Python venv for audio tools..."
    python3 -m venv tools/audio/.venv
    tools/audio/.venv/bin/pip install -q -r tools/audio/requirements.txt 2>/dev/null || warn "No requirements.txt in tools/audio — venv created but empty"
    success "Audio tools venv ready"
  else
    success "Audio tools venv already exists"
  fi
fi

echo ""
echo -e "${BOLD}Setup complete.${RESET}"
echo "  pnpm dev        — start UI dev server"
echo "  pnpm test       — run tests"
echo "  pnpm check      — typecheck + lint"

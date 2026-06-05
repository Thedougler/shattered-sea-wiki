---
name: vault-health
description: Use when preparing for a session, after a large batch of wiki or code edits, or when diagnosing unexplained build or content errors. Skip for single-file changes.
---

# Vault Health

Run from `/Users/nick/ai-os/shattered-sea`. **Stop at the first failure — report what to fix before continuing.**

## Checks (in order)

| # | Command | Pass condition |
|---|---------|----------------|
| 1 | `pnpm check` | No type errors or Biome violations |
| 2 | `sea lint` | Zero errors (warnings non-blocking) |
| 3 | `python3 .claude/scripts/check_taxonomy_sync.py --check` | Exits 0 |
| 4 | `sea health` | Print summary metrics only |

## Output

One status table:

| Check | Status | Notes |
|-------|--------|-------|
| TypeScript | ✓/✗ | error detail if failed |
| Wiki lint | ✓/✗ | counts if non-zero |
| Taxonomy | ✓/✗ | drifted tags if any |
| Vault snapshot | info | files, default-summaries, unresolved links |

All clean → one-line summary. Any failure → list what to fix before proceeding.

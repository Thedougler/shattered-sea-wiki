---
name: vault-health
description: Run full pre-session vault health check — typecheck, Biome lint, wiki lint, taxonomy sync. Use before sessions or before committing a large batch of changes.
---

Run the following checks in order from the workspace root. Stop at the first failure and report what to fix before continuing.

## 1. TypeScript

```bash
pnpm check
```

Reports type errors and Biome lint violations. Must be clean before proceeding.

## 2. Wiki Lint

```bash
python3 .claude/scripts/wiki_lint.py
```

Report only the summary counts (errors, warnings, orphans). Do not list every individual issue unless the error count is non-zero.

## 3. Taxonomy Sync

```bash
python3 .claude/scripts/check_taxonomy_sync.py --check
```

Exit 1 = drift between the TS module and `wiki/system/taxonomy.md`. Report which tags are out of sync.

## 4. Vault Health Snapshot

```bash
python3 .claude/scripts/wiki_health_snapshot.py
```

Print the summary section only (total files, files with default summaries, unresolved wikilinks count).

## Output Format

Present results as a compact status table:

| Check | Status | Notes |
|-------|--------|-------|
| TypeScript | ✓ / ✗ | error summary if failed |
| Wiki lint | ✓ / ✗ | counts if non-zero |
| Taxonomy | ✓ / ✗ | drifted tags if any |
| Vault snapshot | ✓ | key metrics |

If everything is clean, say so in one line. If anything failed, list what needs fixing before the session.

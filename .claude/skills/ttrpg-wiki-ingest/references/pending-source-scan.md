# Pending Source Scan

Use this workflow whenever the user asks what is pending, what has not been ingested,
or before processing an unspecified source.

## Scan Scope

Check these locations:

1. `.raw/` — canonical raw source backend.
2. `Inbox/` — uncategorized incoming material.
3. Top-level source documents when using `--include-root-docs`.

Ignore:

- `CLAUDE.md`
- `AGENTS.md`
- `README.md`
- files under `.git/`, `.claude/`, `.agents/`, `.codex/`, and `wiki/`
- OS/editor files such as `.DS_Store`

## Command

```bash
python3 .claude/skills/ttrpg-wiki-ingest/scripts/scan_pending.py --include-root-docs
```

For automations:

```bash
python3 .claude/skills/ttrpg-wiki-ingest/scripts/scan_pending.py --include-root-docs --json
```

## Interpretation

The script compares discovered source files against `wiki/ingest-registry.md`.

| State | Meaning | Action |
|---|---|---|
| `unregistered` | Source exists but registry has no row | Add row as `pending` |
| `pending` | Registry knows source but wiki outputs are not done | Triage or ingest |
| `in-progress` | A previous ingest started | Resume before starting another source |
| `blocked` | DM judgment needed | Surface exact blocker |
| `ingested` | Registry says complete | Verify outputs only if audit requested |
| `skipped` | Intentionally not wiki material | Leave unless user reopens |

If more than five files are pending or unregistered, report counts and recommend one next
source. Do not dump the full queue into chat unless the user asks.

## Priority Order

1. Reviewed clean session transcripts.
2. Session summaries or table notes.
3. DM-declared canon updates.
4. Player-facing handouts that need publication control.
5. Rules/homebrew with table impact.
6. Entity/location/faction notes.
7. Assets needing captions or source tracking.
8. Research/guidance documents.

The scanner provides a rough type and priority. The agent makes the final call after reading
the source enough to understand it.

## Registry Sync

When the scan finds unregistered sources:

1. Read `ingest-registry-update.md`.
2. Add rows with `Status` = `pending`.
3. Rebuild the Pending Queue section.
4. Log the registry sync in `wiki/log.md`.

Do not mark a source `ingested` just because a wiki page mentions it. A source is ingested
only when the durable claims have been decomposed, placed, linked, and recorded in the
registry output list.

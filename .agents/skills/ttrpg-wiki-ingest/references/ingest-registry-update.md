# Ingest Registry Update

## Purpose

Keep `wiki/ingest-registry.md` current. It should answer three questions quickly:

1. What source files exist?
2. What status is each source in?
3. Which wiki files did each source produce or update?

## Registry Table

Maintain this table:

```markdown
| File | Type | Status | Date | Wiki Outputs |
|---|---|---|---|---|
| `.raw/sessions/session-01-clean.md` | transcript | ingested | 2026-05-28 | `wiki/sessions/session-01.md`; `wiki/hot.md` |
```

Use repo-relative paths. Wrap paths in backticks. Separate multiple outputs with semicolons.

## Status Values

| Status | Use When |
|---|---|
| `pending` | File is discovered but not triaged or ingested |
| `triaged` | Expected outputs are known, but writes have not started |
| `in-progress` | Wiki writes have started but are incomplete |
| `blocked` | DM judgment or missing prerequisite stops ingest |
| `partial` | Some outputs were written, but blocked work remains |
| `ingested` | Durable claims were written, linked, indexed, logged |
| `skipped` | Source intentionally does not belong in wiki canon |
| `superseded` | A cleaner or later source replaces this source for ingest |
| `source-only` | Raw evidence retained but not directly propagated |

Do not invent new status labels unless the user asks.

## Pending Queue Section

After the table, maintain:

```markdown
## Pending Queue (status: pending, priority order)
1. `.raw/sessions/session-04-clean.md` — transcript — ready for reviewed transcript ingest
2. `Inbox/beffa-notes.md` — location-source/situation-source — needs triage
```

Include `pending`, `triaged`, `in-progress`, `blocked`, and `partial` entries. Exclude
`ingested`, `skipped`, `superseded`, and `source-only`.

Priority:

1. `in-progress`
2. `blocked` or `partial`
3. reviewed clean transcripts
4. session notes
5. DM canon updates
6. rules/homebrew
7. entity/location/faction notes
8. assets
9. research/guidance

## Discovery Sync

When scan finds an unregistered file:

1. Add a row with inferred type.
2. Set status to `pending`.
3. Set date to today's date.
4. Set wiki outputs to `—`.
5. Add it to Pending Queue.

If more than five unregistered files appear, add rows but report the count concisely. Do not
paste the entire queue into chat unless requested.

## Completion Sync

When an ingest finishes:

1. Set status to `ingested`.
2. Set date to today's date.
3. List every created or modified wiki file that contains source-derived content.
4. Rebuild Pending Queue.
5. Append `wiki/log.md`:

```markdown
- INGEST: `source/path.md` — status ingested — outputs: `wiki/path.md`, `wiki/hot.md`
```

Use `REGISTRY:` instead of `INGEST:` when only the registry changed.

## Blocked Sync

When blocked:

1. Set status to `blocked`.
2. Put the exact question in Wiki Outputs:
   `blocked: is "Black Eel" the ship or the tavern?`
3. Add the source near the top of Pending Queue.
4. Ask the DM the question in the final answer.

## Audit Checks

A registry row is stale if:

- File path no longer exists and status is not `superseded` or `skipped`.
- Status is `ingested` but outputs are `—`.
- Output path does not exist.
- Pending Queue omits a pending/blocked/partial row.
- A discovered source has no row.

Fix structural registry staleness directly. Escalate only when the fix requires a lore or
lifecycle judgment.

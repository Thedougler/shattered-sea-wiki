---
name: ttrpg-wiki-lint
metadata:
  version: "4.0"
description: >
  Lint the Shattered Sea wiki, fix what's safe to fix, and track improvement
  over time. Checks vault health: frontmatter standardization, broken wikilinks,
  orphans, deadends, lore consistency (dead entity refs, parent-location gaps,
  narrative-island mismatches, status drift), tag hygiene (aliases, deprecated,
  unknown, over-limit, variants), singleton properties.
  Auto-fixes: status-drift synonyms, lifecycle-folder mismatches, tag aliases,
  deprecated frontmatter/system tags. Supports incremental linting (--since),
  priority-ordered action lists (--top), and snapshot diffing (--diff) for
  measuring improvement.
  Trigger on: "lint the wiki", "check wiki health", "fix the frontmatter",
  "fix tags", "find broken links/orphans/deadends", "lore consistency", "check
  consistency", "status drift", "tag hygiene", "audit the wiki", "clean up the
  vault", "timeline issues", "temporal consistency",
  "what improved", "lint diff", "top issues", "highest priority fixes",
  "incremental lint", "lint changed files", "self-improvement", "wiki quality".
---

# TTRPG Wiki Lint — Shattered Sea

The `sea` CLI does the heavy lifting: `node packages/cli/dist/cli.js lint` (or
`sea lint` if linked). It splits every problem into two piles:

- **Safe, reversible -> auto-fixed** (`--fix` / `--fix-tags`): frontmatter
  completion, status-drift correction, lifecycle-folder sync, tag alias
  replacement, and deprecated tag removal. These never invent canon and never
  touch another file, so they converge in one pass.
- **Needs judgment -> reported** (never silently changed): broken wikilinks,
  off-convention filenames, orphans, deadends, invalid values, stale summaries,
  unknown tags, entity-name tags, relationships still in frontmatter. Each line
  ends with a concrete action.

---

## The loop

```
1. Lint            sea lint --top 10
2. Auto-fix safe   sea lint --fix --fix-tags   (then commit)
3. Re-lint         what remains needs you — use --top for the priority list
4. Work the report by category (below), fixing + committing as you go
5. Manual lore     check prose-level consistency on files you touched (see below)
6. Stop            when only DM-judgment items remain — surface those, don't guess
```

Don't read files one by one to assess health — run the CLI. The manual lore
pass (step 5) is for what the linter can't catch: prose contradictions, timeline
drift, and entity identity.

---

## Running it

```bash
# Report only — whole vault. Shows all issues by severity.
sea lint

# Top 10 highest-leverage actions (batches identical issues, priority-ordered).
sea lint --top 10

# Standardize frontmatter + fix safe tag issues, then report what's left.
sea lint --fix --fix-tags

# Incremental: only lint files changed since a git ref or date.
sea lint --since HEAD~5
sea lint --since 2026-06-01
sea lint --fix --since HEAD~10

# Compare against a previous snapshot (saved with --json > file.json).
sea lint --diff .claude/lint-baseline.json

# Scope to a file or directory.
sea lint --fix wiki/entities/characters/npcs/

# Just the counts.
sea lint --summary

# Only errors.
sea lint --min-severity error

# Machine-readable (includes per-rule breakdown for diffing).
sea lint --json

# Write the DM review queue.
sea lint --report
```

If `sea` is not linked, use: `node packages/cli/dist/cli.js lint`

Exit code is `1` when any **error** exists, `0` otherwise.

### Flags

| Flag | What it does |
|---|---|
| `--fix` | Standardize frontmatter (add missing fields, reorder, coerce booleans, strip junk, fix status-drift, sync lifecycle-folder) |
| `--fix-tags` | Also fix safe tag issues: replace aliases with canonical forms, remove deprecated-fm and deprecated-system tags. Implies `--fix`. |
| `--since REF` | Only lint files changed since a git ref or date. Accepts SHA, branch, tag, or date string. |
| `--top N` | Show the top N actions, batched and priority-ordered. Replaces the per-issue listing. |
| `--diff FILE` | Compare current state against a previous `--json` snapshot. Shows per-severity and per-rule deltas. |
| `--report` | Write `wiki/dm/review-queue.md` (DM-facing decisions queue). |
| `--summary` | Print only the count line. |
| `--json` | Machine-readable output with `summary`, `by_rule`, `fixed`, and `issues`. |
| `--min-severity` | Filter: `error`, `warning`, or `quality` (default: show all). |

### Severities

- **error** — breaks the vault: broken wikilink, naming violation, invalid value,
  missing/unparseable frontmatter. Fix first.
- **warning** — standards drift: missing required field, type/path mismatch,
  relationships in frontmatter, lifecycle-folder mismatch, lore consistency,
  tag issues (deprecated, alias, over-limit).
- **quality** — nudge: bare wikilink, orphan, deadend, stale summary, tag
  variant, unknown tag, singleton property.

---

## What `--fix` does (expanded in v3)

Everything `--fix` does is file-local, idempotent, and body-preserving:

| Fix | What happens |
|---|---|
| Missing required fields | Added with path-inferred defaults |
| Junk fields (`title`, `cssclasses`) | Stripped |
| Null-valued fields | Stripped |
| `sources: ["Unknown"]` | Replaced with `sources: []` |
| Empty `aliases: []` | Stripped |
| Empty `relationships: []` | Stripped |
| Boolean coercion | String `"true"`/`"false"` -> real booleans |
| Block-style lists | `tags`/`sources`/`aliases` rendered as `- item` |
| Field ordering | Canonical order enforced |
| **Status-drift** | Synonyms replaced: `deceased` -> `dead`, `open` -> `active` |
| **Lifecycle-folder sync** | Situations: lifecycle set to match folder (active/dormant/resolved) |

### What `--fix-tags` adds

| Fix | What happens |
|---|---|
| **Tag aliases** | Known aliases replaced with canonical form (e.g. `maw` -> `drowned-maw`) |
| **Deprecated-fm tags** | Tags duplicating frontmatter fields removed (e.g. `npc`, `faction`, `active`) |
| **Deprecated-system tags** | System/process tags removed (e.g. `lint`, `review`, `current-state`) |
| **Deduplication** | Duplicate tags (including post-alias-resolution duplicates) removed |

Tags requiring judgment (deprecated-entity, deprecated-source, unknown) are
left for the report — they need the agent to read the file.

---

## Working the report

Fix in this order; commit per logical batch using the conventions in
`.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md`.

Use `--top 10` for the priority-ordered view — it batches identical issues and
shows the highest-leverage actions first. Otherwise, errors first, then warnings,
then quality nudges. Each report line ends with a concrete suggested action.

For the per-category walkthrough — what each check means, how to resolve it, and
the right commit message — see [references/report-handling.md](references/report-handling.md).

---

## Incremental linting

For quick checks during a session (e.g., after ingest or a batch of edits), use
`--since` to lint only what changed:

```bash
# Lint files changed in the last 5 commits.
sea lint --since HEAD~5

# Lint files changed since yesterday.
sea lint --since "1 day ago"

# Fix + lint only what changed since a specific commit.
sea lint --fix --fix-tags --since abc1234
```

This makes lint cheap enough to run after every batch of changes. Cross-file
checks (orphans, deadends, broken wikilinks) still scan the full vault for
accuracy — only the per-file checks and fix pass are scoped.

---

## Measuring improvement

The lint system supports a measure -> fix -> verify loop for tracking vault
health over time.

### Save a baseline

```bash
sea lint --json > .claude/lint-baseline.json
```

### Fix issues, then diff

```bash
sea lint --fix --fix-tags
# ... work the report ...
sea lint --diff .claude/lint-baseline.json
```

The diff shows per-severity and per-rule changes: what improved, what
regressed, and any new files with issues.

### Health snapshots

`sea health` captures the full lint breakdown (per-rule counts) alongside
file counts, token usage, and infrastructure metrics:

```bash
sea health --save --label "post-lint-cleanup"
sea health --diff    # compare last two saved
sea health --history  # trend table
```

The continuous-self-improvement skill uses these snapshots for its
MEASURE -> FIX -> VERIFY loop. The per-rule breakdown makes it possible to
track which lint categories are improving and which are stagnating.

---

## Where flagged decisions live

- **`wiki/dm/review-queue.md`** — written by `--report`, committed, regenerated
  each run. Leads with *decisions needed*, summarizes the mechanical backlog.
  Shrinks as you resolve files — never hand-edit it.
- **`wiki/discrepancy-log.md`** — genuine lore contradictions and ambiguous
  entity identity. Durable judgment calls — append per the escalation protocol.

---

## Manual lore consistency review

The linter catches structural lore drift but cannot read prose for meaning or
reason about time. After working the automated report, do a manual pass over
files the linter flagged or that you touched during fixes. Temporal consistency
is the highest-value part of this pass.

Check: contradicted facts, session-number accuracy, in-world day sequencing,
location-time plausibility, "current state" decay, causal ordering, concurrent
timelines, hot.md coherence, entity identity overlap.

For the full procedure — drift patterns, what each temporal check looks like,
and what NOT to do — see [references/manual-lore-review.md](references/manual-lore-review.md).

---

## LLM-wiki file standards

Every file is optimized for two audiences: Obsidian and Claude Code. The linter
handles mechanical enforcement; the agent handles judgment calls.

For standards detail (frontmatter ordering, block-style lists, token efficiency,
agent-driven fixes) see [references/file-standards.md](references/file-standards.md).

---

## Self-improvement workflow

For scheduled/autonomous runs that improve vault quality without human
intervention, this sequence maximizes leverage:

```bash
# 1. Save baseline.
sea lint --json > /tmp/lint-before.json

# 2. Auto-fix everything safe.
sea lint --fix --fix-tags

# 3. See what's left, prioritized.
sea lint --top 10

# 4. Work the top items (agent judgment).

# 5. Measure improvement.
sea lint --diff /tmp/lint-before.json

# 6. Save snapshot for trend tracking.
sea health --save --label "lint-session"
```

The `continuous-self-improvement` skill wraps this in a formal MEASURE -> FIX ->
VERIFY loop with enforcement guarantees. This lint skill provides the tooling;
that skill provides the discipline.

---

## Reference Files

| File | Load when |
|---|---|
| [references/report-handling.md](references/report-handling.md) | Working the report: per-category meaning, resolution, and commit message |
| [references/manual-lore-review.md](references/manual-lore-review.md) | Doing the manual lore/temporal-consistency pass |
| [references/file-standards.md](references/file-standards.md) | Writing/editing files to the dual-audience standard |

---

## When the rules are wrong, not the files

The linter encodes conventions in three places: path->type/subtype tables in
`packages/lib/src/path-inference.ts`, value vocabularies in
`wiki-frontmatter.schema.json`, and required-fields-by-type in
`packages/lib/src/path-inference.ts`. When a *whole category* of files
trips the same check, the rules may have fallen behind reality. Don't mass-edit
files to satisfy a stale rule, and don't silently relax the rule — surface it
to the DM with both options.

---

## Relationship to other skills

- **ttrpg-llm-wiki-init** — session-start health; delegates full audit to this
  tool. Runs `--summary` on every session start.
- **continuous-self-improvement** — wraps lint + health snapshots in a measured
  fix loop. This skill provides tooling; that skill provides discipline.
- **ttrpg-writing** — for prose quality when weaving relationships into body.
- **Write-time hooks** — `validate-frontmatter.sh` handles single-file completion
  on every save; this skill is the bulk/standalone counterpart.

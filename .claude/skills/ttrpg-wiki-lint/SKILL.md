---
name: ttrpg-wiki-lint
metadata:
  version: "2.0"
description: >
  Lint the Shattered Sea wiki and fix what's safe to fix. Checks vault health:
  frontmatter standardization, broken wikilinks, orphans, deadends, lore
  consistency (dead entity refs, parent-location gaps, narrative-island
  mismatches, status drift), temporal consistency (timeline contradictions,
  impossible travel, stale "current state" claims, session-number/day-sequence
  errors), tag hygiene, singleton properties, and markdown formatting.
  Auto-detects Obsidian CLI and markdownlint-cli2. Trigger on: "lint the wiki",
  "check wiki health", "fix the frontmatter", "find broken links/orphans/
  deadends", "lore consistency", "check consistency", "status drift", "tag
  hygiene", "audit the wiki", "clean up the vault", "check markdown formatting",
  "timeline issues", "temporal consistency", "check the timeline", "stale state",
  "session number wrong".
---

# TTRPG Wiki Lint — Shattered Sea

One script does the heavy lifting: `.claude/scripts/wiki_lint.py`. It splits every
problem into two piles —

- **Safe, file-local, reversible → it fixes automatically** (`--fix`): completing and
  standardizing frontmatter. These never invent canon and never touch another file,
  so they're safe to run in bulk and are idempotent (a second run changes nothing).
- **Needs judgment or a cross-file change → it reports** (never silently changed):
  broken wikilinks, off-convention filenames, orphans, deadends, invalid frontmatter
  values, stale stub summaries, tag variants, singleton properties, and relationships
  still living in frontmatter. Each line ends with a concrete suggested action.

The script auto-detects two external tools and uses them when available:

- **Obsidian CLI** (`--obsidian auto|on|off`) — when Obsidian is running, uses its
  metadata cache for broken-link detection (more accurate than regex — catches
  path-qualified and alias-resolved links) and deadend detection. Falls back to
  regex-based checks when Obsidian is closed.
- **markdownlint-cli2** (`--markdown auto|on|off`) — when installed, checks markdown
  formatting (heading spacing, list spacing, trailing whitespace). Config lives at
  `.markdownlint-cli2.jsonc`, tuned for Obsidian-flavored markdown.

---

## The loop

```
1. Lint            python3 .claude/scripts/wiki_lint.py
2. Auto-fix safe   python3 .claude/scripts/wiki_lint.py --fix      (then commit)
3. Re-lint         what remains needs you
4. Work the report by category (below), fixing + committing as you go
5. Manual lore     check prose-level consistency on files you touched (see below)
6. Stop            when only DM-judgment items remain — surface those, don't guess
```

Don't read files one by one to assess health — run the script. It's the fast path
and it won't miss things you would. The manual lore pass (step 5) is for what the
script *can't* catch: prose contradictions, timeline drift, and entity identity.

## Where flagged decisions live

- **`wiki/dm/review-queue.md`** — written by `--report`, committed, regenerated each run.
  It leads with *decisions needed* (the judgment items) and summarizes the mechanical/content
  backlog. It shrinks as you resolve the underlying files — never hand-edit it.
- **`wiki/discrepancy-log.md`** — for genuine lore contradictions and ambiguous entity
  identity. These are durable judgment calls — record them here per the escalation protocol in `.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md`,
  leaving both traces visible, and escalate to the DM.

---

## Running it

```bash
# Report only — whole vault (auto-detects Obsidian CLI and markdownlint).
python3 .claude/scripts/wiki_lint.py

# Standardize frontmatter in place (safe, idempotent), then report what's left.
python3 .claude/scripts/wiki_lint.py --fix

# Scope to a file or directory — for both reporting and --fix.
python3 .claude/scripts/wiki_lint.py --fix wiki/entities/characters/npcs/

# Just the counts.
python3 .claude/scripts/wiki_lint.py --summary

# Only errors (the things that actually break navigation).
python3 .claude/scripts/wiki_lint.py --min-severity error

# Force Obsidian CLI on/off regardless of auto-detection.
python3 .claude/scripts/wiki_lint.py --obsidian on
python3 .claude/scripts/wiki_lint.py --obsidian off

# Force markdownlint on/off.
python3 .claude/scripts/wiki_lint.py --markdown off

# Persist flagged decisions where the DM will see them across sessions.
python3 .claude/scripts/wiki_lint.py --report      # writes wiki/dm/review-queue.md

# Machine-readable, e.g. to count or filter.
python3 .claude/scripts/wiki_lint.py --json
```

Exit code is `1` when any **error** exists, `0` otherwise — so it can gate a commit.
Warnings and quality notes don't fail.

### Severities

- **error** — breaks the vault's contract: broken wikilink, off-convention filename,
  invalid frontmatter value, missing frontmatter block. Fix these first.
- **warning** — a standards drift to resolve: missing required field, type/path
  mismatch, a relationship still in frontmatter, a situation in the wrong lifecycle
  folder.
- **quality** — a nudge, not a defect: bare (un-aliased) wikilink, orphan page,
  deadend, stub summary, tag variant, singleton property, markdown formatting.
  Improve opportunistically.

---

## What `--fix` does (and only this)

It standardizes the frontmatter block and nothing else — the body is preserved
byte-for-byte. **Tag content is never auto-fixed** — choosing the right canonical
tags requires reading the file and understanding what it's about. Tag issues always
appear in the report for the agent to resolve manually. Specifically: adds any missing required field with a path-inferred
default, drops an empty `relationships: []`, coerces `publish`/`portable` to real
booleans, renders `tags`/`sources`/`aliases` in block style (Obsidian's preferred
list format), and reorders fields into canonical order. Run it freely; it converges
in one pass.

Because `--fix` writes files directly (not through the editor), the frontmatter hook
doesn't re-fire on it — that's fine, the script applies the same completion the hook
would. After a bulk `--fix`, commit: `curation: frontmatter standardized — {N} files`.

---

## Working the report

Fix in this order; commit per logical batch using the conventions in
`.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md` (`fix: {type} — {file} — {what}`).

Errors first (`broken-wikilink`, `naming-convention`, `invalid-value`), then warnings
(`missing-required-field`, `relationships-in-frontmatter`, the lore-consistency family,
`type-path-mismatch`, the tag family), then quality nudges (`orphan`, `deadend`,
`bare-wikilink`, `summary-stale`, `singleton-property`, `md-*`). Each report line ends
with a concrete suggested action.

For the per-category walkthrough — what each check means, how to resolve it, and the
right commit message — see [references/report-handling.md](references/report-handling.md).

---

## Manual lore consistency review

The script catches structural lore drift (dead-entity-ref, island-situation-mismatch,
status-drift, parent-gap) but cannot read prose for meaning — and it cannot reason
about time. After working the automated report, do a manual pass over files the
script flagged or that you touched during fixes. Temporal consistency (when things
happened, whether movements and durations are physically possible, whether "current
state" claims have decayed) is the highest-value part of this pass. This is where
an LLM-wiki agent earns its keep — the compounding knowledge base is only as
reliable as its internal coherence.

In brief, check: contradicted facts across files; temporal consistency
(session-number accuracy, in-world day sequencing, location-time plausibility,
"current state" decay, causal ordering, concurrent timelines); `hot.md` coherence;
and entity identity overlap. When two files disagree and the session notes don't
clarify, escalate — append to `wiki/discrepancy-log.md`, don't pick a side. Do a
manual pass after ingest, after working the automated report, after a world-update,
or when the DM asks.

For the full procedure — drift patterns, what each temporal check looks like, how to
trace a claim to its source, and what NOT to do — see
[references/manual-lore-review.md](references/manual-lore-review.md).

---

## LLM-wiki file standards

Every file in this vault is optimized for two audiences: Obsidian (visual browsing)
and Claude Code (agent context). Linting is the process of transforming files safely
toward that dual-purpose ideal. The script handles the mechanical enforcement; the
agent handles judgment calls the script can't make.

The standards the `--fix` pass enforces and the judgment calls it can't — frontmatter
field ordering, block-style lists, junk-field stripping, concrete summaries, markdown
conventions, token-efficiency / context-engineering rules (`token_profile`, `audience`,
body density, cross-reference over duplication), and agent-driven fixes (vague
summaries, redundant body content, orphaned callouts, dead content blocks) — are
detailed in [references/file-standards.md](references/file-standards.md).

---

## Reference Files

| File | Load when |
|---|---|
| [references/report-handling.md](references/report-handling.md) | Working the report: per-category meaning, resolution, and commit message for each lint check |
| [references/manual-lore-review.md](references/manual-lore-review.md) | Doing the manual lore/temporal-consistency pass the script can't do |
| [references/file-standards.md](references/file-standards.md) | Writing/editing files to the LLM-wiki dual-audience standard, or judging non-mechanical quality |

---

## When the rules are wrong, not the files

The linter encodes the vault's conventions in three places: the path→type/subtype
tables in `wiki_common.py`, the value vocabularies in `wiki-frontmatter.schema.json`,
and required-fields-by-type in `wiki_common.py`. When a *whole category* of files
trips the same check, the rules may have fallen behind reality rather than the files
being wrong. Don't mass-edit files to satisfy a stale rule, and don't silently relax
the rule either — **surface it to the DM**: describe the pattern, name both options,
and let them decide. That's a structural decision, not a lint fix.

Genuine lore contradictions and ambiguous entity identity always escalate to the DM
per the escalation protocol — append to `wiki/discrepancy-log.md`, don't auto-resolve.

---

## Relationship to other skills

`ttrpg-llm-wiki-init` owns session-start health and routing; its **Full Audit Mode
delegates the actual checking to this script** instead of hand-walking files. The
write-time frontmatter hook (`fix_frontmatter.py`) handles single-file completion on
every save; this skill is the bulk/standalone counterpart and goes further
(validation, links, orphans, deadends, lore consistency, tag hygiene, token
optimization, markdown formatting). For prose quality while weaving relationships,
defer to `ttrpg-writing`.

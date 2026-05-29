---
name: ttrpg-wiki-lint
version: "1.0"
description: >
  Lint the Shattered Sea wiki and fix what's safe to fix. Run this whenever you
  need to check vault health, standardize frontmatter (one file or in bulk), find
  broken wikilinks or orphans, or migrate relationships out of frontmatter into the
  body. This is the engine behind a full audit — ttrpg-llm-wiki-init's Full Audit
  Mode routes here. Trigger on: "lint the wiki", "check wiki health", "fix the
  frontmatter", "standardize frontmatter", "find broken links", "find orphans",
  "what's wrong with the wiki", "clean up the vault", "audit the wiki", "any broken
  wikilinks", "validate frontmatter", "move relationships into the body". One Python
  pass auto-fixes the safe, file-local frontmatter problems and reports everything
  that needs judgment, each with a concrete next action. Prefer it over hand-checking
  files token by token — the script is faster, deterministic, and idempotent.
---

# TTRPG Wiki Lint — Shattered Sea

One script does the heavy lifting: `.claude/scripts/wiki_lint.py`. It splits every
problem into two piles —

- **Safe, file-local, reversible → it fixes automatically** (`--fix`): completing and
  standardizing frontmatter. These never invent canon and never touch another file,
  so they're safe to run in bulk and are idempotent (a second run changes nothing).
- **Needs judgment or a cross-file change → it reports** (never silently changed):
  broken wikilinks, off-convention filenames, orphans, invalid frontmatter values,
  stale stub summaries, and relationships still living in frontmatter. Each line ends
  with a concrete suggested action so you can act and commit.

This split is the whole point: moving a file, renaming it, creating a stub, or
weaving a relationship into prose all rewrite the graph or the content, so they're
*your* call, not the script's.

It builds on the same `wiki_common.py` primitives as the other scripts, validates
frontmatter values against the declarative `wiki-frontmatter.schema.json`, and uses
`ruamel.yaml` to round-trip frontmatter without mangling it. You don't maintain any
of that by hand.

---

## The loop

```
1. Lint            python3 .claude/scripts/wiki_lint.py
2. Auto-fix safe   python3 .claude/scripts/wiki_lint.py --fix      (then commit)
3. Re-lint         what remains needs you
4. Work the report by category (below), fixing + committing as you go
5. Stop            when only DM-judgment items remain — surface those, don't guess
```

Don't read files one by one to assess health — run the script. It's the fast path
and it won't miss things you would.

## Where flagged decisions live

So nothing gets forgotten, persistence has two homes:

- **`wiki/dm/review-queue.md`** — written by `--report`, committed, regenerated each run.
  It leads with *decisions needed* (the judgment items) and summarizes the mechanical/content
  backlog. It shrinks as you resolve the underlying files — never hand-edit it. `ttrpg-llm-wiki-init`
  surfaces its open-decision count at session start, so the DM sees it every session.
- **`wiki/discrepancy-log.md`** — for genuine lore contradictions and ambiguous entity
  identity (e.g. "is the *creature* page the same entity as the *npc* page?"). These are
  durable judgment calls, not auto-detectable drift — record them here per `doctrine.md`,
  leaving both traces visible, and escalate to the DM. Don't auto-resolve identity.

---

## Running it

```bash
# Report only — whole vault. Summary to stderr, issues grouped on stdout.
python3 .claude/scripts/wiki_lint.py

# Standardize frontmatter in place (safe, idempotent), then report what's left.
python3 .claude/scripts/wiki_lint.py --fix

# Scope to a file or directory — for both reporting and --fix.
python3 .claude/scripts/wiki_lint.py --fix wiki/entities/characters/npcs/

# Just the counts.
python3 .claude/scripts/wiki_lint.py --summary

# Only errors (the things that actually break navigation).
python3 .claude/scripts/wiki_lint.py --min-severity error

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
- **quality** — a nudge, not a defect: bare (un-aliased) wikilink, orphan page, stub
  summary. Improve opportunistically.

---

## What `--fix` does (and only this)

It standardizes the frontmatter block and nothing else — the body is preserved
byte-for-byte. Specifically: adds any missing required field with a path-inferred
default, drops an empty `relationships: []`, coerces `publish`/`portable` to real
booleans, renders `tags`/`sources`/`aliases` in flow style (`[a, b]`), and reorders
fields into canonical order. Run it freely; it converges in one pass.

Because `--fix` writes files directly (not through the editor), the frontmatter hook
doesn't re-fire on it — that's fine, the script applies the same completion the hook
would. After a bulk `--fix`, commit: `curation: frontmatter standardized — {N} files`.

---

## Working the report

Fix in this order; commit per logical batch using the conventions in
`wiki/system/doctrine.md` (`fix: {type} — {file} — {what}`).

### broken-wikilink (error)
A `[[target]]` resolves to no page (case-insensitive; image embeds and example links
in code are already excluded, so every hit is real). Per `doctrine.md`, the standard
correction is to **create a stub** at the right path with `status: stub` and a
`summary: "Stub — referenced in [[source]]. No page yet."`, then let the hook
complete the frontmatter. If instead the link is just a typo or wrong slug, fix the
link. Don't leave it dangling.

### naming-convention (error)
Filename isn't kebab-case. Rename to kebab-case **and update inbound wikilinks**, then
commit. (`git mv` keeps history.)

### invalid-value (error)
A frontmatter value is outside its allowed vocabulary (e.g. `lifecycle: island` when
the schema allows only `dormant`/`active`/`resolved`). Either correct the value or —
if the vault has genuinely outgrown the vocabulary — that's a schema question for the
DM (see *When the rules are wrong*).

### missing-required-field (warning)
Almost always cleared by `--fix`. If it persists, the field's type-inference is off —
check the file is at the right path.

### relationships-in-frontmatter (warning) — the migration
Relationships belong in the **body prose as wikilinks**, not in a frontmatter field.
Each report line lists every relationship, its note, and whether the target is
**already linked in the body**:

- **target already "in body"** — the link exists; just fold the note into a nearby
  sentence so the relationship reads naturally, then delete that entry.
- **target "NOT in body"** — the relationship isn't reflected in the prose at all;
  write a sentence that introduces it with an aliased wikilink, carrying the note's
  substance.

Weaving prose is a writing task — load `ttrpg-writing` for voice. Don't mechanically
dump `Relationships:` as a bullet list; work each one into the lore/DM text where it
belongs. Once every entry for a file is woven in, **delete the `relationships:` field
entirely**. The hook and linter no longer add or expect it, so it stays gone. Commit:
`curation: {file} — relationships woven into body`.

Empty `relationships: []` fields carry nothing to migrate and are stripped by `--fix`.

### type-path-mismatch (warning)
`type:` disagrees with the file's location. Usually the value is wrong — set it to
match the path. But a cluster of mismatches (e.g. a whole `situations/islands/`
subtree typed `island`) means the directory structure has evolved past what
`wiki_common.py`'s inference tables know — see below.

### orphan (quality)
No other page links here (links from the generated `index.md` don't count; links from
hand-curated `hot.md` do). Link it from a natural parent. Some bestiary stat blocks
and minor NPCs are legitimately standalone — use judgment; this is a nudge.

### bare-wikilink / summary-stale (quality)
Add a display alias (`[[slug|Name]]`); write a concrete summary. Opportunistic.

---

## When the rules are wrong, not the files

The linter encodes the vault's conventions in three places: the path→type/subtype
tables in `wiki_common.py`, the value vocabularies in `wiki-frontmatter.schema.json`,
and required-fields-by-type in `wiki_common.py`. When a *whole category* of files
trips the same check, the rules may have fallen behind reality rather than the files
being wrong (the `situations/islands/` subtree typed `island` with `lifecycle: island`
is the live example). Don't mass-edit files to satisfy a stale rule, and don't
silently relax the rule either — **surface it to the DM**: describe the pattern, name
both options (teach the tables/schema the new category, or the files are genuinely
misplaced), and let them decide. That's a structural decision, not a lint fix.

Genuine lore contradictions and ambiguous entity identity always escalate to the DM
per `doctrine.md` — append to `wiki/discrepancy-log.md`, don't auto-resolve.

---

## Relationship to other skills

`ttrpg-llm-wiki-init` owns session-start health and routing; its **Full Audit Mode
delegates the actual checking to this script** instead of hand-walking files. The
write-time frontmatter hook (`fix_frontmatter.py`) handles single-file completion on
every save; this skill is the bulk/standalone counterpart and goes further
(validation, links, orphans, migration). For prose quality while weaving
relationships, defer to `ttrpg-writing`.

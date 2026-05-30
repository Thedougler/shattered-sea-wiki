---
name: ttrpg-wiki-lint
version: "2.0"
description: >
  Lint the Shattered Sea wiki and fix what's safe to fix. Run this whenever you
  need to check vault health, standardize frontmatter (one file or in bulk), find
  broken wikilinks or orphans, find deadend pages, check tag hygiene, detect
  singleton properties, or migrate relationships out of frontmatter into the
  body. Auto-detects Obsidian CLI for deeper cross-file checks and
  markdownlint-cli2 for markdown formatting. This is the engine behind a full
  audit — ttrpg-llm-wiki-init's Full Audit Mode routes here. Trigger on: "lint
  the wiki", "check wiki health", "fix the frontmatter", "standardize
  frontmatter", "find broken links", "find orphans", "find deadends", "tag
  hygiene", "what's wrong with the wiki", "clean up the vault", "audit the
  wiki", "any broken wikilinks", "validate frontmatter", "move relationships
  into the body", "check markdown formatting".
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
5. Stop            when only DM-judgment items remain — surface those, don't guess
```

Don't read files one by one to assess health — run the script. It's the fast path
and it won't miss things you would.

## Where flagged decisions live

- **`wiki/dm/review-queue.md`** — written by `--report`, committed, regenerated each run.
  It leads with *decisions needed* (the judgment items) and summarizes the mechanical/content
  backlog. It shrinks as you resolve the underlying files — never hand-edit it.
- **`wiki/discrepancy-log.md`** — for genuine lore contradictions and ambiguous entity
  identity. These are durable judgment calls — record them here per `doctrine.md`,
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
A `[[target]]` resolves to no page. When Obsidian CLI is active, this uses Obsidian's
live metadata cache — it catches path-qualified links (`[[wiki/situations/...]]`) and
alias-resolved links that regex-based checking misses. Per `doctrine.md`, the standard
correction is to **create a stub** at the right path with `status: stub` and a
`summary: "Stub — referenced in [[source]]. No page yet."`, then let the hook
complete the frontmatter. If the link is a typo or wrong slug, fix it instead.

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
entirely**. Commit: `curation: {file} — relationships woven into body`.

### type-path-mismatch (warning)
`type:` disagrees with the file's location. Usually the value is wrong — set it to
match the path. But a cluster of mismatches means the directory structure has evolved
past what `wiki_common.py`'s inference tables know — see below.

### deadend (quality)
No outgoing wikilinks. The page is a terminal node in the graph — it doesn't link to
anything. Add wikilinks to related pages where natural. Some stat blocks and minor
entries are legitimately standalone.

### orphan (quality)
No other page links here (links from the generated `index.md` don't count; links from
hand-curated `hot.md` do). Link it from a natural parent.

### tag-variant (quality)
A tag looks like a plural/singular variant of another tag (e.g. `#ship` vs `#ships`).
The less-used variant is flagged. Consolidate to the more common form.

### singleton-property (quality)
A frontmatter property name appears in only one file and isn't in the schema. Likely
a typo or a field that should be consolidated. Verify it's intentional, or fix it.

### bare-wikilink / summary-stale (quality)
Add a display alias (`[[slug|Name]]`); write a concrete summary. Opportunistic.

### md-* (quality, markdownlint)
Markdown formatting issues detected by markdownlint-cli2. Common ones:
`md-blanks-around-headings`, `md-blanks-around-lists`, `md-no-trailing-spaces`.
Config at `.markdownlint-cli2.jsonc` — noisy rules (line-length, table formatting,
multi-H1) are already disabled.

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
per `doctrine.md` — append to `wiki/discrepancy-log.md`, don't auto-resolve.

---

## Relationship to other skills

`ttrpg-llm-wiki-init` owns session-start health and routing; its **Full Audit Mode
delegates the actual checking to this script** instead of hand-walking files. The
write-time frontmatter hook (`fix_frontmatter.py`) handles single-file completion on
every save; this skill is the bulk/standalone counterpart and goes further
(validation, links, orphans, deadends, tag hygiene, markdown formatting). For prose
quality while weaving relationships, defer to `ttrpg-writing`.

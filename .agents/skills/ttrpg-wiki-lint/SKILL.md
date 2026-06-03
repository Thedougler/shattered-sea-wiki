---
name: ttrpg-wiki-lint
version: "2.0"
description: >
  Lint the Shattered Sea wiki and fix what's safe to fix. Run this whenever you
  need to check vault health, standardize frontmatter, find broken wikilinks or
  orphans, find deadend pages, check lore consistency (dead entity refs, parent
  location gaps, narrative island mismatches, status drift), check temporal
  consistency (timeline contradictions, impossible travel, stale "current state"
  claims, session-number misattributions, in-world day sequencing errors), check
  tag hygiene, detect singleton properties, or run markdown formatting checks.
  Auto-detects Obsidian CLI for deeper cross-file checks and markdownlint-cli2
  for formatting. Trigger on: "lint the wiki", "check wiki health", "fix the
  frontmatter", "find broken links", "find orphans", "find deadends", "lore
  consistency", "check consistency", "dead NPC still captaining", "status drift",
  "tag hygiene", "what's wrong with the wiki", "clean up the vault", "audit the
  wiki", "check markdown formatting", "timeline issues", "temporal consistency",
  "when did this happen", "check the timeline", "is this possible given the
  timeline", "stale state", "session number wrong".
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

### broken-wikilink (error)
A `[[target]]` resolves to no page. When Obsidian CLI is active, this uses Obsidian's
live metadata cache — it catches path-qualified links (`[[wiki/situations/...]]`) and
alias-resolved links that regex-based checking misses. Per `.claude/skills/ttrpg-llm-wiki-init/references/wikilink-standards.md`, the standard
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

### dead-entity-ref (warning) — lore consistency
A frontmatter cross-reference field (`captain`, `current_holder`, `owner`) points to
an entity whose status is `dead`, `deceased`, `destroyed`, or `presumed_dead`. The
ship/item page still claims a dead entity fills that role. Either update the field
(new captain, no holder) or mark the parent file's status to reflect the loss.

### island-situation-mismatch (warning) — lore consistency
A narrative island's `contains_situations` lists a situation whose `narrative_island`
field doesn't match (or is unset). Set the situation's `narrative_island` to match
the island that claims it, or remove it from `contains_situations` if the mapping
is wrong.

### status-drift (warning) — lore consistency
A status value has a near-synonym in use elsewhere (`deceased` vs `dead`, `open` vs
`active`). Standardize to the canonical form for consistency. The linter flags the
less-common variant.

### parent-gap (quality) — lore consistency
A place's `parent_location` field points to a parent page, but the parent's body
prose doesn't mention this child. Add a wikilink to the child in the parent page.

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

### tag-deprecated (warning)

A tag in the deprecated list from `wiki/system/taxonomy.md`. Three sub-types, identified in the detail:

- **Frontmatter duplicate** — the tag restates what `type`, `subtype`, `status`, or `audience` already says. Remove it.
- **Entity name** — the tag names an NPC, place, ship, or PC. Add a wikilink to that entity in the body, then remove the tag.
- **Source citation / system tag** — move to `sources:` field or remove.

**Fixing:** Read the file first. Once you know what the page is actually about, choose up to 5 canonical replacements from `wiki/system/taxonomy.md`. Don't just delete the old tag — the page may now have zero tags and deserve real ones.

### tag-alias (warning)

A tag is a known alias for a canonical form (e.g. `maw` → `drowned-maw`, `prep` → `dm-prep`). The fix message names the canonical replacement.

**Fixing:** Read the file. Replace the alias with its canonical form — but also check whether the canonical tag actually applies to this page's content. An alias might have been a lazy tag for something not really covered by the canonical concept.

### tag-unknown (quality)

A tag that isn't in the controlled vocabulary and isn't a known alias or deprecated tag. These are ad-hoc labels accumulated before the taxonomy existed.

**Fixing:** Read the file. Either:
1. Replace with the closest canonical tag from `wiki/system/taxonomy.md` if one fits.
2. If the page doesn't need the tag at all, remove it.
3. If the tag genuinely deserves to be canonical (appears or is needed on 5+ files across 3+ entity types), propose adding it to the taxonomy before applying it.

Never add an unknown tag to more files — only canonicalize or remove.

### tag-over-limit (warning)

More than 5 content tags (visibility tags don't count toward the limit).

**Fixing:** Read the file. Keep the 3–5 tags that are most cross-cutting and useful for DM prep. Prefer faction and theme/domain tags over workflow tags when space is tight. The limit is strict — trim to ≤5.

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

## Manual lore consistency review

The script catches structural lore drift (dead-entity-ref, island-situation-mismatch,
status-drift, parent-gap) but cannot read prose for meaning — and it cannot reason
about time. After working the automated report, do a manual pass over files the
script flagged or that you touched during fixes. Temporal consistency (when things
happened, whether movements and durations are physically possible, whether "current
state" claims have decayed) is the highest-value part of this pass. This is where
an LLM-wiki agent earns its keep — the compounding knowledge base is only as
reliable as its internal coherence.

### What to check

**Contradicted facts across files.** When a file states a fact about another entity
(location, allegiance, status, event), open the target entity's page and verify the
claim matches. Common drift patterns:

- An NPC page says they're in Calveno, but a situation page places them at sea
- A session recap says an event happened during Session 02, but the NPC's page
  describes it as Session 03
- A faction page says NPC X is a member, but NPC X's page says they left
- A place's body says it's governed by faction A, but faction A's page doesn't
  list that place
- An item page says it was found in location X, but the session where it was
  found places the party somewhere else

When you find a contradiction: check session notes (the primary source) to determine
which version is correct. Fix the wrong one. If both could be right (ambiguous source
material), append to `wiki/discrepancy-log.md` — don't guess.

**Temporal consistency.** This is judgment work that no script can do — it requires
understanding when things happened in-world, what was physically possible given
distances and durations, and whether entity pages reflect the world as it stands
after the most recent session.

Session notes are the authoritative timeline. The in-world clock is layered:
sessions map to stretches of in-world time, and within a session the day structure
(e.g. Session 04's Day 1–5 files) establishes what happens when. Reconstructing
the timeline for a specific entity or event means reading the session files that
touch it and building a sequence: where were they, what happened, how much time
passed.

**What to check:**

*Session-number accuracy.* When a page cites "Session 02" or "in Session 03,"
verify the event actually occurred in that session. Open the session recap or
scene file and confirm. Common drift: events get attributed to the session where
they were *discussed* rather than the session where they *happened*.

*In-world day sequencing.* When session files use day numbering (Day 1, Day 2),
entity and situation pages that reference those events should be consistent with
the day they occurred. A ship that docks on Day 1 cannot have a completed 5-day
refit on Day 3. An NPC who departs at dawn on Day 2 should not appear in a scene
set on Day 1 evening as already gone.

*Location-time plausibility.* If an NPC is established as being in location A
during a specific session or day, they cannot simultaneously be in location B
unless travel is plausible in the elapsed time. This applies to the party too —
check that "the party did X in Calveno" claims don't conflict with travel
timelines. The campaign is nautical; sea travel takes days, not hours.

*"Current state" decay.* Entity pages, situation files, and hot.md all carry
claims about the present: "currently docked at La Vasca," "Grigori is aboard,"
"the favor has not been named." Each of these has a session-of-origin. When a
later session changes the state, every page that cached the old state needs
updating. The most dangerous form is a callout or info box labeled
"post-Session N" — these read as authoritative but rot silently.

*Causal ordering.* Some events depend on others: Nona calling off the attacks
requires Perrin to have met her first. The sending stone can't be used before
it's given. When a page describes consequences, verify the cause has already
occurred in the timeline. This catches cases where world-building pages
(written ahead of play) describe outcomes that haven't happened yet in the
session record.

*Concurrent timeline plausibility.* Multiple threads run simultaneously in
Calveno (ship repair, festival days, raid prep, NPC movements). When two
threads reference the same in-world day, their claims must be compatible.
The raid prep timeline in one file and the festival schedule in another should
agree on which day is which.

**How to do it:** Don't try to audit the entire timeline at once. Start from
the files the automated lint flagged or the files you touched during fixes.
For each temporal claim, trace it back to its session source. Use
`qmd query` or `obsidian search` to find cross-references efficiently. When
you find a mismatch, check the session recap (primary source) to determine
which version is correct. Fix the wrong one. If both could be right, or if
the timeline is genuinely ambiguous in the source material, append to
`wiki/discrepancy-log.md`.

**hot.md coherence.** After any batch of fixes, scan `wiki/hot.md` for claims that
conflict with what you just corrected. hot.md is the most-read file and the most
likely to go stale. If it references a dead NPC as active, a resolved situation as
live, or a ship's captain who's been killed — fix it.

**Entity identity.** Two pages may describe the same entity under different names or
from different angles (e.g. `leviathan.md` creature vs NPC — see
`wiki/discrepancy-log.md` for the live example). When you suspect identity overlap:

- Do NOT merge or resolve on your own
- Append to `wiki/discrepancy-log.md` with both file paths, what overlaps, and
  your recommendation
- Leave both pages intact until the DM decides

### When to do a manual pass

- **After ingest** — new source material is the #1 cause of lore drift. The ingest
  skill creates/updates entity pages from session notes, which may contradict existing
  content written from earlier sessions or world-building.
- **After working the automated report** — the files the script flagged are already
  open in your context. Scan their prose while you're there.
- **After a world-update** — faction clock advances and situation resolution can
  invalidate claims in entity pages.
- **When the DM asks** — "check consistency", "anything contradictory", "does this
  all hang together" all trigger this manual pass.

### What NOT to do

- Don't read every file in the vault looking for contradictions. Use the script output
  and `qmd query` / `obsidian search` to target files that reference each other.
- Don't invent lore to resolve a gap. If two files disagree and the session notes don't
  clarify, escalate — don't pick a side.
- Don't silently change established facts. If an NPC's allegiance needs updating because
  of session events, that's a legitimate correction. If two world-building files
  disagree about geography and neither has session backing, that's a discrepancy-log
  entry.

---

## LLM-wiki file standards

Every file in this vault is optimized for two audiences: Obsidian (visual browsing)
and Claude Code (agent context). Linting is the process of transforming files safely
toward that dual-purpose ideal. The script handles the mechanical enforcement; the
agent handles judgment calls the script can't make.

### Frontmatter standards

The `--fix` pass enforces these mechanically. When writing or editing manually,
follow the same conventions so `--fix` is a no-op:

**Field ordering.** Universal fields first in canonical order (`type`, `subtype`,
`campaign`, `status`, `audience`, `publish`, `summary`, `created`, `updated`, `tags`,
`sources`), then type-specific extras, then domain fields. The script reorders on
`--fix`.

**Block-style lists.** `tags`, `sources`, and `aliases` use block style per
Obsidian's preferred format:
```yaml
tags:
  - npc
  - shattered-sea
```
Not flow style (`tags: [npc, shattered-sea]`). The `--fix` script enforces this.
Running `--fix` will convert existing flow-style lists to block style.

**No junk fields.** These waste tokens on every Read and carry no signal:

| Field | Action |
|---|---|
| `title` | Strip — the H1 heading and the filename carry the title. 558 files have this; it's ~2k tokens of pure noise across the vault. |
| `cssclasses` | Strip — only matters to Obsidian's CSS renderer, invisible to the agent. 93 files (`wiki-monster`, `wiki-ship`). |
| `null` values (`field: null`) | Strip or set to a real default. 23 files have `narrative_island: null`. |
| `sources: [Unknown]` | Replace with `sources: []` — "Unknown" is not a source. |
| `aliases: []` | Strip empty alias lists — adds nothing. |

These are safe to remove in `--fix` bulk passes (the script currently handles
`relationships: []` stripping; the others are candidates for future `--fix` scope).
Until then, remove by hand when touching a file.

**Concrete summaries.** Every summary must state a fact the agent can use for
routing. "Stub — no summary yet." fails this. A summary like "Tavern in the Warren
district of Calveno, run by Nona" lets the agent decide whether to read the file
without opening it. Write summaries as if the agent is scanning 500+ of them in
an index.

### Markdown standards

**Aliased wikilinks.** Always alias: `[[bastian-crev|Bastian Crev]]`, not
`[[bastian-crev]]`. Bare links render as slugs in agent context — the alias is how
the entity name reaches the agent without it opening the target file.

**One H1 per file.** The H1 is the page title. Use H2+ for sections. (markdownlint
rule MD025 is disabled because some legacy files violate this, but new content should
comply.)

**Blank lines around headings and lists.** markdownlint enforces this (MD022, MD032).
Missing blank lines cause Obsidian to sometimes merge content into the heading or
misparse list items.

**No trailing whitespace.** Invisible bytes that inflate diffs and token counts.

**Image embeds are for Obsidian, not the agent.** `![[portrait.webp]]` renders
visually in Obsidian but is a dead token for the agent. Keep them for visual
reference but don't rely on them to convey information — the body text must stand
alone.

**Thematic breaks (`---`) in body.** Use sparingly between major sections. They're
three tokens each and 190 files have them. Not wrong, but don't add them reflexively.

### Token efficiency and context engineering

The vault exists so the agent can answer questions and generate content without
reading everything. Every file should be optimized for **selective loading**:

**Frontmatter is the routing layer.** The agent reads frontmatter (via the index,
via `qmd`, via direct file reads) to decide what to load fully. `summary`, `type`,
`status`, `tags`, and `audience` are the fields that drive routing. If these are
wrong or vague, the agent either loads the wrong files or misses the right ones.

**`token_profile`** (system files only) signals how aggressively a file should be
loaded:

| Value | Meaning |
|---|---|
| `always-read` | Load every session (hot.md, doctrine) |
| `quick-ref` | Load the summary; read fully only when task matches |
| `on-demand` | Read only when explicitly needed |
| `map` | Index/generated file — scan, don't read deeply |

**`audience`** gates what the agent surfaces to players:

| Value | Meaning |
|---|---|
| `dm` | DM-only content; never show to players |
| `players` | Safe to surface in player-facing contexts |
| `agent` | System/infrastructure; not campaign content |

**Body density.** Prefer concrete facts over atmospheric prose in DM-reference
pages. A 200-word page with 10 actionable facts is more useful to the agent than a
1000-word page with 2 facts buried in flavor. Save the prose for `read-aloud`
callouts and player-facing content. See `ttrpg-writing` for the two content modes.

**Cross-reference over duplication.** If fact X lives on Entity A's page, don't
restate it on Entity B's page — link to it. Duplication means two places to update
and two places that can drift. Use wikilinks and section embeds (`![[A#Section]]`).

### Agent-driven fixes (what the script can't catch)

When touching files during a lint pass, also check for these by judgment:

**Vague summaries.** The script flags `"Stub — no summary yet."` but can't judge
whether `"An NPC in the campaign"` is useful. It isn't. Rewrite to include the
entity's distinguishing fact: role, location, relationship to a PC, or reason
they matter.

**Redundant body content.** If the frontmatter already carries a field (`captain`,
`parent_location`, `species`) and the body restates the same fact in prose with no
additional context, the prose version wastes tokens. Either enrich the prose version
(add context the field can't carry) or cut it.

**Orphaned callouts.** A `> [!secret]` or `> [!mechanic]` callout whose content
has been revealed in play or superseded by later sessions. These should be converted
to plain text or removed. The script can't know what's been revealed — you can, by
checking session notes.

**Dead content blocks.** Sections like "## Hooks" or "## Rumors" that are empty or
contain only placeholder text like "TBD" or "None yet". Either populate them with
real content or remove the heading entirely. Empty sections waste tokens and mislead
the agent into thinking there's structure where there's none.

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

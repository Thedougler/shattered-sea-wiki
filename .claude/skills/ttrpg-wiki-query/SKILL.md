---
name: ttrpg-wiki-query
metadata:
  version: "1.0"
description: >
  The mandatory default method for finding anything in the Shattered Sea wiki. Use
  this ANY time you need in-world information — whether the user explicitly asks you
  to look something up, or you need context before answering, prepping, or writing.
  Invoke it BEFORE asserting, inventing, or assuming any campaign fact: NPCs,
  locations, ships, factions, creatures and stat blocks, items, deities, lore,
  situations, session history, the party, or current world state. Trigger on phrases
  like "look up", "what do we know about", "is there a page for", "find the entry
  for", "does the wiki say", "search the wiki", "what's the current state of", "who
  is", "where is", "what happened with". Also trigger silently whenever you would
  otherwise guess a campaign detail — if you are not certain something is established
  canon, search first. Every other Shattered Sea skill defers to this one for lookups.
  Uses a tiered search (in-context index/hot → frontmatter → qmd semantic search):
  fast on easy lookups, comprehensive on hard ones.
---

# TTRPG Wiki Query — Shattered Sea

**This is how you find things. Use it before you state anything.**

The campaign has 250+ wiki pages and you carry almost none of them in context. The
single worst failure mode in a sandbox wiki is **confidently inventing a fact that
contradicts established canon** — a renamed NPC, a ship that sank two sessions ago, a
faction that wants the opposite of what you said. This skill exists to make that
failure impossible: when a campaign fact matters, you retrieve it instead of guessing.

Two non-negotiables:

1. **Never assert an in-world fact you have not found in a wiki page** (or confirmed is
   genuinely absent). If you can't find it, say so — don't fill the gap with invention.
2. **Gather *complete* context, not the first hit.** A page rarely stands alone. The
   NPC links to a faction, a situation, a location, a session. Incomplete context
   produces answers that are locally right and globally wrong.

---

## The tiered method

Climb the tiers in order. **Stop the moment you have a confident, complete answer** —
most lookups never reach Tier 3. Each tier is more powerful and more expensive than the
last, so paying for Tier 3 on a question Tier 1 already answered just wastes time.

### Tier 1 — What you already have (free)

`wiki/index.md` and `wiki/hot.md` are cheap and often already in context.

- **`index.md`** is the master catalog — every page, by path, with its one-line summary.
  Use it to answer *"does a page exist, and where?"* and to turn a vague name into an
  exact path. If `index.md` lists the entity, you have your file in one step.
- **`hot.md`** is current world state — live threads, faction clocks, where the party is
  *right now*. Any "what's the current state of…" or "what's happening with…" question
  starts here, because hot.md is curated to be the present-tense truth.

If the answer is a known page's location or a piece of live state, you may already be
done. Read the specific file (Tier 2's read step) and stop.

### Tier 2 — Frontmatter and exact-term search (fast, deterministic)

When you know the name, slug, or a distinctive term, you don't need an LLM — you need a
match. Two fast tools, no rerank latency:

- **Grep the vault** for proper nouns, slugs, or distinctive phrases:
  ```bash
  grep -rli "barnaby rook" wiki/        # which files mention it
  grep -rn "summary:" wiki/entities/characters/  # scan summaries in a branch
  ```
  Every file leads with a `summary:` frontmatter line written to answer *what is this
  right now, and why does it matter*. **Read summaries before opening full files** —
  often the summary is the whole answer, and you save the context budget.

- **`qmd search`** — BM25 keyword search, no LLM, returns in well under a second. Best
  when you know the vocabulary (exact names, code-like identifiers, distinctive terms):
  ```bash
  qmd search "Uncertainty dry dock La Vasca" -c shattered_sea_wiki
  ```

Then **Read the actual file** for the matched path. qmd and grep tell you *which* file;
the file itself is the source of truth — read it directly (full content, line numbers,
and you can see its wikilinks for the completeness pass below).

### Tier 3 — Semantic search (comprehensive, slower)

Reach for this when you *don't* know the exact term: conceptual or thematic questions,
fuzzy memory, synonyms, "anything we have about…", or when Tiers 1–2 came up empty or
partial. `qmd query` runs hybrid retrieval (keyword + vector + reranking) and finds pages
by *meaning*, not just words. It takes ~15–20s because of the rerank step — worth it for
recall, wasteful for a lookup you could have grepped.

```bash
qmd query "what favor does Nona want from Perrin" -c shattered_sea_wiki --json \
  | jq -r '.[] | "[\(.score)] \(.file)\n\(.snippet)\n"'
```

The `jq` filter strips qmd's repeated per-result `context` blob and keeps only score,
path, and snippet — far leaner on your context budget. Then Read the top files.

For how to craft `lex` / `vec` / `hyde` queries, when to add an `intent`, and how to
combine them for hard questions, read **`references/qmd-querying.md`**. The default
single-line `qmd query "..."` form auto-expands and is the right starting point; reach
for the structured forms when a plain query underperforms.

---

## The completeness pass (always)

A single page is a starting point, not an answer. Once you have your primary hit, gather
the pages it depends on — this is what makes context *comprehensive* rather than just
*present*:

- **Follow the `relationships:` frontmatter** and inline `[[wikilinks]]` from the page.
  An NPC's faction, home location, the situation they're entangled in, the ship they crew.
- **Read summaries first.** For each linked page, the `summary:` frontmatter usually tells
  you whether you need the full file. Open the body only when the summary is insufficient
  (the reading-order: summary → section → full).
- **Pull current state.** If the entity appears in `hot.md` or an active situation
  (`wiki/situations/active/`), that present-tense state overrides older page prose.

Stop expanding when further pages stop changing the answer. The goal is *complete enough
to be correct*, not *the whole vault*.

---

## Escalation to raw sources

The canonical wiki (`shattered_sea_wiki`) is the default and usually sufficient. Only when
a compiled page is **missing or visibly incomplete** for what you need, search the raw
sources — unprocessed GM notes, transcripts, and drafts:

```bash
qmd query "<question>" -c shattered_sea_raw --json | jq -r '.[] | "[\(.score)] \(.file)\n\(.snippet)\n"'
```

Treat raw hits as **draft, not settled canon** — flag that the fact came from raw material
and may not yet be reconciled into the wiki. If a raw source answers something the wiki
should have, that's a signal the page needs ingesting; note it.

---

## Reporting what you found

How you close out a search determines whether the next step is trustworthy:

- **Ground every claim in a path.** When you state a campaign fact, it should be traceable
  to a file you read — reference it (`wiki/entities/.../barnaby-rook.md`). This lets the DM
  verify and lets you catch your own drift.
- **Be explicit about absence.** If the wiki genuinely has nothing, say
  *"No wiki page covers X"* — do not manufacture an answer. Absence is useful information
  (it usually means the page should be created, which routes to a `prep-*` skill).
- **Surface contradictions, don't resolve them silently.** If two pages disagree, or a page
  contradicts `hot.md`, present both and flag it per the discrepancy protocol — append to `wiki/discrepancy-log.md`, never quietly pick one.

---

## Index freshness

A write hook (`.claude/hooks/qmd-reindex.sh`) re-indexes the vault after wiki edits, so
qmd's keyword search and file list stay current automatically — you don't manage this.

One caveat worth knowing: vector **embeddings** are regenerated in the background and lag a
little behind brand-new pages. So a page created moments ago in *this* session may not yet
surface in `qmd query` semantic results. That's fine — for pages you just wrote you already
have them in context, and grep / `qmd search` (keyword) catch them immediately. If
`qmd status` ever shows the index badly stale, `qmd update` re-indexes on demand.

---

## Quick reference

| Need | Tool |
|---|---|
| Does a page exist / where is it | `wiki/index.md` (Tier 1) |
| Current world state, live threads | `wiki/hot.md` (Tier 1) |
| Find pages by exact name / term | `grep -rli` or `qmd search … -c shattered_sea_wiki` (Tier 2) |
| Find pages by meaning / concept | `qmd query "…" -c shattered_sea_wiki --json \| jq …` (Tier 3) |
| Read a known page | Read the file directly (full content + wikilinks) |
| Raw / unprocessed sources | `qmd … -c shattered_sea_raw` (escalation only) |

| Reference file | Read when |
|---|---|
| `references/qmd-querying.md` | Writing lex/vec/hyde queries, using `intent`, tuning a query that underperformed, or the collection/path map |

Operational rules (auto-correct, wikilinks) are in `.claude/skills/ttrpg-llm-wiki-init/references/`. Sandbox rules are in CLAUDE.md (always loaded).

---
name: cross-linker
description: >
  Scan the Obsidian wiki and automatically discover missing cross-references between pages.
  Use this skill whenever the user says "link my pages", "find missing links", "cross-reference",
  "connect my wiki", "add wikilinks", "what pages should be linked", "weave this into the graph",
  "improve discoverability", or "needs more connections". Also trigger automatically after any
  wiki-ingest or ttrpg-writing run — new pages are almost always under-connected and this skill is
  the fix. Trigger when wiki-lint reports orphan pages, or when the user says things like
  "my wiki feels disconnected" or "pages aren't linked well". This is a write-heavy skill —
  it actually modifies pages to add links. When in doubt, run it — a well-linked wiki compounds
  in value every time a new page connects to something that already exists.
---

# Cross-Linker — Automated Wiki Cross-Referencing

Weave the wiki's knowledge graph tighter by finding and inserting missing `[[wikilinks]]` between pages that should reference each other but currently don't. The goal is a graph where every new page immediately connects to the existing body of knowledge — orphans and dead-ends are the primary symptom of a poorly linked wiki.

**Requires Obsidian to be open.** This skill uses the Obsidian CLI (`obsidian`) throughout. Verify tools are available before starting:

```bash
bash .claude/skills/cross-linker/scripts/check-tools.sh
```

If any tool is missing, follow the remediation hint in the output. For `obsidian` failures, open Obsidian and retry.

## Before You Start

1. Resolve config per `llm-wiki` § Config Resolution. Variables needed: `OBSIDIAN_VAULT_PATH`, `OBSIDIAN_LINK_FORMAT` (default: `wikilink`).
2. Read `content/index.md` to get the full entity catalog and one-line descriptions.
3. Check `git log --oneline -5` to identify recently ingested pages — focus linking effort there first.
4. Run a quick scope assessment to know where to focus:
   ```bash
   bash .claude/skills/cross-linker/scripts/orphans-clean.sh -limit 10 -suggest
   ```
   This shows your top-priority orphans with QMD-suggested related pages. Use `-suggest` output to guide Step 2 — those suggested paths are high-confidence link candidates. Keep `-limit` at 10 or below when using `-suggest`; each orphan triggers a QMD vector search, so higher limits add ~1–2 seconds per result.

When inserting links, apply the format from `llm-wiki/SKILL.md` (Link Format section) using `OBSIDIAN_LINK_FORMAT`. When `markdown`, compute the relative `.md` path from the file being edited to the target.

## Step 1: Build the Page Registry

Glob all `.md` files in `content/` (excluding `.obsidian/`). For each page, extract from frontmatter only — read no bodies yet:

- **Filename** (without `.md`) — this is the wikilink target
- **Title**, **aliases**, **tags**, **category** from frontmatter
- **Summary** — `summary` field or first line

Build a lookup table: `page_name → { path, title, aliases, tags, summary }`

This vocabulary is the only thing you need to score candidates in Step 3. You can also run `obsidian tags sort=count counts` to quickly identify high-traffic tags worth prioritizing for connection scoring.

## Step 2: Find Unlinked Mentions

**Orphan and dead-end sweep first:**
```bash
# Orphan pages (no incoming OR outgoing links) — highest priority:
bash .claude/skills/cross-linker/scripts/orphans-clean.sh                    # all orphans
bash .claude/skills/cross-linker/scripts/orphans-clean.sh -limit 20          # cap results
bash .claude/skills/cross-linker/scripts/orphans-clean.sh -limit 10 -suggest # with QMD suggestions (keep limit ≤ 10 — each result runs a vector search)

obsidian deadends        # pages with no outgoing links — secondary candidates
obsidian deadends total  # quick count to scope the work
```

Orphan pages have no incoming or outgoing links — they're fully invisible to anyone navigating the wiki. Dead-ends link to nothing, so they're sinks. Work orphans first, dead-ends second.

Then find unlinked text mentions using `obsidian search` and `obsidian backlinks` — the key is working entity-by-entity rather than page-by-page, which lets you build the full candidate list without reading any page bodies:

For each entity `E` in the registry (skip names under 4 characters — they're too likely to be common words and will generate noise):

1. **Get existing backlinks** — pages already linking to E; nothing to do for them:
   ```bash
   obsidian backlinks file="E"
   ```

2. **Get existing outgoing links from E** — skip these targets when checking if E needs links added:
   ```bash
   obsidian links file="E"
   ```

3. **Find text mentions of E** — search for the entity's title and any aliases:
   ```bash
   obsidian search query="entity title or alias" limit=30
   ```

4. **Candidates = search results − existing backlinks − {E itself}**
   These pages mention E but don't link to it. Add each as a candidate with score +4 (exact name match).

5. **Augment with tag/directory overlap** using registry data only — no additional reads:
   - Pages sharing 2+ tags with E but no link → score +2 per pair
   - Pages in the same directory as E but no link → score +2 per pair

### Matching considerations

**Diacritics**: If an entity name has accented characters (e.g., `Anzolò`), also search the stripped form (`Anzolo`) — wiki editors often drop diacritics in prose.

**Ambiguous short names**: Names under 4 characters or generic words like "sea", "the", "old" appear everywhere and produce mostly false positives. Skip them.

**Shortest unambiguous path**: Use `[[page-name]]` not `[[full/path/to/page-name]]` when the name is unique across the vault. This keeps links readable and portable.

**Link placement**: When you read a page to apply links (Step 4), only link the first natural mention, not every occurrence. Don't link inside code blocks, frontmatter, or callouts. One link per concept per page is enough — more is noise.

## Step 3: Score and Rank Suggestions

Score each candidate so you can distinguish certain links from guesses.

### Scoring

| Signal | Points | Example |
|---|---|---|
| **Exact name match in text** | +4 | "Beaumont Sel" appears in body text → link to `Beaumont-Sel.md` |
| **Shared tags (2+)** | +2 | Both tagged `npc` + `faction` but no link |
| **Same directory, no link** | +2 | Two ship pages with no cross-reference |
| **Mentioned entity/concept** | +2 | Page mentions "Antheri ruins" → link to the lore page |
| **Cross-category connection** | +2 | NPC page links to a faction page — different knowledge layers make this architecturally valuable |
| **Peripheral→hub reach** | +2 | A new page with ≤ 2 links connected to a hub page with ≥ 8 — pulls the new page into the graph |
| **Partial name match** | +1 | "crown" appears but page is `Sunken-Crown` — plausible but ambiguous |

### Confidence labels

| Score | Label | Action |
|---|---|---|
| ≥ 6 | **EXTRACTED** | Effectively certain — exact mention or very strong multi-signal match. Apply inline. |
| 3–5 | **INFERRED** | Reasonable inference — shared context, cross-category, peripheral→hub. Apply inline or as Related. |
| 1–2 | **AMBIGUOUS** | Weak or partial match. Skip these — they're more likely to confuse than help. |

Include confidence labels in the report so the user can review INFERRED links before fully trusting them.

## Step 4: Apply Links

For each page with missing links, read it now — this is the first full-page read in the workflow:

```bash
obsidian read file="page-name"
```

### 4a: Inline linking (preferred)

Wrap the first natural mention in wikilinks:

```markdown
Before: The Sable Company hired Beaumont Sel to investigate.
After:  The Sable Company hired [[Beaumont-Sel]] to investigate.
```

Use `[[path|display text]]` when the wikilink path differs from the display text:
```markdown
[[npcs/Beaumont-Sel|Beaumont Sel]]
```

### 4b: Related section (fallback)

When pages are semantically related but the term isn't mentioned naturally in the body, add a `## Related` section at the bottom:

```markdown
## Related

- [[factions/Sable-Company]] — Beaumont's employer during the Antheri investigation
- [[lore/Antheri-Ruins]] — primary site of the events described above
```

If a `## Related` section already exists, append to it — don't create a duplicate.

## Step 5: Report

Present a summary:

```markdown
## Cross-Link Report

### Links Added: 23 across 12 pages

| Page | Links Added | Confidence | Type |
|---|---|---|---|
| `npcs/Beaumont-Sel.md` | 3 | EXTRACTED | 2 inline, 1 related |
| `factions/Sable-Company.md` | 5 | INFERRED | 3 inline, 2 related |

### Orphan Pages Remaining: 2
- `lore/Fae-Crossroad.md` — no incoming or outgoing links found
- `beastiary/fey/Moucheron.md` — no related pages identified

### Pages Skipped: 3
- `content/index.md`, `content/hot.md` — structural files, not content entities
- `content/_meta/taxonomy.md` — meta file
```

## Step 6: Commit and Update Hot Cache

```bash
git add content/ && git commit -m "cross-link: add N links across M pages"
```

Update `content/hot.md` — add a one-line summary to Recent Activity: e.g. "Cross-linked 23 mentions across 12 pages; 2 orphans remain." Keep the last 3 operations.

## Tips

- Run this after every ingest. New pages are nearly always under-connected, and every unlinked mention is a missed navigation path for anyone reading the wiki.
- Be conservative with inline links — one link per concept per page is the goal. More than that creates visual clutter without navigation benefit.
- Respect existing structure. If a page carefully curates a `## Key Concepts` section, add to it rather than creating a separate `## Related`.
- Entity pages (NPCs, factions, ships) are link magnets — they should be referenced from almost every related content page. Prioritize them.
- Pages in `content/_meta/` and `content/index.md` are structural, not content entities. Don't link to them as if they were wiki articles.


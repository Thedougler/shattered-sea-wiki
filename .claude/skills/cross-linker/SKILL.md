---
name: cross-linker
description: >
  Use when the wiki needs more cross-references between pages. Trigger on:
  "link my pages", "find missing links", "cross-reference", "connect my wiki",
  "weave this into the graph", orphan/deadend pages reported by wiki-lint, or
  after any ingest or writing run — new pages are almost always under-connected.
---

# Cross-Linker

Add missing `[[wikilinks]]` between wiki pages that reference each other but aren't linked. Orphans (no inbound links) and deadends (no outbound links) are the primary targets.

Link conventions: always alias (`[[slug|Display Name]]`), first mention only per section, bidirectional for durable relationships. Full rules in `.claude/skills/ttrpg-llm-wiki-init/references/wikilink-standards.md`.

## Triage — Start Here

A full-vault pass is impractical in one session. Every run targets a batch.

1. Get the target list from wiki-lint:
   ```bash
   sea lint 2>&1 | grep -E "orphan|deadend" | grep -v "wiki/assets/"
   ```

2. Pick a batch of **15–25 targets** per run. Prioritize:
   - **Orphans** over deadends (orphans are invisible to the graph)
   - **Entity pages** (NPCs, factions, ships, places) over generic items
   - **Recently created/ingested pages** — check `git log --oneline -10`
   - Skip: junk files (`" 2.md"` duplicates), asset files, stat-block-only creature pages (these are reference data, not narrative — link them only if a narrative page references the creature)

3. Read `wiki/index.md` — this is the entity catalog with slugs, display names, and summaries. Use it as your lookup for finding link targets. Do NOT build a separate registry.

## Orphan Fix (no inbound links)

The page exists but nothing links to it. Find pages that *should* link to it.

For each orphan:
1. **Read the orphan's frontmatter + first few lines** to get its display name, aliases, and what it is.
2. **Search for text mentions** of the entity across the vault:
   ```bash
   grep -rli "entity name" wiki/ --include="*.md" | grep -v index.md
   ```
   Use `-i` for case-insensitive matching. Search both the display name and the slug form. For accented names (e.g. Anzolo), search both accented and stripped forms.
3. **Read each candidate page** and wrap the first natural mention in a wikilink:
   ```
   Before: Nona sent Anzolo to handle it.
   After:  Nona sent [[anzolo|Anzolo]] to handle it.
   ```
4. If no text mention exists but a **semantic parent** is obvious (e.g. an item belongs to an NPC, a building is in a settlement), read the parent page and add the link to its relevant section or a `## Related` block.
5. **Duplicate check:** If grep finds mentions that already link to a *different file* with a similar name (e.g. `minor/dario.md` vs `npcs/dario-vanni.md`), the files may be duplicates of the same entity. Flag these for the DM rather than adding a second link.

## Deadend Fix (no outbound links)

The page has inbound links but links to nothing else. It needs outbound links added.

For each deadend:
1. **Read the page body.** Look for entity names mentioned in prose that aren't wikilinked.
2. **Check each name against `wiki/index.md`** — if a matching slug exists, wrap the first mention.
3. For **generic items** (weapons, ship repairs, supplies): link to the NPC or vehicle that uses/owns them, or the place they're found. If no natural prose mention exists, add a short `## Related` entry.
4. **Stat-block-only pages** (`entities/creatures/`): these have YAML stat blocks and no prose. Use the `## Related` fallback to link to the encounter, dungeon, or situation that features them.

## Applying Links

**Inline (preferred):** Wrap the first natural mention per section. Never inside frontmatter, code blocks, or callouts.
```markdown
Before: The Sable Company hired Beaumont Sel to investigate.
After:  The Sable Company hired [[beaumont-sel|Beaumont Sel]] to investigate.
```

**Related section (fallback):** When pages are semantically connected but don't mention each other in prose:
```markdown
## Related

- [[sable-company|Sable Company]] — Beaumont's employer during the Antheri investigation
```
Add to an existing `## Related` section if one exists. Respect curated sections like `## Key Concepts` — add there instead of creating a duplicate.

**Bidirectional rule:** If A links B as a durable relationship (not a passing mention), B should link back to A.

## Exclusions

Do not add cross-links to or from:
- `wiki/system/`, `wiki/dm/`, `wiki/rules/`
- System files: `index.md`, `hot.md`, `log.md`, `discrepancy-log.md`, `hub.md`, `work-queue.md`, `faq.md`, `player-primer.md`
- Duplicate/broken files (filenames with spaces, `" 2.md"` suffixes)

`wiki/sessions/` files (run guides, recaps) are valid cross-link targets — they reference entities heavily and benefit from wikilinks. Apply the same inline-first, first-mention-per-section rules as entity pages.

Do not link to `index.md` or `hot.md` from content pages — they are agent-facing, not content entities.

## Commit and Report

After applying links:

```bash
git add wiki/
git commit -m "cross-link: add N links across M pages"
```

Update `wiki/hot.md` — add a one-line entry to Recent Activity listing what was connected.

Report to the user:
```
## Cross-Link Summary
- Links added: N across M pages
- Orphans resolved: K (list which ones)
- Deadends resolved: J
- Remaining: X orphans, Y deadends still unlinked (next run)
```

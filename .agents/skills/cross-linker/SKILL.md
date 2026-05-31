---
name: cross-linker
description: >
  Use when the wiki needs more cross-references between pages. Trigger on:
  "link my pages", "find missing links", "cross-reference", "connect my wiki",
  "weave this into the graph", "improve discoverability", orphan pages reported
  by wiki-lint, or after any ingest or writing run — new pages are almost always
  under-connected. Also trigger on "my wiki feels disconnected" or "pages aren't
  linked well".
---

# Cross-Linker — Automated Wiki Cross-Referencing

Weave the wiki's knowledge graph tighter by finding and inserting missing `[[wikilinks]]` between pages that should reference each other but don't. Orphans and dead-ends are the primary symptom.

Link conventions are defined in `.claude/skills/ttrpg-llm-wiki-init/references/wikilink-standards.md` — always alias (`[[slug|Display Name]]`), first mention only per section, create stubs for missing targets, bidirectional for durable relationships.

## Before You Start

1. Read `wiki/index.md` to get the full entity catalog.
2. Check recent activity:
   ```bash
   git log --oneline -5
   ```
3. Run wiki-lint to identify orphans and dead-ends — these are priority targets:
   ```bash
   python3 .claude/scripts/wiki_lint.py --json 2>/dev/null | python3 -c "
   import json,sys
   for issue in json.load(sys.stdin):
       if issue['rule'] in ('orphan','deadend'):
           print(f\"{issue['rule']:8s} {issue['path']}\")
   "
   ```

## Step 1: Build the Page Registry

Scan all `.md` files in `wiki/` (excluding `wiki/system/`, `wiki/dm/`, `wiki/sessions/`, and system files like `index.md`, `hot.md`, `log.md`). For each page, extract from frontmatter only — read no bodies yet:

- **Slug** (filename without `.md`) — the wikilink target
- **Title**, **aliases**, **tags**, **category** from frontmatter
- **Summary** field

Build a lookup: `slug → { path, title, aliases, tags, summary }`

Use `find` + frontmatter reads or `mcp__obsidian-vault__obsidian_list_files_in_dir` to enumerate pages. For bulk frontmatter extraction, `mcp__obsidian-vault__obsidian_batch_get_file_contents` is efficient.

## Step 2: Find Unlinked Mentions

Work entity-by-entity, not page-by-page. Skip names under 4 characters (too many false positives).

For each entity `E` in the registry:

1. **Find existing inbound links** — grep for `[[slug` across `wiki/`:
   ```bash
   grep -rl "\[\[${slug}" wiki/ --include="*.md" | grep -v "index.md"
   ```

2. **Find existing outbound links from E** — read the file and extract `[[...]]` targets.

3. **Find text mentions of E** — search for the entity's title and aliases:
   ```bash
   grep -rl "${entity_title}" wiki/ --include="*.md"
   ```
   Or use `mcp__obsidian-vault__obsidian_simple_search` for broader text matching.

4. **Candidates = text mentions − existing inbound links − E itself**
   These pages mention E but don't link to it. Score +4 (exact name match).

5. **Augment with tag/directory overlap** from registry data (no reads):
   - Pages sharing 2+ tags with E but no link → score +2
   - Pages in the same directory as E but no link → score +2

### Matching Considerations

**Diacritics**: Search both accented (`Anzolò`) and stripped (`Anzolo`) forms.

**Shortest unambiguous path**: Use `[[slug|Display Name]]` when the slug is unique. Only path-qualify when needed to disambiguate.

**Link placement**: Only link the first natural mention per section. Never inside code blocks, frontmatter, or callouts.

## Step 3: Score and Rank

| Signal | Points |
|---|---|
| **Exact name match in text** | +4 |
| **Shared tags (2+)** | +2 |
| **Same directory, no link** | +2 |
| **Cross-category connection** | +2 |
| **Peripheral→hub reach** (≤2 links → ≥8 links) | +2 |
| **Partial name match** | +1 |

| Score | Label | Action |
|---|---|---|
| ≥ 6 | **EXTRACTED** | Certain — apply inline |
| 3–5 | **INFERRED** | Reasonable — apply inline or as Related |
| 1–2 | **AMBIGUOUS** | Skip |

## Step 4: Apply Links

Read each page that needs links. Use the Read tool or `mcp__obsidian-vault__obsidian_get_file_contents`, then Edit to apply changes.

### 4a: Inline (preferred)

Wrap the first natural mention in a wikilink with alias:

```markdown
Before: The Sable Company hired Beaumont Sel to investigate.
After:  The Sable Company hired [[beaumont-sel|Beaumont Sel]] to investigate.
```

### 4b: Related section (fallback)

When pages are semantically related but the entity isn't mentioned in prose, append a `## Related` section (or add to the existing one):

```markdown
## Related

- [[sable-company|Sable Company]] — Beaumont's employer during the Antheri investigation
```

Use `mcp__obsidian-vault__obsidian_patch_content` to append to an existing heading, or Edit to add a new section.

## Step 5: Report

```markdown
## Cross-Link Report

### Links Added: N across M pages

| Page | Links Added | Confidence | Type |
|---|---|---|---|
| `wiki/entities/characters/npcs/beaumont-sel.md` | 3 | EXTRACTED | 2 inline, 1 related |

### Orphans Remaining: K
- `wiki/lore/fae-crossroad.md` — no connections found

### Skipped
- System files (`index.md`, `hot.md`, etc.)
```

## Step 6: Commit and Update

```bash
git add wiki/ && git commit -m "cross-link: add N links across M pages"
```

Update `wiki/hot.md` — add a one-line summary to Recent Activity.

## Tips

- Run after every ingest. New pages are almost always under-connected.
- One link per concept per page. More is clutter.
- Respect existing structure — if a page has a curated `## Key Concepts`, add to it rather than creating `## Related`.
- Entity pages (NPCs, factions, ships) are link magnets — prioritize them.
- System files (`wiki/system/`, `index.md`, `hot.md`) are not content entities. Don't link to them.

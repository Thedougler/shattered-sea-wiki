---
name: ttrpg-wiki-organize
description: >
  Use when the wiki's file and folder structure should be evaluated or
  improved for LLM-agent navigability. Trigger on: "organize the wiki",
  "is the structure good?", "sort these files", "should we restructure?",
  "too many files in this directory", "propose improvements", "clean up
  the layout", misplaced files found during other work, directories that
  feel overcrowded or too sparse, or after bulk ingest when new files land
  unsorted. Also trigger when frontmatter type/subtype doesn't match the
  file's path, or when proposing new directories or structural changes.
---

# TTRPG Wiki Organize

Proactive, autonomous organizer for the LLM-wiki file and folder structure.
Analyzes content to determine what structure serves agents best, executes
obvious improvements directly, and defers hard judgment calls to the DM.

There is no single "correct" structure. The optimal layout evolves as the
wiki grows. This skill reasons from first principles about what makes a
folder tree navigable, not from a static canonical template.

**Default mode is autonomous.** Execute what's clear, defer what's not,
report everything.

---

## Governing Principles

These are the design constraints. Every structural decision must trace back
to at least one of them.

**P1 — Path prediction over search.** If an agent knows what something IS,
it should know where it LIVES without searching. Paths encode type. Type
encodes path. When this breaks down, the structure needs work.

**P2 — One dimension of specificity per level.** Three to four levels max.
Deeper than four creates navigation complexity that exceeds the benefit.
When in doubt: flatter.

**P3 — Audience is frontmatter, not folder.** `audience: dm` hides content
from player output. Don't create `dm/` or `private/` folders for audience
separation — use the field. Exception: `wiki/dm/` exists for planning
intelligence that is structurally separate from content.

**P4 — Depth proportional to engagement.** A settlement the party visits
once gets a flat file. A settlement they spend four sessions in earns a
subfolder with sub-locations. Structure follows player attention.

**P5 — Folders earn their existence.** A folder with 1-2 files doesn't
justify itself — flatten up. A folder with 40+ files has lost its sorting
value — subdivide. The sweet spot is 5-25 files per directory.

**P6 — Moves are cheap; wrong moves are expensive.** `git mv` preserves
history. But broken wikilinks, stale frontmatter, and confused scripts
compound across every future agent interaction.

---

## When to Use

- A directory has 40+ files and agents can't predict which subfolder to look in
- A directory has 1-2 files and the extra nesting adds no navigability
- Files at a directory root that share an obvious grouping
- `type`/`subtype` frontmatter doesn't match the file's actual path
- After bulk ingest — new files often land unsorted
- DM asks for a structural audit or proposes a restructure
- You notice a pattern that would improve path prediction

## When NOT to Use

- Content quality (summaries, prose, wikilinks) → `ttrpg-wiki-lint`
- Frontmatter field completion → the write hook handles it
- Cross-linking / orphan resolution → `cross-linker`
- Lore contradictions → `ttrpg-wiki-lint` manual review
- Session-start health check → `ttrpg-llm-wiki-init`

---

## Step 1 — Analyze the Current Structure

Don't start from a canonical template. Start from what exists and evaluate
it against the governing principles.

### Density scan

```bash
# File count per directory (sorted by count, descending)
find wiki -type f -name '*.md' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn

# Directories with only 1-2 files (candidates for flattening)
find wiki -type f -name '*.md' | sed 's|/[^/]*$||' | sort | uniq -c | sort -n | awk '$1 <= 2'

# Directories with 40+ files (candidates for subdivision)
find wiki -type f -name '*.md' | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | awk '$1 >= 40'
```

### Depth scan

```bash
# Deepest paths (should be ≤4 levels below wiki/)
find wiki -type f -name '*.md' | awk -F/ '{print NF-1, $0}' | sort -rn | head -10
```

### Path-prediction test

For 5-10 random files, ask: "If I knew this entity's type and name, could I
predict its path without searching?" If the answer is no for more than 2,
the structure has a navigability problem.

### Type/path alignment

```bash
sea lint 2>&1 | grep -i "type-path-mismatch"
```

### Produce a findings table

Mark each finding ACT (execute now) or DEFER (needs DM).

| Finding | Principle | Act/Defer | Action |
|---|---|---|---|
| `entities/species/` has 1 file | P5 | ACT | Merge `human.md` into `lore/species/`, delete dir |
| `entities/places/calven.md` at root, is an island | P1 | ACT | `git mv` → `places/islands/` |
| `entities/places/the-drowned-maw.md` — region or dungeon? | P1 | DEFER | Could be either; DM decides |
| `entities/items/` has 191 flat files | P5 | DEFER | Needs new subcategory design — DM decision |
| `settlements/calveno/` has 15 files | P4 | — | Keep as-is, engagement justifies depth |

---

## Step 2 — Act or Defer

For each finding, decide: can you execute this autonomously, or does the DM
need to weigh in?

### ACT autonomously when ALL of these are true

1. **The target location is unambiguous.** There is exactly one correct
   subfolder, determined by what the file IS (read it, don't guess from the
   filename).
2. **The subfolder already exists**, or creating it groups 5+ files that
   clearly belong together.
3. **No scripts, skills, or code reference the current path.** Check:
   ```bash
   grep -r "current/path/slug" .claude/ packages/ --include="*.md" --include="*.ts" --include="*.py" | grep -v node_modules
   ```
   If zero hits, the move has near-zero blast radius.
4. **The change doesn't rename or merge entity categories.** Moving a file
   into an existing bucket is autonomous. Redefining what the buckets ARE
   (e.g., merging `minor/` into `npcs/`, splitting `items/` into subtypes)
   is a DM decision.

Autonomous actions to execute directly:

| Action | Example | Principle |
|---|---|---|
| File → obvious existing subfolder | `entities/places/calven.md` → `islands/` (it's an island) | P1 |
| Singleton directory → merge into parent | `entities/species/human.md` → `lore/species/` | P5 |
| Empty directory → delete | `rmdir` after all files moved out | P5 |
| Frontmatter type/subtype → match new path | Update after every move | P1 |
| `-dm.md` file → follow its counterpart | `galewall-dm.md` moves with `galewall.md` | colocation |

### DEFER to the DM when ANY of these are true

- **The file could reasonably go in two places** and you can't resolve it
  by reading the content
- **The change redefines categories** (new subfolder taxonomy, merging
  directories, splitting a large directory into new buckets)
- **Scripts or skills hardcode the current path** — the DM decides whether
  the refactor is worth the blast radius
- **40+ files would move** — that's a structural project, not a quick fix
- **You're uncertain** — an unsorted file at a directory root is honest;
  a file in the wrong subfolder is a lie

For deferred items, log them clearly:

```
DEFERRED: {finding} — {options} — {why it needs DM input}
```

Continue executing autonomous actions. Don't block on deferred items.

### Design questions for deferred proposals

When proposing a structural change to the DM, answer these:

1. Does it improve path prediction?
2. Is the grouping stable as the wiki grows?
3. What's the blast radius (scripts, skills, code)?
4. What's the alternative (including doing nothing)?

---

## Step 3 — Plan and Execute ACT Items

Group all ACT items into batches by target directory. Each batch is one
commit. Skip DEFER items — they're logged for the DM.

For each batch, list:
- Files to move
- Target directory (create if missing)
- Frontmatter fields to update (`subtype`, possibly `type`)

**If more than 10 ACT files: create a `wiki/work-queue.md` entry BEFORE
touching any files.**

---

## Step 4 — Execute a Batch

For each batch, in this exact order:

### 4a. Create target directory if needed
```bash
mkdir -p wiki/entities/places/planes
```

### 4b. Move files with git mv
```bash
git mv wiki/entities/places/elemental-plane-of-water.md wiki/entities/places/planes/
```

**Always `git mv`.** Never `mv` then `git add`. `git mv` preserves
`git log --follow` history.

### 4c. Update frontmatter to match new path

After moving, `type` and `subtype` must match the new path. The linter
defines the mapping — check `frontmatter-defaults.md` if unsure.

### 4d. Check for explicit path references

```bash
grep -r "entities/places/elemental-plane-of-water" wiki/ packages/ .claude/ --include="*.md" --include="*.ts" --include="*.py"
```

Obsidian wikilinks (`[[slug]]`) resolve by filename, not path — most survive
moves. But explicit paths in code, CLI tools, scripts, or skills break. Fix
these before committing.

### 4e. `-dm.md` suffix files move with their counterpart

`galewall-dm.md` goes wherever `galewall.md` goes. The suffix is an
audience-split pattern, not a routing signal.

---

## Step 5 — Validate the Batch

Run validation BEFORE committing:

```bash
# New errors introduced by the move?
sea lint --min-severity error 2>&1 | head -30

# Broken wikilinks?
sea lint 2>&1 | grep "broken-wikilink"

# Type/path mismatches fixed or introduced?
sea lint 2>&1 | grep "type-path-mismatch"
```

**A batch is clean when the linter reports zero new errors.** Fix issues
before committing.

### Rollback

If validation reveals cascading breakage:

```bash
git checkout -- .
```

Reverts all unstaged changes. Reassess before retrying.

---

## Step 6 — Commit, Report, and Defer

One commit per batch. Prefix: `fix:` for structural corrections.

After all ACT batches are committed:
1. Close the work-queue entry if one exists
2. Run `sea lint --summary`
3. Report to the DM:

```
## Executed (autonomous)
- Moved N files across M batches
- Directories created: K
- Directories removed: J
- Frontmatter updated: N files

## Deferred (needs your input)
- {finding} — {options} — {why}
- {finding} — {options} — {why}

## Lint: {summary line}
```

The deferred section is the DM's action queue. If the DM approves any
deferred items in the same session, execute them immediately using the
same batch protocol.

---

## Structural Patterns Worth Knowing

These are patterns this wiki has adopted. They aren't sacred — they're the
current state. Evaluate them against the principles if they seem wrong.

| Pattern | Rationale |
|---|---|
| `entities/creatures/` with `type: monster` | 129 stat-block files; all skills/hooks reference this path. Moving would be a multi-system refactor — propose to DM if warranted, never unilateral. |
| `narrative-islands/` not `islands/` | Distinguishes plot-device clusters from geographic `entities/places/islands/` |
| Settlement subfolders (`settlements/calveno/`) | P4 depth-proportional-to-engagement — high-engagement locations earn subfolders |
| `-dm.md` suffix files next to counterpart | Audience-split colocation; `audience:` field does the filtering |
| `rules/backgrounds/`, `rules/classes/`, etc. | Extensions natural to a 5e campaign |

**These patterns can change.** If the content has shifted and a pattern no
longer serves navigability, propose the change with reasoning.

---

## Red Flags — STOP and Reassess

- **Moving 10+ files without a work queue** — create the queue first
- **File could go in two places** — DEFER, don't guess
- **Redefining category boundaries** (merging dirs, new taxonomy) — DEFER
- **40+ files would move in one structural change** — DEFER
- **Scripts or skills hardcode the path** — DEFER
- **Skipping validation after a batch** — run the linter
- **Using `mv` instead of `git mv`** — undo, use `git mv`
- **Committing with lint errors** — fix first
- **Editing file content during an organize pass** — organize is structural;
  content changes are a separate commit
  not a quick fix; propose to DM

---

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "This is obvious, no queue needed" | 10+ files = queue. Obvious moves still break things. |
| "I'll fix frontmatter later" | Frontmatter must match path immediately. Stale frontmatter compounds. |
| "Wikilinks resolve by slug, moves are safe" | Code paths, scripts, and skills may use explicit paths. Check. |
| "This file could go either way, I'll just pick" | DEFER. A wrong placement is worse than an unsorted file. |
| "I'll validate at the end" | Validate per batch. Cascading errors across batches are exponentially harder. |
| "I should fix the content while I'm in the file" | Organize is structural. Content is a separate task. |
| "The canonical structure says X" | The canonical structure is a starting point, not law. Evaluate against the principles. |
| "I need DM approval for everything" | No — clear, unambiguous, zero-blast-radius moves are autonomous. Don't block on the obvious. |
| "I'll just restructure this whole directory" | Redefining categories is a DEFER. Moving files into existing categories is an ACT. |

---

## Reference Files

| File | Load when |
|---|---|
| `.claude/skills/ttrpg-llm-wiki-init/references/universal-structure.md` | Understanding the original design intent and content decision tree |
| `.claude/skills/ttrpg-llm-wiki-init/references/frontmatter-defaults.md` | Updating frontmatter after a move |
| `.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md` | Commit message format and escalation protocol |

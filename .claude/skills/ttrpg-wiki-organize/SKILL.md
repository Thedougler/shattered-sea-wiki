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

Proactive, dynamic organizer for the LLM-wiki file and folder structure.
Analyzes the actual content to determine what structure serves agents best,
proposes and executes changes, and ensures every change is tracked in git.

There is no single "correct" structure. The optimal layout evolves as the
wiki grows. This skill reasons from first principles about what makes a
folder tree navigable, not from a static canonical template.

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
python3 .claude/scripts/wiki_lint.py 2>&1 | grep -i "type-path-mismatch"
```

### Produce a findings table

| Finding | Principle | Severity | Proposed action |
|---|---|---|---|
| `entities/places/` has 30 root files | P1 — can't predict path | high | Sort into subfolders |
| `entities/species/` has 1 file | P5 — folder doesn't earn existence | low | Merge into `lore/species/` |
| `settlements/calveno/` has 15 files | P4 — depth matches engagement | none | Keep as-is |

---

## Step 2 — Propose Improvements

For each finding, design a structural change. This is where you reason about
what's best for the content — not what a template says.

### Questions to ask for each proposed change

1. **Does this improve path prediction?** After the change, can an agent
   predict where a file lives from its type alone?
2. **Does it reduce or increase depth?** Prefer flatter unless subdivision
   adds real navigability.
3. **Does it match how agents actually use these files?** Files accessed
   together should live near each other.
4. **Is the grouping stable?** Will new content naturally sort into the same
   buckets, or will the categories break as the wiki grows?
5. **What's the blast radius?** How many wikilinks, scripts, and skills
   reference the current paths?

### Propose, don't just execute

Present the findings table and proposed changes to the DM before executing.
Include the reasoning — which principle drives each change, what the
tradeoff is, and what you're uncertain about.

The DM may:
- Approve all proposals
- Approve some and reject others
- Suggest a different structure entirely
- Defer until later

Only execute what's approved.

### When to act without approval

Small, unambiguous fixes that clearly improve P1 and have near-zero blast
radius can be executed directly:

- Moving a single file from a directory root to an obvious existing subfolder
- Creating a subfolder when 10+ files at a root share an obvious grouping
  and no scripts/skills reference the current path
- Merging a 1-file directory into its parent

For anything else — propose first.

---

## Step 3 — Plan the Moves

Group approved moves into batches by target directory. Each batch is one
commit.

For each batch, list:
- Files to move
- Target directory (create if missing)
- Frontmatter fields to update (`subtype`, possibly `type`)
- Blast radius: scripts, skills, or code referencing the current path

**If more than 10 files need moving: create a `wiki/work-queue.md` entry
BEFORE touching any files.**

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
python3 .claude/scripts/wiki_lint.py --min-severity error 2>&1 | head -30

# Broken wikilinks?
python3 .claude/scripts/wiki_lint.py 2>&1 | grep "broken-wikilink"

# Type/path mismatches fixed or introduced?
python3 .claude/scripts/wiki_lint.py 2>&1 | grep "type-path-mismatch"
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

## Step 6 — Commit and Close

One commit per batch. Prefix: `fix:` for structural corrections.

After all batches:
1. Close the work-queue entry if one exists
2. Run `python3 .claude/scripts/wiki_lint.py --summary`
3. Report what changed and what's left

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
- **Guessing where an ambiguous file goes** — propose to DM, don't guess
- **Skipping validation after a batch** — run the linter
- **Using `mv` instead of `git mv`** — undo, use `git mv`
- **Committing with lint errors** — fix first
- **Editing file content during an organize pass** — organize is structural;
  content changes are a separate commit
- **Restructuring a 100+ file directory unilaterally** — that's a project,
  not a quick fix; propose to DM

---

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "This is obvious, no queue needed" | 10+ files = queue. Obvious moves still break things. |
| "I'll fix frontmatter later" | Frontmatter must match path immediately. Stale frontmatter compounds. |
| "Wikilinks resolve by slug, moves are safe" | Code paths, scripts, and skills may use explicit paths. Check. |
| "This file could go either way, I'll just pick" | Propose to DM. A wrong placement is worse than an unsorted file. |
| "I'll validate at the end" | Validate per batch. Cascading errors across batches are exponentially harder. |
| "I should fix the content while I'm in the file" | Organize is structural. Content is a separate task. |
| "The canonical structure says X" | The canonical structure is a starting point, not law. Evaluate against the principles. |

---

## Reference Files

| File | Load when |
|---|---|
| `.claude/skills/ttrpg-llm-wiki-init/references/universal-structure.md` | Understanding the original design intent and content decision tree |
| `.claude/skills/ttrpg-llm-wiki-init/references/frontmatter-defaults.md` | Updating frontmatter after a move |
| `.claude/skills/ttrpg-llm-wiki-init/references/auto-correct.md` | Commit message format and escalation protocol |

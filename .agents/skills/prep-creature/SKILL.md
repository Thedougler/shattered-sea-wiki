---
name: prep-creature
description: >
  Create or expand a creature or monster entry for the Shattered Sea campaign. Invoke
  for: "create stats for [creature]", "I need a [monster] for the encounter", "expand
  the entry for [creature type]", "make a homebrew monster", "design a [creature]",
  "statblock for [enemy]", "bestiary entry for [creature]", "named villain statblock",
  "make me a [monster]". Distinguishes between creature-type lore pages and named
  creature entities. Reads party combat primer before finalizing any stat calibration.
  Uses Fantasy Statblocks plugin codeblock format for all statblocks.
---

> Cross-cutting rules (reading order, sandbox constraints, PC-connection requirement, frontmatter, auto-correct) live in `wiki/system/doctrine.md`. This skill covers only what's specific to its domain.

## Prerequisites

Prerequisites: see reading order in `wiki/system/doctrine.md`. Always check `wiki/index.md` for an existing stub before creating a new page.

Domain-specific:
1. **Named entity or creature type?**
   - Named creature (specific individual): `wiki/entities/characters/npcs/{slug}.md` + statblock
   - Creature type/species lore: `wiki/lore/creatures/{slug}.md`
2. Read `wiki/system/party-combat-primer.md` before finalizing any stat calibration.
   Party primer Avoid flags apply to creature design.

---

## Creature Page Structure

**Lore entry** (`wiki/lore/creatures/`): ecology, behavior, habitat, distinguishing
features, typical encounter role. DM-facing reference prose — not a novel.

**Named entity** (`wiki/entities/characters/npcs/` or `wiki/entities/characters/minor/`):
full NPC structure + integrated statblock. Use `prep-npc` workflow for the NPC page,
then append the statblock in Fantasy Statblocks codeblock format.

**Statblock:** Read `references/STATBLOCK.md` for exact syntax. Read
`references/STATBLOCK-CONFIG.md` for plugin config keys and layout options.

---

## Behavioral Profile

Every creature needs a behavioral profile for encounter use, distinct from lore:

- **Opening move** — what they do in round 1
- **Escalation** — what changes when they reach ~50% HP
- **Morale threshold** — when they flee, surrender, or go berserk
- **Encounter role** — controller / bruiser / skirmisher / artillery / lurker

Read `references/NAMED-ENEMIES.md` for named antagonist stat citation patterns and
villain design.

Load `ttrpg-writing` for all prose and formatting standards.

---

## Filing

- Lore entry: `wiki/lore/creatures/{slug}.md`
- Named entity: `wiki/entities/characters/npcs/{slug}.md`
- Add to `wiki/index.md` in appropriate section
- Add reciprocal links to all referenced entities

---

## Reference Files

| File | Read when |
|---|---|
| `references/MONSTER.md` | Full monster page structure, homebrew stat integration |
| `references/MONSTER-EXAMPLES.md` | Worked examples — quality and format benchmark |
| `references/BESTIARY.md` | Bestiary structure for creature-type lore entries |
| `references/NAMED-ENEMIES.md` | Named antagonist stat citations and villain patterns |
| `references/STATBLOCK.md` | Fantasy Statblocks plugin syntax and codeblock format |
| `references/STATBLOCK-CONFIG.md` | Statblock plugin configuration keys and layouts |
| `references/STAT-BLOCKS.md` | Encounter enemy stat block reference tables |

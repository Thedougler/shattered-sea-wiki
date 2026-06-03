---
name: prep-creature
description: >
  Create or expand a creature or monster entry for the Shattered Sea campaign. Invoke
  for: "create stats for [creature]", "I need a [monster] for the encounter", "expand
  the entry for [creature type]", "make a homebrew monster", "design a [creature]",
  "statblock for [enemy]", "bestiary entry for [creature]", "named villain statblock",
  "make me a [monster]".
---

> **Shared prep conventions** — stub check, interview + PC-connection requirement, combat calibration, prose pass, and filing — live in [`prep-family-standards`](../ttrpg-llm-wiki-init/references/prep-family-standards.md). Read it before generating; this file covers only what's specific to this content type.
**Named entity or creature type?**
- Named creature (specific individual): `wiki/entities/characters/npcs/{slug}.md` + statblock
- Creature type/species lore: `wiki/lore/creatures/{slug}.md`

Read `wiki/system/party-combat-primer.md` before finalizing any stat calibration.
Party primer Avoid flags apply to creature design.

---

## Interview

If the user message doesn't already answer these, ask all at once:
- CR target or party level
- Role (controller / bruiser / skirmisher / artillery / lurker / solo boss)
- One-sentence concept — origin and defining trait
- Named individual or creature type/species lore?
- Which PC thread connects to this creature, and how?

Name the connecting PC or ask before generating.

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

---

## Cross-Skill Coordination

- **Named creature:** Run `prep-npc` workflow first to generate the NPC page, then append the statblock here.
- **Encounter calibration:** If this creature anchors a specific combat encounter, load `prep-encounter` after completing this skill for full calibration against the party's empirical patterns.
- **Dungeon inhabitant:** If placing this creature in a dungeon or lair, `prep-dungeon` Phase 2 routes here — deliver the statblock and behavioral profile, then return to that skill.

---

## Frontmatter

Universal and entity fields are auto-completed by the write hook. You must author:

- Lore entries (`wiki/lore/creatures/`): `type: lore`, `subtype: creature`
- Named entities: handled by `prep-npc` frontmatter; append statblock to the body only

---

## Visual Aid

Load `ttrpg-visual-aids` to generate a creature illustration. Category: **Portraits**
(3:4 vertical) for named creatures, or **Scene art** (16:9) showing the creature in
its habitat for lore entries. Skip for generic stat blocks embedded in encounter files.

---

## Filing

- Lore entry: `wiki/lore/creatures/{slug}.md`
- Named entity: `wiki/entities/characters/npcs/{slug}.md`
- Add to `wiki/index.md` in appropriate section
- Add reciprocal links to all referenced entities
- Commit: `feat: creature — {slug} — {one-line summary}`

---

Load `ttrpg-writing` before writing any prose. **DM-facing reference** for lore entries,
behavioral profiles, and stat integration. **Player-facing prose** for `[!read-aloud]`
descriptions.

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
| `../ttrpg-writing/references/dm-reference-standards.md` | Writing lore entries, behavioral profiles |
| `../ttrpg-writing/references/player-facing-prose.md` | Writing `[!read-aloud]` creature descriptions |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement and conversion |
| `../ttrpg-llm-wiki-init/references/auto-correct.md` | Fixing structural issues during or after content creation |
| `../ttrpg-llm-wiki-init/references/wikilink-standards.md` | Creating or fixing wikilinks |

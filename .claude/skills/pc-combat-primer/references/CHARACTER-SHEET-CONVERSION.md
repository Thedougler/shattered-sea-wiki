# Character Sheet Conversion — PDF to Agent-Readable Markdown

> Read this when a character sheet PDF is available and needs conversion to
> the canonical agent-readable format.

---

## Purpose

PDF character sheets are authoritative but agent-hostile. This protocol converts
them into a structured markdown format that serves as the **canonical mechanical
reference** for all downstream operations (combat profiles, encounter design,
primer updates). The PDF stays in place for player reference; the markdown copy
is the agent's source of truth.

---

## When to Convert

- First time a PC's PDF sheet is provided or updated
- After a level-up when the player provides an updated PDF
- When a combat profile references sheet data that doesn't have a markdown source

---

## File Locations

| File | Path | Purpose |
|---|---|---|
| Original PDF | Keep where found (typically `.raw/characters/` or `wiki/entities/characters/pcs/`) | Player reference; do not move or delete |
| Agent-readable markdown | `wiki/system/players/{pc-slug}-sheet.md` | Canonical mechanical reference |

If the PDF lives in `.raw/characters/`, it stays there. If a player drops a new
PDF in `Inbox/characters/`, convert it, then archive the PDF to `.raw/characters/`
via `archive_source.py`.

---

## Frontmatter Template

```yaml
---
type: system
subtype: character-sheet
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "{PC name} character sheet — level {N} {class(es)}. Canonical mechanical reference for agent operations."
pc: "{pc-slug}"
pc_level: {number}
class_levels: "{e.g., Bard 3 / Warlock 1}"
pdf_source: "{relative path to original PDF}"
last_synced: "{date — when this markdown was last verified against PDF}"
created: "{date}"
updated: "{date}"
tags:
  - player-resource
  - character-sheet
---
```

---

## Body Structure

Organize for agent scanning — group by operation type, not by how the PDF
lays out the data.

### Section Order

1. **Identity** — name, class/level, race, background, player
2. **Ability Scores & Saves** — single table, includes proficiency markers
3. **Combat Stats** — AC, HP, speed, initiative, proficiency bonus
4. **Attacks & Damage** — all attack options with full stat lines
5. **Spellcasting** (if applicable) — DC, attack bonus, slots, known/prepared spells
6. **Class Features** — organized by class, level gained, mechanical effect
7. **Racial/Species Traits** — mechanical features from race/species
8. **Skills** — full skill list with bonuses and proficiency level
9. **Equipment** — notable items with mechanical effects (skip mundane supplies)
10. **Resource Pools** — all limited-use features with max and recovery
11. **Conditions & Resistances** — immunities, resistances, vulnerabilities, senses

---

## Formatting Rules

### Ability Scores & Saves (combined table)

```markdown
## Ability Scores & Saves

| Ability | Score | Mod | Save | Prof? |
|---|---|---|---|---|
| STR | 6 | -2 | -1 | |
| DEX | 18 | +4 | +5 | |
| CON | 15 | +2 | +3 | |
| INT | 11 | +0 | +1 | |
| WIS | 11 | +0 | +3 | Yes |
| CHA | 20 | +5 | +8 | Yes |
```

Note: Include any flat bonuses from items (e.g., Cloak of Protection +1) in the
save column and note the source.

### Attacks (agent-optimized format)

```markdown
## Attacks & Damage

| Attack | To Hit | Damage | Type | Range | Properties | Notes |
|---|---|---|---|---|---|---|
| Longsword (Pact) | +7 | 1d8+5 | Slashing/Necrotic/Psychic/Radiant | 5 ft | Versatile, Sap | CHA-based via Pact |
| Eldritch Blast | +7 | 1d10 | Force | 120 ft | V/S | Warlock cantrip |
| Booming Blade | +7 | 1d8+5 + 1d8 thunder | Slash + Thunder | 5 ft | S/M, rider on move | Extra 2d8 if target moves |
```

### Spellcasting (organized for quick lookup)

```markdown
## Spellcasting

- **Spell save DC:** 15
- **Spell attack:** +7
- **Spellcasting ability:** CHA

### Slots

| Source | Level | Slots | Recovery |
|---|---|---|---|
| Bard | 1st | 4 | Long rest |
| Bard | 2nd | 2 | Long rest |
| Warlock (Pact) | 1st | 1 | Short rest |

### Spells Known

| Spell | Level | Source | Cast time | Range | Duration | Conc? | Key effect |
|---|---|---|---|---|---|---|---|
| Minor Illusion | Cantrip | Bard | 1A | 30 ft | 1 min | No | 5ft cube illusion |
| Vicious Mockery | Cantrip | Bard | 1A | 60 ft | Inst | No | WIS 15 or 1d6 psychic + disadv |
| Healing Word | 1st | Bard | 1BA | 60 ft | Inst | No | 1d4+5 HP |
| Tasha's Hideous Laughter | 1st | Bard | 1A | 30 ft | 1 min | Yes | WIS 15 or prone + incapacitated |
```

### Class Features (mechanical focus)

```markdown
## Class Features

### Bard (Level 3)

| Feature | Effect | Uses | Recovery |
|---|---|---|---|
| Bardic Inspiration | Grant 1d6 to ally within 60ft; add to failed d20 test | 5 | Long rest |
| Jack of All Trades | +1 to non-proficient ability checks | Passive | — |
| Cutting Words | Reaction: subtract 1d6 from enemy attack/check/damage | Uses Inspiration | — |
| Expertise | Double proficiency in Acrobatics, Persuasion | Passive | — |

### Warlock (Level 1)

| Feature | Effect | Uses | Recovery |
|---|---|---|---|
| Pact of the Blade | Conjure/bond weapon; use CHA for attacks; choose damage type | Passive | — |
| Eldritch Invocations | Pact of the Blade | Passive | — |
```

### Resource Pools (consolidated)

```markdown
## Resource Pools

| Resource | Max | Recovery | Notes |
|---|---|---|---|
| Bardic Inspiration | 5 | Long rest | Also powers Cutting Words |
| Bard spell slots (1st) | 4 | Long rest | |
| Bard spell slots (2nd) | 2 | Long rest | |
| Warlock Pact slot (1st) | 1 | Short rest | |
| Pack Tactics (Rattkin) | 2 | Short rest | Reaction attack when adjacent ally hits |
| Hit Dice | 4d8 | Long rest (half) | Healing during short rest |
```

---

## Conversion Quality Gates

- **Every number must be verifiable** from the PDF. If a value seems wrong
  (e.g., save doesn't match ability mod + proficiency), note the discrepancy
  rather than silently "fixing" it — the player may have a magic item or feature
  you're not seeing.
- **No editorializing.** This is a mechanical reference, not a primer. Don't add
  "this is good for..." commentary — that belongs in the combat profile.
- **Include inactive/conditional features.** A feature that only works in specific
  conditions (e.g., Umbral Sight in dim/dark) still gets listed with its condition.
- **Spell descriptions are abbreviated.** Use "Key effect" column for the mechanical
  impact, not full spell text. An agent that needs the full description can look it up.
- **Equipment: only mechanically relevant items.** Skip rope, rations, torches
  (unless they're the party's only light source). Include magic items, weapons,
  armor, and items with unique mechanical effects.

---

## Handling PDF Quality Issues

| Issue | Approach |
|---|---|
| PDF is a scanned image (not text) | Use `preprocess_pdf.py` to OCR extract first |
| Values appear inconsistent | Note discrepancy with `[verify]` tag; don't silently correct |
| Feature text is truncated | Look up the feature in the PHB 2024 source and fill in |
| PDF is outdated (lower level than current) | Convert what's there; note `[outdated — verify level]` |
| Multiple pages / complex layout | Process page by page; ability scores first, then features |

---

## Post-Conversion Steps

1. Write the markdown to `wiki/system/players/{pc-slug}-sheet.md`
2. Verify frontmatter hook doesn't flag issues
3. Add to `wiki/index.md` under a `## system/players` section if one exists
4. If this conversion was triggered by a combat profile update, continue to
   the profile calculation step — the sheet is now available as a source

---

## Keeping Sheets in Sync

The `last_synced` frontmatter field records when the markdown was last verified
against the PDF. When a player says "I leveled up" or provides a new PDF:

1. Read the new PDF
2. Diff against existing markdown mentally — what changed?
3. Update the markdown: new level, new features, updated scores/slots
4. Bump `last_synced` and `updated` dates
5. Flag downstream documents as stale: combat profile, party combat profile

**Never delete the old content.** If a feature was replaced (e.g., subclass
choice changed), note it as `[replaced at level X]` rather than removing it —
this preserves the history for calibration notes that reference earlier sessions.

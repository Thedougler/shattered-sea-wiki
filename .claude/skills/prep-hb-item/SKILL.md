---
name: prep-hb-item
description: >
  Create a homebrewed D&D 5e item for the Shattered Sea campaign. Invoke for:
  "homebrew an item for [PC]", "design a [item concept]", "make a custom [item]",
  "I want an item that does [effect]", "create a magic item for [PC]",
  "invent an item for the setting". Do NOT use for standard 5e items that already
  exist in RAW — check wiki/entities/items/ first. Symptoms requiring this skill:
  desired item doesn't exist in RAW, needs setting-specific mechanics or flavor,
  or the DM wants to tie an item to a specific PC's story thread.
---

> **Shared prep conventions** — stub check, interview + PC-connection requirement, combat calibration, prose pass, and filing — live in [`prep-family-standards`](../ttrpg-llm-wiki-init/references/prep-family-standards.md). Read it before generating; this file covers only what's specific to this content type.
## Prerequisites

Check `wiki/index.md` for existing item stubs before creating. A reskinned RAW item
beats homebrew when the mechanical effect is the same. Only build new if the setting
flavor or mechanical concept genuinely can't be satisfied by a RAW item.

---

## Interview

If not answered in the request, ask all at once — not one at a time:
- Which PC is this for? What tension in their backstory, goals, or fears does this item pull on?
- What is the **one thing** this item does — the core mechanic, in one sentence?
- What rarity target? (Common / Uncommon / Rare / Very Rare / Legendary)
- What is the narrative reason the party could encounter this item in the current arc?

Name the connecting PC or ask before generating. If you cannot state the one-thing in one sentence, the design is not ready — ask the DM to narrow it.

---

## Power Budget

**Set rarity before designing mechanics.** Never work backwards from mechanics to rarity.

Read `references/RARITY-BUDGET.md` for full tier tables and RAW benchmarks.

**Quick calibration:**

| Rarity | Power level | Attunement |
|---|---|---|
| Common | Always-on cosmetic or trivial QoL | Never |
| Uncommon | One situational advantage — skill or minor combat | If combat-relevant |
| Rare | One strong broadly-useful advantage, or two situational | Always if combat-altering |
| Very Rare | Game-changing; reshapes encounter design | Always |
| Legendary | Campaign-altering | Always |

**Attunement rule:** Any item that grants a bonus to attack rolls, damage rolls, saving throws, or AC requires attunement. Three or more distinct powers require attunement regardless of individual power level.

**Balance citation:** Before writing mechanics, name 2 RAW items at the same rarity and confirm the item's power is comparable. If it's clearly stronger, raise the rarity.

---

## Prohibited Design Space

Never give items these class-exclusive mechanics:

- Sneak Attack dice (Rogue)
- Rage or Reckless Attack (Barbarian)
- Ki points, Stunning Strike, or Step of the Wind (Monk)
- Bardic Inspiration dice (Bard)
- Divine Smite (Paladin)
- Extra Attack beyond what the PC's class already grants

Use item-native design instead: charges that recover on rest, stored spell effects (X charges,
cast Y at Zth level), skill/ability check bonuses, AC adjustments, condition immunities,
damage resistances.

---

## One-Thing Discipline

Homebrew items do one thing excellently, not three things adequately.

**Signs you are designing three things:**
- The Properties section has three H3 headers
- The item has a combat trigger AND a social trigger AND a passive benefit
- You reached for "and also..." to make it feel interesting

If the item needs three things, identify which one is the item. The others are future items,
or not items at all.

---

## Cross-Skill Coordination

- **NPC vendor:** If the item is sold by a named NPC, run `prep-npc` for that NPC first
  (or confirm the NPC page exists), then wikilink the item to their page and add a reciprocal
  link on the NPC's Connections section.
- **Location context:** If the item is tied to a specific location (dungeon treasure, shop
  inventory, wreck salvage), ensure that location page exists and add a reciprocal wikilink.
- **Called from `prep-dungeon`:** If this skill is invoked mid-dungeon to fill a treasure
  slot, deliver the complete item wiki page, then return to `prep-dungeon` and place the
  item reference in the relevant room's Features block using *italic* typographic encoding.
  The DM review gate still applies — present the item before the dungeon Phase 4 output.
- **Session prep:** If `prep-session` is requesting an item as a session prop or reward,
  complete the DM review gate before the session plan is finalized. An unapproved homebrew
  item in a session plan is a forward commitment to balance.

---

## Output Structure

**Flavor description** — two to four sentences. Appearance, provenance, feel in hand. No
mechanical content. Read-aloud quality: a player could read this before picking it up.

**Stat line** — one line immediately after: `*[Type] · [Rarity] · [Attunement or No attunement]*`

**`## Properties`**
- Label every homebrew mechanic with `**[HB]**`
- Label any RAW-borrowed mechanics with `**[RAW]**`
- Bound every mechanic: range, duration, recovery (long rest / short rest / X charges / at-will)
- State edge cases: undead, unconscious targets, environments (underwater, darkness, etc.)

**`## Limitations`** — What the item cannot do. Explicit limits prevent table arguments.

**`## History`** — Provenance in Shattered Sea. Who made it, who owned it, how it arrived here.

**`> [!dm]`** — DM secrets, hidden mechanics, future hooks. Nothing in this callout is player-facing.

**`## Current Location`** — Where is it now? Who holds, sells, or guards it?

**`## Connections`** — Wikilinks to the connected PC(s), NPC(s), locations, factions.

---

## Frontmatter

Standard entity fields auto-complete. Author these item-specific values:

| Field | What goes here |
|---|---|
| `item_type` | `weapon` / `armor` / `wondrous` / `tool` / `ammunition` |
| `rarity` | `common` / `uncommon` / `rare` / `very-rare` / `legendary` / `artifact` |
| `attunement` | `true` or `false` |
| `homebrew` | Always `true` for this skill |
| `asking_price` | gp value as string — omit entirely if not for sale |

---

## DM Review Gate

**Present the item to the DM before committing.** State: the one-thing, the rarity
justification, and the two RAW benchmarks. Wait for approval before writing to the wiki.

Homebrew items affect game balance at the table. A misbalanced item is harder to retract
after players have used it. This gate is not optional.

---

## Visual Aid

For named, PC-relevant items: load `ttrpg-visual-aids` after DM approval. Category:
**Props** (1:1 square, object-focused). Skip for items never described to players.

---

## Filing

After DM approval:
1. `wiki/entities/items/{slug}.md`
2. Add entry to `wiki/index.md` under `## entities/items`
3. Add reciprocal links in all connected entity files (PC page, NPC vendor, location)
4. Commit: `feat: item — {slug} — {one-line summary}`

---

Load `ttrpg-writing` before writing any prose. **DM-facing reference** for DM callout,
history, and limitations. **Player-facing prose** for flavor description (read-aloud
quality — a player could read this before picking up the item).

---

## Reference Files

| File | Read when |
|---|---|
| `references/RARITY-BUDGET.md` | Setting rarity and checking power against RAW benchmarks |
| `../ttrpg-writing/references/dm-reference-standards.md` | Writing DM callout, history, limitations |
| `../ttrpg-writing/references/player-facing-prose.md` | Writing flavor description |
| `../ttrpg-writing/references/callout-standard.md` | Callout type enforcement and conversion |
| `../ttrpg-llm-wiki-init/references/auto-correct.md` | Fixing structural issues |
| `../ttrpg-llm-wiki-init/references/wikilink-standards.md` | Creating or fixing wikilinks |

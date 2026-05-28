# 5e Statblock Field Reference

All data fields supported by the `Basic 5e Layout` in Fantasy Statblocks. Load this file when generating a statblock from scratch. For codeblock config keys (`layout:`, `columns:`, `monster:`, `extends:`, etc.) see `STATBLOCK-CONFIG.md`. For bestiary registration patterns see `BESTIARY.md`.

---

## Required Fields

| Field | Type | Example |
|---|---|---|
| `name` | string | `"Ancient Red Dragon"` |
| `size` | enum | `Tiny` `Small` `Medium` `Large` `Huge` `Gargantuan` |
| `type` | string | `humanoid` `beast` `monstrosity` `undead` `fiend` `celestial` `dragon` `elemental` `fey` `giant` `construct` `ooze` `plant` `aberration` |
| `alignment` | string | `"neutral evil"` `"chaotic good"` `"unaligned"` |
| `ac` | number or string | `15` or `"15 (natural armor)"` |
| `hp` | number | `136` |
| `hit_dice` | string | `"16d10 + 48"` |
| `speed` | string | `"30 ft., fly 60 ft."` — always quote |
| `stats` | int[6] | `[20, 10, 16, 12, 14, 16]` — STR DEX CON INT WIS CHA |
| `cr` | number or string | `5` or `"1/2"` or `"1/4"` — use string for fractions |

---

## Optional Identity Fields

```yaml
subtype: goblinoid          # humanoid subtype
gender: female              # for NPC pronoun display
environment: "cave, coast"  # habitat tags (display only)
source: "Homebrew"          # bestiary source group
```

---

## Defenses

```yaml
saves:
  - Dex: +5
  - Con: +8
  - Wis: +4

skillsaves:
  - Perception: +7
  - Stealth: +5

damage_vulnerabilities: "fire"
damage_resistances: "cold; bludgeoning, piercing, and slashing from nonmagical attacks"
damage_immunities: "poison, psychic"
condition_immunities: "charmed, frightened, poisoned"
```

All resistance/immunity fields are plain strings. Separate multiple entries with `;` when grouping is meaningful.

---

## Senses and Languages

```yaml
senses: "darkvision 60 ft., passive Perception 17"
languages: "Common, Goblin"
```

Both are plain strings. Always include passive Perception in `senses`.

---

## Traits

```yaml
traits:
  - name: "Pack Tactics"
    desc: "The creature has advantage on attack rolls against a creature if at least one of the creature's allies is adjacent to the creature."
  - name: "Spellcasting"
    desc: "The creature is a 5th-level spellcaster (Wisdom, spell save DC 13, +5 to hit). It has the following druid spells prepared: ..."
```

`traits` = passive features that are always active. Each entry requires `name` and `desc`.

---

## Actions

```yaml
actions:
  - name: Multiattack
    desc: "The creature makes two claw attacks."
  - name: Claw
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 11 (2d6 + 4) slashing damage."
  - name: Fire Breath
    desc: "The creature exhales fire in a 30-foot cone. Each creature in that area must make a DC 15 Dexterity saving throw, taking 45 (10d8) fire damage on a failed save, or half as much on a successful one."
    usage:
      times: 1
      per: day
```

**Attack format**: `"Melee/Ranged Weapon/Spell Attack: +X to hit, reach/range Y ft., one target. Hit: N (XdN + Y) damage type damage."`

Optional `usage` sub-key for limited-use actions.

---

## Bonus Actions

```yaml
bonus_actions:
  - name: Cunning Action
    desc: "The creature takes the Dash, Disengage, or Hide action."
```

---

## Reactions

```yaml
reactions:
  - name: Parry
    desc: "The creature adds 3 to its AC against one melee attack that would hit it. To do so, the creature must see the attacker and be wielding a melee weapon."
```

---

## Legendary Actions

```yaml
legendary_actions:
  - name: ""
    desc: "The creature can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. Spent legendary actions are regained at the start of each turn."
  - name: "Detect"
    desc: "The creature makes a Wisdom (Perception) check."
  - name: "Attack (Costs 2 Actions)"
    desc: "The creature makes one claw attack."
```

The first entry (blank `name`) is the preamble. Subsequent entries are the options. Cost-2+ actions note the cost in the name.

---

## Lair Actions and Regional Effects

```yaml
lair_actions:
  - desc: "On initiative count 20 (losing initiative ties), the creature takes a lair action to cause one of the following effects; the creature can't use the same effect two rounds in a row:"
  - desc: "Magma erupts from a point on the ground the creature can see within 120 feet of it, creating a 20-foot-high, 5-foot-radius geyser. Each creature in the geyser must succeed on a DC 15 Dexterity saving throw or take 21 (6d6) fire damage and be knocked prone."

regional_effects:
  - desc: "The region within 1 mile of the creature's lair is warped by the creature's magic, creating one or more of the following effects:"
  - desc: "Small earthquakes are common within 6 miles of the creature's lair."
```

Each entry uses only `desc` (no `name` key).

---

## Spells

```yaml
spells:
  - "The creature is a 9th-level spellcaster (Charisma, spell save DC 14, +6 to hit)."
  - "Cantrips (at will): fire bolt, mage hand, prestidigitation"
  - "1st level (4 slots): detect magic, mage armor, magic missile, shield"
  - "2nd level (3 slots): misty step, suggestion"
  - "3rd level (3 slots): counterspell, fireball, fly"
  - "4th level (3 slots): greater invisibility, ice storm"
  - "5th level (1 slot): cone of cold"
```

Each entry is a plain string. First entry is always the preamble. Subsequent entries are spell level lines.

---

## Mythic Actions

```yaml
mythic:
  - name: "Mythic Trait Name"
    desc: "When the creature is reduced to 0 hit points, it doesn't die. Instead, [trigger]. Until [condition], [effect]."

mythic_actions:
  - name: ""
    desc: "If [mythic trait] is active, the creature can use the options below as legendary actions."
  - name: "Mythic Action"
    desc: "Description."
```

---

## Image

```yaml
image: "[[portraits/creature-name.png]]"
token: "[[icons/creature-token.png]]"
```

Use Obsidian wikilink syntax. The `image` field renders above the stat block; `token` is for Initiative Tracker only.

---

## Full Skeleton — 5e Homebrew Creature

```yaml
---
statblock: inline
name: "Creature Name"
domain: shattered-sea
type: monster
summary: "One-line description."
source_count: 1
status: draft
visibility: private
tags: [monster]
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Creature Name

```statblock
layout: Basic 5e Layout
name: "Creature Name"
size: Medium
type: humanoid
alignment: neutral evil
ac: 13
hp: 45
hit_dice: "6d8 + 18"
speed: "30 ft."
stats: [16, 12, 16, 10, 10, 8]
saves:
  - Con: +5
skillsaves:
  - Perception: +2
senses: "darkvision 60 ft., passive Perception 12"
languages: "Common"
cr: 2
traits:
  - name: "Trait Name"
    desc: "Trait description."
actions:
  - name: Multiattack
    desc: "The creature makes two attacks."
  - name: "Weapon Attack"
    desc: "Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (1d8 + 3) slashing damage."
` ``

## Overview

## Appearance

## Behavior

## Lore
```

---

## Ability Description Wording Patterns

Use these exact phrasings in `desc:` values. WotC wording is load-bearing — deviating from it creates rules ambiguity.

### Attacks

**Melee weapon attack:**
```
Claws. Melee Weapon Attack: +7 to hit, reach 5 ft., one target. Hit: 13 (2d8 + 4) slashing damage.
```

**With a rider:**
```
Bite. Melee Weapon Attack: +9 to hit, reach 5 ft., one creature. Hit: 18 (3d8 + 5) piercing damage, and the target is grappled (escape DC 17). Until this grapple ends, the target is restrained, and the [name] can't bite another target.
```

**Ranged:**
```
Spine Volley. Ranged Weapon Attack: +6 to hit, range 30/120 ft., one target. Hit: 11 (2d6 + 4) piercing damage.
```

### Saving Throw Abilities

**Cone:**
```
Acid Breath (Recharge 5–6). The [name] exhales acid in a 30-foot cone. Each creature in that area must make a DC 14 Dexterity saving throw, taking 49 (11d8) acid damage on a failed save, or half as much damage on a successful one.
```

**Sphere:**
```
Spore Cloud (Recharge 6). The [name] releases a cloud of toxic spores in a 20-foot-radius sphere centered on itself. Each creature in that area must make a DC 15 Constitution saving throw, taking 35 (10d6) poison damage on a failed save, or half as much damage on a successful one. The area is heavily obscured until the end of the [name]'s next turn.
```

**Save-or-suffer (no damage):**
```
Paralyzing Gaze. The [name] targets one creature it can see within 30 feet. The target must succeed on a DC 14 Wisdom saving throw or be paralyzed until the end of the [name]'s next turn. The target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.
```

### Common Trait Patterns

**Magic resistance:**
```
Magic Resistance. The [name] has advantage on saving throws against spells and other magical effects.
```

**Pack tactics:**
```
Pack Tactics. The [name] has advantage on an attack roll against a creature if at least one of the [name]'s allies is within 5 feet of the creature and the ally isn't incapacitated.
```

**Regeneration:**
```
Regeneration. The [name] regains [X] hit points at the start of its turn. If the [name] takes [acid or fire] damage, this trait doesn't function at the start of the [name]'s next turn. The [name] dies only if it starts its turn with 0 hit points and doesn't regenerate.
```

**Damage threshold:**
```
Damage Threshold. The [name] has immunity to all damage unless it takes [X] or more damage from a single attack or spell, in which case it takes damage as normal.
```

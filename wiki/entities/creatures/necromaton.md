---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 20 undead lich. Artificer lich that transfers its soul into a construct of its own making — three stat block variants by chassis type. Permanently destroyed only when all construct bodies are eliminated."
created: 2026-05-15
updated: 2026-05-28
tags: [creature, undead, lich, bestiary, cr20]
sources: ["Inbox/Necromaton.md"]
confidence_level: high
cr: 20
aliases: ["Necromaton"]
---

# Necromaton

Three chassis variants. The soul anchors to a biological component housed inside the construct. Destroying all bodies ends the Necromaton permanently.

## Base Model (Ground)

```statblock
layout: Basic 5e Layout
name: "Necromaton (Base)"
size: Medium
type: undead
alignment: Any Alignment
ac: 19
hp: 153
hit_dice: 18d8 + 72
speed: "30 ft."
stats: [16, 18, 19, 20, 14, 15]
saves:
  - constitution: 10
  - intelligence: 11
skillsaves:
  - arcana: 11
  - investigation: 11
  - medicine: 8
damage_resistances: "Cold"
damage_immunities: "Necrotic, Poison; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks"
condition_immunities: "Charmed, Exhaustion, Frightened, Paralyzed, Poisoned"
senses: "Truesight 120 ft., Passive Perception 12"
languages: "The languages it knew in life"
cr: "20"
traits:
  - name: "Necromaton Phylactery"
    desc: "The Necromaton's body is its phylactery, anchored by a biological soul component. It is permanently destroyed only if all construct bodies are destroyed."
  - name: "Magic Resistance"
    desc: "Advantage on saving throws against spells and other magical effects."
  - name: "Soul Transference"
    desc: "Move its soul to another body: within 500 ft. (instant), within 10 miles (1 hour), within 60 miles (1 day), anywhere on the plane (1 week), other plane (1 week)."
spells:
  - "Spellcasting. INT-based (spell save DC 19, +11 to hit). Requires no material components."
  - "At will: Mage Hand, Mending, Alarm, Catapult, Magic Missile (4th level), Thunderwave (3rd level)"
  - "3/day each: Counterspell, Heat Metal, Hold Person, Magic Weapon, Scorching Ray, Shatter"
  - "2/day each: Fireball (5th level), Haste, Protection from Energy, Resilient Sphere"
  - "1/day each: Animate Objects (7th level), Arcane Hand (7th level), Wall of Force, Seeming"
actions:
  - name: "Arm Cannon"
    desc: "Ranged Weapon Attack: +9 to hit, range 150/600 ft. Hit: 17 (4d6+3) lightning damage."
  - name: "Arm Torch"
    desc: "Melee Weapon Attack: +9 to hit, reach 5 ft. Hit: 17 (4d6+3) bludgeoning plus 7 (2d6) fire damage."
legendary_actions:
  - name: "Missile"
    desc: "Cast Magic Missile at 4th level."
  - name: "Spell"
    desc: "Cast a non-damaging spell."
  - name: "Arm Attack"
    desc: "Make one Arm Cannon or Arm Torch attack."
  - name: "Propulsed Backstep"
    desc: "Move up to speed without provoking opportunity attacks."
```

**Flying Model:** Small chassis. AC 17, HP 135, Speed 30 ft./Fly 60 ft. (hover). DEX +5. Arm Cannon: +11 to hit, 19 (4d6+5) lightning. Sniper trait: no disadvantage at long range, +1d6 damage when no creatures within 5 feet.

**Bulldozer Model:** Large chassis. AC 21, HP 171, Speed 50 ft./Burrow 30 ft. STR +5. Arm Torch: +11 to hit, 19 (4d8+5) bludgeoning. Charge trait: extra 9 (2d8) bludgeoning and prone if moved 20+ feet straight toward target.

## Lore

An artificer who achieved lichdom by building a construct body and transferring their soul into it using a biological anchor — typically a preserved organ. They can build and inhabit multiple construct bodies simultaneously. Necromatons must constantly maintain and replace construct bodies as the biological components inside decay.

*Source: Pointy Hat*

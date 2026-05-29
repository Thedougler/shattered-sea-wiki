---
title: Necromaton
type: monster
publish: false
created: 2026-05-15
updated: 2026-05-15
summary: A Pointy Hat artificer lich that transfers its soul into a construct of its own making — it can possess multiple construct bodies and has three stat block variants by chassis type.
tags:
  - creature
  - undead
  - lich
  - bestiary
campaign: shattered-sea
audience: dm
subtype: monster
confidence_level: high
aliases:
  - Necromaton
sources:
  - Homebrew
  - Pointy Hat
cr: 20
creature_type: undead
cssclasses:
  - wiki-monster
relationships:
  - relation: listed_in
    target: Bestiary
---

# Necromaton

Three chassis variants. The soul anchors to a biological component (an organ, typically) housed inside the construct. Destroying all bodies ends the Necromaton permanently.

---

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
  - sleight_of_hand: 10
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
  - name: "Turn Resistance"
    desc: "Advantage on saving throws against any effect that turns undead."
  - name: "Inventory"
    desc: "Always aware of the exact location of all its phylactery bodies."
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

---

## Flying Model

Small chassis. AC 17, HP 135 (18d6+72), Speed 30 ft. / Fly 60 ft. (hover). STR 16, DEX 20 (+5), CON 19, INT 20, WIS 14, CHA 15. Arm Cannon: +11 to hit, 19 (4d6+5) lightning. Additional trait: **Sniper** — no disadvantage at long range; +1d6 damage when no creatures within 5 feet.

## Bulldozer Model

Large chassis. AC 21, HP 171 (18d10+72), Speed 50 ft. / Burrow 30 ft. STR 20 (+5), DEX 18, CON 19, INT 20, WIS 14, CHA 15. Arm Torch: +11 to hit, 19 (4d8+5) bludgeoning. Additional trait: **Charge** — if moves 20+ feet straight toward target before hitting with Arm Torch, target takes extra 9 (2d8) and must succeed DC 19 STR or be knocked prone.

---

## Lair Actions

On initiative count 20:
- Extend necromantic energy to constructs within 90 ft.: +1d8 necrotic damage on attacks until count 20 next round.
- Shock one construct within 60 ft.: doubled movement and two actions/reactions until count 20 next round.
- Grant arcane gifts to constructs within 30 ft.: can use action to cast Mending (heal 2d6) until count 20 next round.

---

## Lore

An artificer who achieved lichdom by building a construct body and transferring their soul into it using a biological anchor — typically a preserved organ. They can build and inhabit multiple construct bodies simultaneously, with the soul moving between them. The biological component is the true phylactery; the metal body is just a vessel. Necromatons must constantly maintain and replace construct bodies as the biological components inside decay.

---

## Source

- [[raw/ingested/Pointy Hat The Necromaton|Pointy Hat — The Necromaton]]

---
title: Death March
type: monster
publish: false
created: 2026-05-15
updated: 2026-05-15
summary: A Pointy Hat fighter lich whose phylacteries are the undead corpses of warriors it has slain and conscripted — it must keep hunting worthy opponents to replace decaying anchors.
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
  - Death March
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

# Death March

```statblock
layout: Basic 5e Layout
name: "Death March"
size: Medium
type: undead
alignment: Any Alignment
ac: 20
hp: 199
hit_dice: 21d10 + 84
speed: "40 ft."
stats: [22, 18, 22, 16, 11, 15]
saves:
  - strength: 12
  - constitution: 12
skillsaves:
  - athletics: 12
  - insight: 9
  - intimidation: 8
  - perception: 6
damage_resistances: "Cold, Necrotic"
damage_immunities: "Poison; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks"
condition_immunities: "Charmed, Exhaustion, Frightened, Paralyzed, Poisoned"
senses: "Darkvision 120 ft., Passive Perception 15"
languages: "The languages it knew in life"
cr: "20"
traits:
  - name: "Action Surge (3/Day)"
    desc: "Take an additional action. Deals +6 damage if the action is an attack action. Regain one use on a killing blow."
  - name: "Army of Phylacteries"
    desc: "If destroyed, the Death March instantly possesses the nearest phylactery within 300 feet. If none are within range, it takes 1d8 days to reach the closest one."
  - name: "Artillerist"
    desc: "Ignores reload property and ammo requirements on all ranged weapons."
  - name: "Indomitable (3/Day)"
    desc: "Reroll a failed saving throw. Regain one use on a killing blow."
  - name: "Legendary Resistance (3/Day)"
    desc: "If the Death March fails a saving throw, it can choose to succeed instead."
  - name: "Turn Resistance"
    desc: "Advantage on saving throws against any effect that turns undead."
  - name: "Walking Arsenal"
    desc: "Change weapons as a free action. Can wield a two-handed weapon while also using a shield."
  - name: "Ways of War"
    desc: "After each long rest, choose three fighting styles to have active."
actions:
  - name: "Multiattack"
    desc: "Four weapon attacks."
  - name: "Maul"
    desc: "Melee Weapon Attack: +12 to hit, reach 5 ft. Hit: 13 (2d6+6) bludgeoning plus 7 (2d6) necrotic damage."
  - name: "Rapier"
    desc: "Melee Weapon Attack: +12 to hit, reach 5 ft. Hit: 10 (1d8+6) piercing plus 7 (2d6) necrotic damage."
  - name: "Heavy Crossbow"
    desc: "Ranged Weapon Attack: +12 to hit, range 100/400 ft. Hit: 10 (1d8+6) piercing plus 7 (2d6) necrotic damage."
  - name: "Second in Command (Bonus Action)"
    desc: "Empower one phylactery within 300 feet: it gains 5 (1d10) temp HP and +3 to attack and damage rolls until the start of the Death March's next turn."
  - name: "Second Wind (3/Day, Bonus Action)"
    desc: "Regain 1d10+20 HP. Regain one use on a killing blow."
legendary_actions:
  - name: "Attack"
    desc: "Make one weapon attack."
  - name: "Riposte"
    desc: "After a creature misses the Death March with an attack, make one weapon attack against that creature with advantage."
  - name: "Maneuver (Costs 2 Actions)"
    desc: "Move up to half speed without provoking opportunity attacks."
```

---

## Lore

A fighter lich that achieves undeath by slaying the greatest warriors it can find and resurrecting them as undead phylacteries. The phylactery army decays over time; the Death March must constantly hunt new worthy opponents to conscript. It is perpetually at war by necessity, not choice.

---

## Source

- [[raw/ingested/Pointy Hat The Death March|Pointy Hat — The Death March]]

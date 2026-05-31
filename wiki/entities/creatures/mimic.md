---
type: monster
subtype: monster
campaign: shattered-sea
status: unknown
audience: players
publish: true
summary: CR 2 shapechanger monstrosity; disguises itself as mundane objects and grapples prey with adhesive pseudopods.
created: 2026-04-25
updated: 2026-05-31
tags: []
sources:
  - XMM
confidence_level: high
aliases:
  - Mimic
cha: 8
con: 15
cr: 2
creature_type: monstrosity
dex: 12
environment: underdark, urban
int: 5
page: 212
statblock: inline
str: 17
wis: 13
---

# Mimic

```statblock
layout: Basic 5e Layout
name: "Mimic"
size: Medium
type: monstrosity
alignment: Neutral
ac: 12
hp: 58
hit_dice: 9d8 + 18
speed: "20 ft."
stats: [17, 12, 15, 5, 13, 8]
skillsaves:
  - stealth: 5
damage_immunities: "acid"
condition_immunities: "prone"
senses: "Darkvision 60 ft., Passive Perception 11"
languages: "—"
cr: "2"
traits:
  - name: "Adhesive (Object Form Only)"
    desc: "The mimic adheres to anything that touches it. A Huge or smaller creature adhered to the mimic has the Grappled condition (escape DC 13). Ability checks to escape this grapple have Disadvantage."
actions:
  - name: "Bite"
    desc: "Melee Weapon Attack: +5 to hit (with Advantage if the target is Grappled by the mimic), reach 5 ft. Hit: 7 (1d8 + 3) Piercing damage, or 12 (2d8 + 3) Piercing damage if the target is Grappled by the mimic, plus 4 (1d8) Acid damage."
  - name: "Pseudopod"
    desc: "Melee Weapon Attack: +5 to hit, reach 5 ft. Hit: 7 (1d8 + 3) Bludgeoning damage plus 4 (1d8) Acid damage. If the target is a Large or smaller creature, it has the Grappled condition (escape DC 13). Ability checks to escape this grapple have Disadvantage."
bonus_actions:
  - name: "Shape-Shift"
    desc: "The mimic shape-shifts to resemble a Medium or Small object while retaining its game statistics, or it returns to its true blob form. Any equipment it is wearing or carrying isn't transformed."
```

## Habitat

Shape-shifting ambush predator found in urban ruins and sealed vaults. Looks like furniture, a chest, a door, or any other Medium-or-smaller object until contact triggers Adhesive.

## Related

- [[animated-armor|Animated Armor]]
---
type: monster
subtype: monster
campaign: shattered-sea
status: unknown
audience: dm
publish: false
summary: CR 1/2 fungal plant that explodes on death, releasing spores that infect creatures and reanimate their corpses as tiny gas spore fungi.
created: 2026-04-25
updated: 2026-05-31

sources:
  - XMM
confidence_level: high
aliases:
  - Gas Spore Fungus
cha: 1
con: 3
cr: 1/2
creature_type: plant
dex: 1
environment: underdark
int: 1
page: 125
statblock: inline
str: 5
wis: 1
tags:
  - combat
---

# Gas Spore Fungus

```statblock
layout: Basic 5e Layout
name: "Gas Spore Fungus"
size: Large
type: plant
alignment: Unaligned
ac: 8
hp: 13
hit_dice: 9d10 - 36
speed: "5 ft., Fly 10 ft. (hover)"
stats: [5, 1, 3, 1, 1, 1]
damage_immunities: "poison"
condition_immunities: "blinded, charmed, deafened, frightened, paralyzed, poisoned, prone"
senses: "Blindsight 30 ft., Passive Perception 5"
languages: "—"
cr: "1/2"
traits:
  - name: "Death Burst"
    desc: "DC 10 Constitution saving throw (each creature in a 20-foot emanation when the gas spore dies). On a failed save, the target takes 10 (3d6) Poison damage and has the Poisoned condition for 1d12 hours. Unless the Poisoned condition is removed, the target dies at the end of that time and sprouts 2d4 Tiny Gas Spore Fungi (each with 1 Hit Point). After 2d6 days, they become Large and have 13 Hit Points."
actions:
  - name: "Tendril"
    desc: "Melee Weapon Attack: +0 to hit, reach 5 ft. Hit: 3 (1d6) Poison damage, and the target has the Poisoned condition until the end of its next turn."
```

## Related

- [[myconid-adult|Myconid Adult]]
- [[myconid-sovereign|Myconid Sovereign]]

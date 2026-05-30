---
title: Myconid Adult
type: monster
publish: false
created: '2026-04-25'
updated: 2026-05-05
summary: CR 1/2 fungal plant creature. Communicates via spores and can merge consciousnesses in a Rapport circle.
tags:
- creature
- plant
subtype: monster
confidence_level: high
sources: XMM
cha: 7
con: 12
cr: 1/2
creature_type: plant
cssclasses:
- wiki-monster
dex: 10
environment: underdark
int: 10
page: 223
statblock: inline
str: 10
wis: 13
---

# Myconid Adult

```statblock
layout: Basic 5e Layout
name: "Myconid Adult"
size: Medium
type: plant
alignment: Lawful Neutral
ac: 12
hp: 16
hit_dice: 3d8 + 3
speed: "20 ft."
stats: [10, 10, 12, 10, 13, 7]
senses: "Darkvision 120 ft., Passive Perception 11"
languages: "telepathy 240 ft."
cr: "1/2"
traits:
  - name: "Sun Sickness"
    desc: "While in sunlight, the myconid has Disadvantage|XPHB on D20 Test|XPHB|D20 Tests. The myconid dies if it spends more than 1 hour in sunlight."
actions:
  - name: "Slam"
    desc: "Melee Weapon Attack: +2 to hit, reach 5 ft. Hit: 4 (1d8) Bludgeoning damage plus 3 (1d6) Poison damage."
  - name: "Pacifying Spores (1/Day)"
    desc: "con 11, one creature the myconid can see within 10 feet. {@actSaveFail} The target has the Stunned|XPHB condition and repeats the save at the end of each of its turns, ending the effect on itself on a success. After 1 minute, it succeeds automatically."
  - name: "Rapport Spores"
    desc: "The myconid expels spores in a 30-foot Emanation [Area of Effect]|XPHB|Emanation originating from itself. Creatures in that area with an Intelligence score of 2 or higher that aren't Constructs, Elementals, or Undead gain telepathy with a range of 30 feet for 1 hour."
```
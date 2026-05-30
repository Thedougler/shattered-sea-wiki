---
title: Harpy
type: monster
publish: true
created: '2026-04-25'
updated: '2026-05-03'
summary: Public statblock reference for Harpy, a CR 1 monstrosity in the Shattered
  Sea bestiary.
tags:
- creature
- monstrosity
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Harpy
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: habitat
  target: Ashwall Islands
- relation: habitat
  target: The Tail
- relation: habitat
  target: Meth-Var
cha: 13
con: 12
cr: 1
creature_type: monstrosity
cssclasses:
- wiki-monster
dex: 13
environment: coastal, forest, hill, mountain
int: 7
page: 164
statblock: inline
str: 12
wis: 10
---

# Harpy

```statblock
layout: Basic 5e Layout
name: "Harpy"
size: Medium
type: monstrosity
alignment: Chaotic Evil
ac: 11
hp: 38
hit_dice: 7d8 + 7
speed: "20 ft., Fly 40 ft."
stats: [12, 13, 12, 7, 10, 13]
senses: "Passive Perception 10"
languages: "Common"
cr: "1"
actions:
  - name: "Claw"
    desc: "Melee Weapon Attack: +3 to hit, reach 5 ft. Hit: 6 (2d4 + 1) Slashing damage."
  - name: "Luring Song"
    desc: "The harpy sings a magical melody, which lasts until the harpy's Concentration|XPHB ends on it. wis 11, each Humanoid and Giant in a 300-foot Emanation [Area of Effect]|XPHB|Emanation originating from the harpy when the song starts. {@actSaveFail} The target has the Charmed|XPHB condition until the song ends and repeats the save at the end of each of its turns. While Charmed|XPHB, the target has the Incapacitated|XPHB condition and ignores the Luring Song of other harpies. If the target is more than 5 feet from the harpy, the target moves on its turn toward the harpy by the most direct route, trying to get within 5 feet of the harpy. It doesn't avoid Opportunity Attack|XPHB|Opportunity Attacks; however, before moving into damaging terrain (such as lava or a pit) and whenever it takes damage from a source other than the harpy, the target repeats the save. {@actSaveSuccess} The target is immune to this harpy's Luring Song for 24 hours."
```
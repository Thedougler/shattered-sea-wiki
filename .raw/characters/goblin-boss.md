---
title: Goblin Boss
type: monster
publish: false
created: '2026-04-25'
updated: 2026-05-05
summary: CR 1 fey goblin leader. Commands goblin minions and uses the Redirect Attack reaction to avoid harm.
tags:
- creature
- fey
subtype: monster
confidence_level: high
sources: XMM
cha: 10
con: 10
cr: 1
creature_type: fey
cssclasses:
- wiki-monster
dex: 15
environment: forest, grassland, hill, planar, acheron, planar, feywild, underdark
int: 10
page: 143
statblock: inline
str: 10
wis: 8
---

# Goblin Boss

```statblock
layout: Basic 5e Layout
name: "Goblin Boss"
size: Small
type: fey
alignment: Chaotic Neutral
ac: 17
hp: 21
hit_dice: 6d6
speed: "30 ft."
stats: [10, 15, 10, 10, 8, 10]
skillsaves:
  - stealth: 6
senses: "Darkvision 60 ft., Passive Perception 9"
languages: "Common, Goblin"
cr: "1"
actions:
  - name: "Multiattack"
    desc: "The goblin makes two attacks, using Scimitar or Shortbow in any combination."
  - name: "Scimitar"
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft. Hit: 5 (1d6 + 2) Slashing damage, plus 2 (1d4) Slashing damage if the attack roll had Advantage|XPHB."
  - name: "Shortbow"
    desc: "Ranged Weapon Attack: +4 to hit, range 80/320 ft. Hit: 5 (1d6 + 2) Piercing damage, plus 2 (1d4) Piercing damage if the attack roll had Advantage|XPHB."
bonus_actions:
  - name: "Nimble Escape"
    desc: "The goblin takes the Disengage|XPHB or Hide|XPHB action."
reactions:
  - name: "Redirect Attack"
    desc: "{@actTrigger} A creature the goblin can see makes an attack roll against it. {@actResponse} The goblin chooses a Small or Medium ally within 5 feet of itself. The goblin and that ally swap places, and the ally becomes the target of the attack instead."
```
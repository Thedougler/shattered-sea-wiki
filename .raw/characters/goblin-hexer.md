---
title: Goblin Hexer
type: monster
publish: false
created: 2026-04-25
updated: 2026-05-05
summary: Spellcasting goblin variant that curses and debilitates enemies with fey magic.
tags:
- creature
- fey
campaign: shattered-sea
subtype: monster
confidence_level: high
sources: XMM
cha: 10
con: 12
cr: 3
creature_type: fey
cssclasses:
- wiki-monster
dex: 16
environment: forest, grassland, hill, planar, acheron, planar, feywild, underdark
int: 16
page: 143
statblock: inline
str: 8
wis: 10
---

# Goblin Hexer

```statblock
layout: Basic 5e Layout
name: "Goblin Hexer"
size: Small
type: fey
alignment: Chaotic Neutral
ac: 13
hp: 45
hit_dice: 10d6 + 10
speed: "30 ft."
stats: [8, 16, 12, 16, 10, 10]
skillsaves:
  - sleight of hand: 5
  - stealth: 7
senses: "Darkvision 60 ft., Passive Perception 10"
languages: "Common, Goblin"
cr: "3"
actions:
  - name: "Multiattack"
    desc: "The goblin makes two Hex Stick attacks. It can replace one attack with a use of Spellcasting."
  - name: "Hex Stick"
    desc: "m,r +5 to hit, reach 5 ft. or range 60 ft. Hit: 12 (2d8 + 3) Psychic damage."
reactions:
  - name: "Jinx"
    desc: "{@actTrigger} A creature the goblin can see hits it with an attack roll. dwis 13, the triggering creature. {@actSaveFail} The attack misses instead."
spells:
  - "The goblin casts one of the following spells, using Intelligence as the spellcasting ability (spell save 13):"
  - "At will: Minor Illusion|XPHB"
  - "1e: Blindness/Deafness|XPHB, Faerie Fire|XPHB, Grease|XPHB"
```
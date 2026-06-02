---
type: monster
subtype: monster
campaign: shattered-sea
status: unknown
audience: dm
publish: false
summary: CR 3 fey goblin spellcaster; curses and debilitates enemies with fey magic, and can negate a hit against it once per round with Jinx.
created: 2026-04-25
updated: 2026-06-01

sources:
  - XMM
confidence_level: high
aliases:
  - Goblin Hexer
cha: 10
con: 12
cr: 3
creature_type: fey
dex: 16
environment: forest, grassland, hill, planar, underdark
int: 16
page: 143
statblock: inline
str: 8
wis: 10
tags:
  - combat
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
    desc: "Melee or Ranged Spell Attack: +5 to hit, reach 5 ft. or range 60 ft. Hit: 12 (2d8 + 3) Psychic damage."
reactions:
  - name: "Jinx"
    desc: "Trigger: A creature the goblin can see hits it with an attack roll. The triggering creature makes a DC 13 Wisdom saving throw. On a failed save, the attack misses instead."
spells:
  - "INT-based spellcasting (spell save DC 13). At will: Minor Illusion. 1/day each: Blindness/Deafness, Faerie Fire, Grease."
```

## Related

- [[goblin-boss|Goblin Boss]]
- [[goblin-warrior|Goblin Warrior]]
- [[goblin-minion|Goblin Minion]]
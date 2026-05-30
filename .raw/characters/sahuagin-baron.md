---
title: Sahuagin Baron
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Sahuagin Baron, a CR 5 fiend in the Shattered Sea bestiary.
tags:
- creature
- fiend
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Sahuagin Baron
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: hunts_in
  target: The Drowned Maw
cha: 17
con: 16
cr: 5
creature_type: fiend
cssclasses:
- wiki-monster
dex: 15
environment: coastal, underwater
int: 14
page: 265
statblock: inline
str: 19
wis: 13
---

# Sahuagin Baron

```statblock
layout: Basic 5e Layout
name: "Sahuagin Baron"
size: Large
type: fiend
alignment: Lawful Evil
ac: 16
hp: 76
hit_dice: 9d10 + 27
speed: "30 ft., Swim 50 ft."
stats: [19, 15, 16, 14, 13, 17]
saves:
  - dexterity: 5
  - constitution: 6
  - wisdom: 4
skillsaves:
  - perception: 7
damage_resistances: "acid, cold"
senses: "Darkvision 120 ft., Passive Perception 17"
languages: "Sahuagin"
cr: "5"
traits:
  - name: "Blood Frenzy"
    desc: "The sahuagin has Advantage|XPHB on attack rolls against any creature that doesn't have all its Hit Points|XPHB."
  - name: "Limited Amphibiousness"
    desc: "The sahuagin can breathe air and water, but it must be submerged at least once every 4 hours to avoid suffocating outside water."
  - name: "Shark Telepathy"
    desc: "The sahuagin can magically control sharks within 120 feet of itself, using a special telepathy."
actions:
  - name: "Multiattack"
    desc: "The sahuagin makes three Trident attacks."
  - name: "Trident"
    desc: "m,r +7 to hit, reach 5 ft. or range 20/60 ft. Hit: 13 (2d8 + 4) Piercing damage."
reactions:
  - name: "Fiendish Blood"
    desc: "{@actTrigger} The sahuagin takes Piercing or Slashing damage. dcon 14, each creature of the sahuagin's choice in a 5-foot Emanation [Area of Effect]|XPHB|Emanation originating from the sahuagin. {@actSaveFail} 10 (3d6) Acid damage, and the target is cursed until it finishes a Short Rest|XPHB|Short or Long Rest|XPHB. While cursed, the target can't benefit from the Invisible|XPHB condition, its Speed|XPHB decreases by 10 feet, and all Fiends within 120 feet of the target can sense its location regardless of interposing obstacles."
```
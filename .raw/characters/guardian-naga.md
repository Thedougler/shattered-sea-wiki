---
title: Guardian Naga
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Guardian Naga, a CR 10 celestial in the Shattered Sea bestiary.
tags:
- creature
- celestial
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Guardian Naga
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: rumored_in
  target: Antheri Ruins
cha: 18
con: 16
cr: 10
creature_type: celestial
cssclasses:
- wiki-monster
dex: 18
environment: desert, forest, planar, upper
int: 16
page: 161
statblock: inline
str: 19
wis: 19
---

# Guardian Naga

```statblock
layout: Basic 5e Layout
name: "Guardian Naga"
size: Large
type: celestial
alignment: Lawful Good
ac: 18
hp: 136
hit_dice: 16d10 + 48
speed: "40 ft., Climb 40 ft., Swim 40 ft."
stats: [19, 18, 16, 16, 19, 18]
saves:
  - dexterity: 8
  - constitution: 7
  - intelligence: 7
  - wisdom: 8
  - charisma: 8
skillsaves:
  - arcana: 11
  - history: 11
  - religion: 11
damage_immunities: "poison"
condition_immunities: "charmed, paralyzed, poisoned, restrained"
senses: "Darkvision 60 ft., Passive Perception 14"
languages: "Celestial, Common"
cr: "10"
traits:
  - name: "Celestial Restoration"
    desc: "If the naga dies, it returns to life in 1d6 days and regains all its Hit Points|XPHB unless Dispel Evil and Good|XPHB is cast on its remains."
actions:
  - name: "Multiattack"
    desc: "The naga makes two Bite attacks. It can replace any attack with a use of Poisonous Spittle."
  - name: "Bite"
    desc: "Melee Weapon Attack: +8 to hit, reach 10 ft. Hit: 17 (2d12 + 4) Piercing damage plus 22 (4d10) Poison damage."
  - name: "Poisonous Spittle"
    desc: "con 16, one creature the naga can see within 60 feet. {@actSaveFail} 31 (7d8) Poison damage, and the target has the Blinded|XPHB condition until the start of the naga's next turn. {@actSaveSuccess} Half damage only."
spells:
  - "The naga casts one of the following spells, requiring no Somatic or Material components and using Wisdom as the spellcasting ability (spell save 16):"
  - "At will: Thaumaturgy|XPHB"
  - "1e: Clairvoyance|XPHB, Cure Wounds|XPHB (level 6 version), Flame Strike|XPHB (level 6 version), Geas|XPHB, True Seeing|XPHB"
```
---
title: Pirate
type: monster
publish: true
created: '2026-04-25'
updated: '2026-05-03'
summary: Public statblock reference for Pirate, a CR 1 humanoid in the Shattered Sea
  bestiary.
tags:
- creature
- humanoid
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Pirate
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: active_in
  target: The Central Strait
- relation: active_in
  target: The Midchain
- relation: active_in
  target: Kalowe
- relation: active_in
  target: The Drowned Maw
- relation: active_in
  target: The Galewall
cha: 14
con: 12
cr: 1
creature_type: humanoid
cssclasses:
- wiki-monster
dex: 16
environment: any
int: 8
page: 241
statblock: inline
str: 10
wis: 12
---

# Pirate

```statblock
layout: Basic 5e Layout
name: "Pirate"
size: Small
type: humanoid
alignment: Neutral
ac: 14
hp: 33
hit_dice: 6d8 + 6
speed: "30 ft."
stats: [10, 16, 12, 8, 12, 14]
saves:
  - dexterity: 5
  - charisma: 4
senses: "Passive Perception 11"
languages: "Common plus one other language"
cr: "1"
actions:
  - name: "Multiattack"
    desc: "The pirate makes two Dagger attacks. It can replace one attack with a use of Enthralling Panache."
  - name: "Dagger"
    desc: "m,r +5 to hit, reach 5 ft. or range 20/60 ft. Hit: 5 (1d4 + 3) Piercing damage."
  - name: "Enthralling Panache"
    desc: "wis 12, one creature the pirate can see within 30 feet. {@actSaveFail} The target has the Charmed|XPHB condition until the start of the pirate's next turn."
```
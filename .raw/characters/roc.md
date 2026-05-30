---
title: Roc
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Roc, a CR 11 monstrosity in the Shattered Sea bestiary.
tags:
- creature
- monstrosity
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Roc
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: habitat
  target: The Galewall
- relation: habitat
  target: The High Eyrie
cha: 9
con: 20
cr: 11
creature_type: monstrosity
cssclasses:
- wiki-monster
dex: 10
environment: arctic, coastal, desert, hill, mountain
int: 3
page: 261
statblock: inline
str: 28
wis: 10
---

# Roc

```statblock
layout: Basic 5e Layout
name: "Roc"
size: Gargantuan
type: monstrosity
alignment: Unaligned
ac: 15
hp: 248
hit_dice: 16d20 + 80
speed: "20 ft., Fly 120 ft."
stats: [28, 10, 20, 3, 10, 9]
saves:
  - dexterity: 4
  - wisdom: 4
skillsaves:
  - perception: 8
senses: "Passive Perception 18"
languages: "—"
cr: "11"
actions:
  - name: "Multiattack"
    desc: "The roc makes two Beak attacks. It can replace one attack with a Talons attack."
  - name: "Beak"
    desc: "Melee Weapon Attack: +13 to hit, reach 10 ft. Hit: 28 (3d12 + 9) Piercing damage."
  - name: "Talons"
    desc: "Melee Weapon Attack: +13 to hit, reach 5 ft. Hit: 23 (4d6 + 9) Slashing damage. If the target is a Huge or smaller creature, it has the Grappled|XPHB condition (escape 19) from both talons, and it has the Restrained|XPHB condition until the grapple ends."
bonus_actions:
  - name: "Swoop 5"
    desc: "If the roc has a creature Grappled|XPHB, the roc flies up to half its Fly Speed|XPHB without provoking Opportunity Attack|XPHB|Opportunity Attacks and drops that creature."
```
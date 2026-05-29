---

title: Pirate Admiral
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Pirate Admiral, a CR 12 humanoid in the Shattered Sea bestiary.
tags:
- creature
- humanoid
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Pirate Admiral
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: active_in
  target: The Galewall
- relation: active_in
  target: The Tail
- relation: active_in
  target: The Central Strait
cha: 19
con: 14
cr: 12
creature_type: humanoid
cssclasses:
- wiki-monster
dex: 22
environment: any
int: 12
page: 242
statblock: inline
str: 14
wis: 14
---

# [[pirate]] Admiral

```statblock
layout: Basic 5e Layout
name: "Pirate Admiral"
size: Small
type: humanoid
alignment: Neutral
ac: 20
hp: 182
hit_dice: 28d8 + 56
speed: "30 ft."
stats: [14, 22, 14, 12, 14, 19]
saves:
  - strength: 6
  - dexterity: 10
  - wisdom: 6
  - charisma: 8
skillsaves:
  - acrobatics: 10
  - athletics: 6
  - perception: 6
senses: "Passive Perception 16"
languages: "Common plus one other language"
cr: "12"
actions:
  - name: "Multiattack"
    desc: "The pirate makes three attacks, using Scimitar or Pistol in any combination."
  - name: "Scimitar"
    desc: "Melee Weapon Attack: +10 to hit, reach 5 ft. Hit: 16 (3d6 + 6) Slashing damage plus 7 (2d6) Poison damage, and the target suffers one of the following effects of the pirate's choice: Awestruck: The target has the Charmed|XPHB condition until the start of the pirate's next turn. Poison: The target has the Poisoned|XPHB condition until the start of the pirate's next turn."
  - name: "Pistol"
    desc: "Ranged Weapon Attack: +10 to hit, range 30/90 ft. Hit: 28 (4d10 + 6) Piercing damage."
bonus_actions:
  - name: "Rally (1/Day)"
    desc: "The pirate chooses up to three other creatures it can see within 30 feet. Until the start of the pirate's next turn, the targets have Advantage|XPHB on attack rolls and saving throws."
reactions:
  - name: "Defensive Stance"
    desc: "{@actTrigger} The pirate is hit by a melee attack roll while holding a weapon. {@actResponse} The pirate adds 4 to its AC against melee attack rolls (including the triggering attack) until the start of its next turn, possibly causing the attacks to miss."
```
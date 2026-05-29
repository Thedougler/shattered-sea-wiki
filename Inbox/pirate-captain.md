---

title: Pirate Captain
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Pirate Captain, a CR 6 humanoid in the Shattered Sea bestiary.
tags:
- creature
- humanoid
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: high
aliases:
- Pirate Captain
sources:
- XMM
relationships:
- relation: listed_in
  target: Bestiary
- relation: active_in
  target: The Central Strait
- relation: active_in
  target: The Shelfworks
- relation: active_in
  target: The Drowned Maw
- relation: active_in
  target: The Outer Reach
- relation: active_in
  target: The Tail
- relation: active_in
  target: Kalowe
cha: 17
con: 14
cr: 6
creature_type: humanoid
cssclasses:
- wiki-monster
dex: 18
environment: any
int: 10
page: 242
statblock: inline
str: 10
wis: 14
---

# [[pirate]] Captain

```statblock
layout: Basic 5e Layout
name: "Pirate Captain"
size: Small
type: humanoid
alignment: Neutral
ac: 17
hp: 84
hit_dice: 13d8 + 26
speed: "30 ft."
stats: [10, 18, 14, 10, 14, 17]
saves:
  - strength: 3
  - dexterity: 7
  - wisdom: 5
  - charisma: 6
skillsaves:
  - acrobatics: 7
  - perception: 5
senses: "Passive Perception 15"
languages: "Common plus one other language"
cr: "6"
actions:
  - name: "Multiattack"
    desc: "The pirate makes three attacks, using Rapier or Pistol in any combination."
  - name: "Rapier"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 13 (2d8 + 4) Piercing damage, and the pirate has Advantage|XPHB on the next attack roll it makes before the end of this turn."
  - name: "Pistol"
    desc: "Ranged Weapon Attack: +7 to hit, range 30/90 ft. Hit: 15 (2d10 + 4) Piercing damage."
bonus_actions:
  - name: "Captain's Charm"
    desc: "wis 14, one creature the pirate can see within 30 feet. {@actSaveFail} The target has the Charmed|XPHB condition until the start of the pirate's next turn."
reactions:
  - name: "Riposte"
    desc: "{@actTrigger} The pirate is hit by a melee attack roll while holding a weapon. {@actResponse} The pirate adds 3 to its AC against that attack, possibly causing it to miss. On a miss, the pirate makes one Rapier attack against the triggering creature if within range."
```
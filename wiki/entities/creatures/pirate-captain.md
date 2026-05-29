---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "CR 6 humanoid pirate captain. Rapier and pistol multiattack, Captain's Charm, Riposte reaction."
created: 2026-04-25
updated: 2026-05-28
tags: [creature, humanoid, bestiary, cr6]
sources: ["Inbox/pirate-captain.md"]
cr: 6
confidence_level: high
---

# Pirate Captain

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
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 13 (2d8 + 4) Piercing damage, and the pirate has Advantage on the next attack roll it makes before the end of this turn."
  - name: "Pistol"
    desc: "Ranged Weapon Attack: +7 to hit, range 30/90 ft. Hit: 15 (2d10 + 4) Piercing damage."
bonus_actions:
  - name: "Captain's Charm"
    desc: "DC 14 Wisdom save, one creature within 30 feet. On a failed save, the target has the Charmed condition until the start of the pirate's next turn."
reactions:
  - name: "Riposte"
    desc: "When the pirate is hit by a melee attack roll while holding a weapon, the pirate adds 3 to its AC against that attack, possibly causing it to miss. On a miss, the pirate makes one Rapier attack against the triggering creature if within range."
```

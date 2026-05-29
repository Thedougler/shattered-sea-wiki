---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "CR 1 humanoid pirate statblock. Charming, daggers-out, fights with panache."
created: 2026-04-25
updated: 2026-05-28
tags: [creature, humanoid, bestiary, cr1]
sources: ["Inbox/pirate.md"]
cr: 1
confidence_level: high
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
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft. Hit: 5 (1d4 + 3) Piercing damage."
  - name: "Enthralling Panache"
    desc: "DC 12 Wisdom save, one creature within 30 feet. On a failed save, the target has the Charmed condition until the start of the pirate's next turn."
```

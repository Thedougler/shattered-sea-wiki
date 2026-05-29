---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "CR 12 humanoid pirate admiral. Scimitar and pistol, Rally bonus action, Defensive Stance reaction."
created: 2026-04-25
updated: 2026-05-28
tags: [creature, humanoid, bestiary, cr12]
sources: ["Inbox/pirate-admiral.md"]
cr: 12
confidence_level: high
---

# Pirate Admiral

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
    desc: "Melee Weapon Attack: +10 to hit, reach 5 ft. Hit: 16 (3d6 + 6) Slashing damage plus 7 (2d6) Poison damage, and the target suffers one effect of the admiral's choice: Awestruck (Charmed until start of admiral's next turn) or Poison (Poisoned until start of admiral's next turn)."
  - name: "Pistol"
    desc: "Ranged Weapon Attack: +10 to hit, range 30/90 ft. Hit: 28 (4d10 + 6) Piercing damage."
bonus_actions:
  - name: "Rally (1/Day)"
    desc: "The pirate chooses up to three other creatures it can see within 30 feet. Until the start of the pirate's next turn, the targets have Advantage on attack rolls and saving throws."
reactions:
  - name: "Defensive Stance"
    desc: "When the pirate is hit by a melee attack roll while holding a weapon, the pirate adds 4 to its AC against melee attack rolls (including the triggering attack) until the start of its next turn."
```

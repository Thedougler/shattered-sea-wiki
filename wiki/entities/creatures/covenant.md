---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 20 undead lich. Warlock lich whose phylacteries are signed pact contracts — it reforms as long as any pact-holder still lives."
created: 2026-05-15
updated: 2026-05-28
tags: [creature, undead, lich, bestiary, cr20]
sources: ["Inbox/Covenant.md"]
cr: 20
confidence_level: high
aliases: ["Covenant"]
---

# Covenant

```statblock
layout: Basic 5e Layout
name: "Covenant"
size: Medium
type: undead
alignment: Any Alignment
ac: 18
hp: 300
hit_dice: 40d8 + 120
speed: "30 ft."
stats: [12, 17, 17, 18, 16, 20]
saves:
  - wisdom: 9
  - charisma: 11
skillsaves:
  - arcana: 10
  - deception: 11
  - persuasion: 17
damage_resistances: "Cold, Necrotic"
damage_immunities: "Poison, Radiant; Charmed, Exhaustion, Frightened, Paralyzed, Poisoned"
senses: "Truesight 120 ft., Passive Perception 13"
languages: "All languages"
cr: "20"
traits:
  - name: "Legendary Resistance (4/Day)"
    desc: "If the Covenant fails a saving throw, it can choose to succeed instead."
  - name: "Covenant Resurrection"
    desc: "If any pact-holder still lives, a destroyed Covenant reforms in 1d4 days beside its oldest surviving contract."
  - name: "Pact Mage"
    desc: "Once per turn, choose one active pact option: Pact of the Blade, Pact of the Chain, or Pact of the Tome."
spells:
  - "Spellcasting. CHA-based (spell save DC 19, +11 to hit). Requires no material components."
  - "At will: Mage Hand, True Strike"
  - "2/day each: Blight (5th level), Fly (5th level), Hallucinatory Terrain, Hold Person (5th level)"
  - "1/day each: Circle of Death, Mass Suggestion, Power Word Kill"
actions:
  - name: "Multiattack"
    desc: "Three Eldritch Blast attacks (can replace one with Hexblade if Blade pact active)."
  - name: "Eldritch Blast"
    desc: "Ranged Spell Attack: +11 to hit, range 120 ft. Hit: 31 (4d12+5) force damage. Choose one: push target 10 feet, pull target 10 feet, or deal double CHA modifier as bonus damage."
  - name: "Hexblade (Pact of the Blade only)"
    desc: "Melee Weapon Attack: +11 to hit, reach 5 ft. Hit: 10 (1d10+5) slashing plus 31 (4d12+5) force damage."
legendary_actions:
  - name: "Change Pact"
    desc: "Choose a new active pact option."
  - name: "Compelled Covenant"
    desc: "Cast Dominate Person (bypasses Charmed immunity on pact-holders)."
  - name: "Misty Step"
    desc: "Teleport up to 30 feet to an unoccupied space."
```

## Lore

A warlock who achieved lichdom through their pact. Each contract they convince mortals to sign becomes a phylactery — the physical document anchors the Covenant's existence. They make extraordinarily good deals, terms that seem too fair to refuse. They are, in the long run, collecting anchors.

*Source: Pointy Hat*

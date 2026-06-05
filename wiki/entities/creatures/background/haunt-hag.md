---
type: entity
subtype: monster
campaign: shattered-sea
status: unknown
audience: dm
publish: false
summary: CR 5 fey hag of fear and illusion; reads victims' deepest terrors and physically manifests as those fears — she runs encounters like a horror director.
created: 2026-05-15
updated: 2026-05-31
tags:
  - combat
  - homebrew
  - mystery
sources:
  - Homebrew
  - Pointy Hat
confidence_level: high
aliases:
  - Haunt Hag
cha: 10
con: 16
cr: 5
creature_type: fey
dex: 14
environment: forest, urban
int: 15
page: 0
statblock: inline
str: 9
wis: 18
---

# Haunt Hag

```statblock
layout: Basic 5e Layout
name: "Haunt Hag"
size: Medium
type: fey
alignment: Typically Neutral Evil
ac: 14
hp: 75
hit_dice: 10d8 + 30
speed: "30 ft., Fly 20 ft. (hover)"
stats: [9, 14, 16, 15, 18, 10]
skillsaves:
  - insight: 7
  - perception: 7
  - performance: 3
  - stealth: 5
damage_resistances: "Necrotic"
condition_immunities: "Frightened"
senses: "Darkvision 120 ft., Passive Perception 16"
languages: "Common, Infernal, Sylvan"
cr: "5"
traits:
  - name: "Darkness Affinity"
    desc: "Magical darkness does not impede the hag's Darkvision."
  - name: "Eye for Horror"
    desc: "Instantly knows the deepest fear of any creature that enters its lair."
spells:
  - "WIS-based spellcasting (spell save DC 15, +7 to hit). Requires no material components."
  - "At will: Dancing Lights, Hideous Laughter, Mage Hand, Silent Image"
  - "3/day each: Darkness, Invisibility, Moonbeam"
actions:
  - name: "Multiaction"
    desc: "Use any two of the following: Touch of Horror, Hands of Horror, See Fear, or Embody Fear."
  - name: "Touch of Horror"
    desc: "Melee Spell Attack: +7 to hit, reach 5 ft. Hit: 13 (2d8+4) Necrotic damage, plus 4 (1d8) additional if the hag was unseen by the target."
  - name: "Hands of Horror"
    desc: "Ranged Spell Attack: +7 to hit, range 60 ft. Hit: 9 (1d10+4) Necrotic damage."
  - name: "See Fear"
    desc: "Make an Insight check contested by the target's Deception. On success, learn the target's darkest fear."
  - name: "Embody Fear"
    desc: "Requires knowing the target's fear. Transform into the target's deepest fear. Gain Advantage on attacks. Target is Frightened of the hag. The hag reverts at the end of its next turn."
```

## Lair Actions (Initiative Count 20)

- **House of Horrors:** The lair takes the illusory form of a location embodying the target's deepest fear. The target is Frightened, its speed drops to 0, and attackers have Advantage against it.
- **Hide and Seek:** Teleport up to 60 feet within the lair and immediately take the Hide action.
- **Lights Out:** Fill the lair with magical darkness. Dispels automatically on the next lair action.

## Lore

A fey hag who hunts through fear rather than force. She reads the unique terror of each intruder the moment they enter her lair, then plays the encounter like theatre — slow, building dread punctuated by sudden shock. She transforms herself into the thing each victim fears most, making every fight intensely personal.

## Related

- [[gentle-hag|Gentle Hag]]

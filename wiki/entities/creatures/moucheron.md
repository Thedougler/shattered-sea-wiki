---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 8 fey mercenary from the Plane of Faerie that feeds exclusively on blood. Pays negotiated in bloodletting. Highly social when fed, vicious when starved. Active on Murrat; hires out of Kalowe."
created: 2026-05-15
updated: 2026-05-28
tags: [creature, fey, bestiary, cr8]
sources: ["Inbox/Moucheron.md"]
cr: 8
confidence_level: high
aliases: ["Moucheron"]
relationships:
  - "[[kalowe|Kalowe]] — primary Midchain hiring port"
  - "[[dravosi-crown|Dravosi Crown]] — classifies as hazardous wildlife"
  - "[[five-blades|Five Blades]] — known Moucheron mercenary group"
---

# Moucheron

![[Moucheron.webp|A mosquito-like fey mercenary with four blades and a blood-drawing proboscis]]

```statblock
layout: Basic 5e Layout
name: "Moucheron"
size: Small
type: fey
alignment: Any
ac: 16
hp: 130
hit_dice: 20d6 + 60
speed: "30 ft., fly 60 ft."
stats: [12, 19, 17, 14, 14, 13]
saves:
  - dexterity: 7
  - constitution: 6
skillsaves:
  - acrobatics: 7
  - perception: 5
senses: "Darkvision 60 ft., Passive Perception 15"
languages: "Common, Sylvan"
cr: "8"
traits:
  - name: "Magic Resistance"
    desc: "Advantage on saving throws against spells and other magical effects."
  - name: "Sanguivore — Satiated"
    desc: "If the Moucheron hit with its Stinger last turn: no opportunity attacks against it, and AC becomes 17."
  - name: "Sanguivore — Voracious"
    desc: "If the Moucheron did not hit with its Stinger last turn: +1 bonus to all attack and damage rolls."
actions:
  - name: "Multiattack"
    desc: "Four Fey Blade attacks. Can replace one with a Stinger attack."
  - name: "Fey Blade"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 14 (3d6+4) piercing damage."
  - name: "Stinger"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 11 (2d6+4) piercing damage."
  - name: "Feeding Frenzy (2/Day, Bonus Action)"
    desc: "After hitting a Bloodied creature with Stinger, gain both Satiated and Voracious benefits simultaneously until the end of next turn."
```

## Lore

Native to [[murrat|Murrat]] and the surrounding reef islands in the [[midchain|Midchain]]. Villages are built into cliff faces and canopy — each a separate kin-group running its own blood economy. Within the community, bloodletting is formal and consensual: it settles debts, pays for skilled work, and marks agreements.

Murrat itself is hostile to outsiders — island Moucherons attack anything that lands. The ones who leave and work as mercenaries in the wider Midchain are the same creature. They've just learned that fighting other people's wars pays better than hunting.

**Mercenary work:** Moucheron squads hire out of [[kalowe|Kalowe]] in groups of three to six. They are reliable — they don't break contracts, don't abandon clients under fire, and the feeding terms are stated upfront. The caveat is the bloodless job: if a fight doesn't materialize, the feeding clause still stands.

**Dravosi classification:** The [[dravosi-crown|Dravosi Crown]] classifies Moucherons alongside [[rattkin|Rattkin]] under species bounty in Crown territories, but files them separately as hazardous wildlife removal at a higher rate.

## Blood Requirements

**The clock — consecutive days without a full feed:**

| Days unfed | State | Behavior | Mechanical |
|---|---|---|---|
| 0 | Satiated | Fed today. Normal, sociable, professional. | Sanguivore — Satiated active. |
| 1 | Hungry | Irritable. Will ask for a willing draw. | Voracious active, Satiated lost. −0 |
| 2 | Difficult | Will feed on animals without asking. | −2 to all Charisma checks. |
| 3 | Desperate | Biology overrides contract. Will feed on any available creature. | Disadvantage on Wisdom saves. Advantage on attacks against bloodied creatures. |
| 4+ | Starving | Attacks to feed. Takes 1d8 necrotic per day. Dies at 0 HP. | All above plus 1d8 necrotic/day. |

> [!dm]
> The Five Blades carry 2–3 blood keeps each, meaning they can go 2–3 days without a contract before hitting Hungry. A Moucheron at Difficult or worse will not lie about their state if asked directly. They consider it a contractual disclosure.

## Related

- [[murrat|Murrat]]
- [[kalowe|Kalowe]]
- [[five-blades|Five Blades]]
- [[dravosi-crown|Dravosi Crown]]

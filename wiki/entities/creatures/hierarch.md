---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "CR 19 undead lich. Sorcerer lich whose soul is bound to its own bloodline — every living descendant is a phylactery. Two confirmed Hierarchs in the campaign: Aldric Drave and Shepherd Grigori."
created: 2026-05-15
updated: 2026-05-28
tags: [creature, undead, lich, bestiary, cr19]
sources: ["Inbox/Hierarch.md"]
confidence_level: high
cr: 19
aliases: ["Hierarch", "Hierarch lich"]
relationships:
  - "[[aldric-drave|Aldric Drave]] — confirmed Hierarch; founded the Dravosi Crown"
  - "[[shepherd-grigori|Shepherd Grigori]] — confirmed CR 19 Hierarch; currently aboard ship"
---

# Hierarch

![[Hierarch.webp|A Hierarch sorcerer lich binding its bloodline through family phylactery magic]]

```statblock
layout: Basic 5e Layout
name: "Hierarch"
size: Medium
type: undead
alignment: Any Alignment
ac: 17
hp: 263
hit_dice: 31d8 + 124
speed: "30 ft."
stats: [11, 18, 18, 16, 15, 21]
saves:
  - constitution: 10
  - charisma: 12
skillsaves:
  - arcana: 9
  - deception: 12
  - history: 9
  - intimidation: 12
  - persuasion: 12
damage_resistances: "Cold, Necrotic, Poison; Bludgeoning, Piercing, and Slashing from Nonmagical Attacks"
condition_immunities: "Charmed, Exhaustion, Frightened, Paralyzed, Poisoned"
senses: "Darkvision 120 ft., Passive Perception 12"
languages: "The languages it knew in life"
cr: "19"
traits:
  - name: "Blood Phylactery"
    desc: "A destroyed Hierarch gains a new body as long as any bloodline descendants still act as phylacteries. 10+ phylacteries: 1d10 days to reform. 5+: 1d10 weeks. Fewer than 5: 1d10 months."
  - name: "Family Reunion"
    desc: "For each conscious bloodline phylactery within 10 feet, the Hierarch gains +1 to melee and spell attack rolls."
  - name: "Turn Resistance"
    desc: "Advantage on saving throws against any effect that turns undead."
  - name: "Metamagic"
    desc: "At will: Careful Spell, Subtle Spell. 5/day: Distant Spell, Extended Spell. 3/day: Quickened Spell, Seeking Spell, Transmuted Spell. 2/day: Heightened Spell, Twinned Spell."
spells:
  - "Spellcasting. CHA-based (spell save DC 19, +11 to hit). Requires no material components."
  - "At will: Alter Self, Chill Touch, Fire Bolt, Hold Person, Message"
  - "3/day each: Blur, Counterspell, Fear, Hypnotic Pattern, Scorching Ray (3rd level)"
  - "2/day each: Sleet Storm, Blight, Dominate Person"
  - "1/day each: Circle of Death, Disintegrate, Finger of Death"
actions:
  - name: "Might of the Bloodline"
    desc: "Ranged Spell Attack: +11 to hit, range 60 ft. Hit: 10 (3d6) Necrotic damage. If either the Hierarch or the target is within 10 feet of one of the Hierarch's phylacteries, the damage increases by 1d6."
  - name: "Reanimate Family"
    desc: "The Hierarch targets the corpse of a bloodline creature that died within the last minute. It rises immediately as a wight under the Hierarch's control."
  - name: "Blood Sacrifice"
    desc: "One bloodline creature must succeed on a DC 19 Constitution saving throw or take 3d10 Necrotic damage. The Hierarch regains HP equal to the damage dealt and regains one expended spell slot or Metamagic use."
legendary_actions:
  - name: "Cantrip"
    desc: "Cast a cantrip."
  - name: "Might of the Bloodline (Costs 2 Actions)"
    desc: "Make one Might of the Bloodline attack."
  - name: "Reanimate Family (Costs 2 Actions)"
    desc: "Use Reanimate Family."
  - name: "Blood Sacrifice (Costs 2 Actions)"
    desc: "Use Blood Sacrifice."
  - name: "Family Influence (Costs 3 Actions)"
    desc: "One bloodline creature within 30 feet gains +2 to all weapon and spell attack rolls until the end of its next turn."
```

## In The Shattered Sea

A Hierarch is a sorcerer who has bound their soul to their own blood. Every living descendant becomes a phylactery. The bloodline is both the immortality mechanism and the power source. The mechanism has a structural weakness: blood thins across generations. The solution is the Heir ritual — possessing a sufficiently powerful descendant and beginning the process again.

**[[aldric-drave|Aldric Drave]]** founded the Dravosi Crown before the colonial project began, seeding his bloodline into every noble family the Crown would produce. The Crown's genealogical archives are an inadvertent map of his phylactery network. He has been running this cycle for at least three centuries.

**[[shepherd-grigori|Shepherd Grigori]]** is a CR 19 Hierarch currently traveling with the party. His phylactery network is a collection of noble heirs whose incurable illnesses he cured. As long as any of them live, he cannot be permanently killed. His magic type is still unidentified by the party (red viscous light, no components — Arcana 18 failed). His connection to the [[khlysty|Khlysty]] is DM truth.

## Lair Actions

On initiative count 20:
- Bloodied floor — spilled blood covers the area as magical difficult terrain.
- Ancestral surge — all bloodline creatures gain +1 to attacks and saving throws.
- Family rally — all bloodline creatures move up to their speed without opportunity attacks.
- Bloodline metamagic — apply one Metamagic option to any spell cast in the lair without expending uses.

*Source: Pointy Hat*

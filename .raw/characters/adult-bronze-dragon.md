---

title: Adult Bronze Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Adult Bronze Dragon, a CR 15 dragon in the Shattered Sea bestiary.
tags:
- creature
- dragon
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: medium
aliases:
- Adult Bronze Dragon
sources:
- XMM
- Homebrew
relationships:
- relation: listed_in
  target: Bestiary
- relation: patrols
  target: The Galewall
- relation: associated_with
  target: Ashwall Islands
cha: 20
con: 23
cr: 15
creature_type: dragon
cssclasses:
- wiki-monster
dex: 10
environment: coastal
int: 16
page: 59
statblock: inline
str: 25
wis: 15
---

# Adult Bronze Dragon

```statblock
layout: Basic 5e Layout
name: "Adult Bronze Dragon"
size: Huge
type: dragon
alignment: Lawful Good
ac: 18
hp: 212
hit_dice: 17d12 + 102
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [25, 10, 23, 16, 15, 20]
saves:
  - dexterity: 5
  - wisdom: 7
skillsaves:
  - insight: 7
  - perception: 12
  - stealth: 5
damage_immunities: "lightning"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 22"
languages: "Common, Draconic"
cr: "15"
traits:
  - name: "Amphibious"
    desc: "The dragon can breathe air and water."
  - name: "Legendary Resistance (3/Day, or 4/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of (A) Repulsion Breath or (B) Spellcasting to cast Guiding Bolt|XPHB (level 2 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +12 to hit, reach 10 ft. Hit: 16 (2d8 + 7) Slashing damage plus 5 (1d10) Lightning damage."
  - name: "Lightning Breath 5"
    desc: "dex 19, each creature in a 90-foot-long, 5-foot-wide Line [Area of Effect]|XPHB|Line. {@actSaveFail} 55 (10d10) Lightning damage. {@actSaveSuccess} Half damage."
  - name: "Repulsion Breath"
    desc: "str 19, each creature in a 30-foot Cone [Area of Effect]|XPHB|Cone. {@actSaveFail} The target is pushed up to 60 feet straight away from the dragon and has the Prone|XPHB condition."
legendary_actions:
  - name: "Guiding Light"
    desc: "The dragon uses Spellcasting to cast Guiding Bolt|XPHB (level 2 version)."
  - name: "Pounce"
    desc: "The dragon moves up to half its Speed|XPHB, and it makes one Rend attack."
  - name: "Thunderclap"
    desc: "con 17, each creature in a 20-foot-radius Sphere [Area of Effect]|XPHB|Sphere centered on a point the dragon can see within 90 feet. {@actSaveFail} 10 (3d6) Thunder damage, and the target has the Deafened|XPHB condition until the end of its next turn."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 17, +10 to hit, to hit with spell attacks):"
  - "At will: Detect Magic|XPHB, Guiding Bolt|XPHB (level 2 version), Shapechange|XPHB (Beast or Humanoid form only), Speak with Animals|XPHB, Thaumaturgy|XPHB"
  - "1e: Detect Thoughts|XPHB, Water Breathing|XPHB"
```

---

## In The Shattered Sea

[[Galewall|Galewall]] crews have a name for it: the Stormwarden. Not a fixed name — the figure appears differently each generation, always in humanoid form, always in a small boat that has no business being where it is. A battered cutter in the middle of the storm belt. A one-mast smack running alongside a failing ship without apparent difficulty. An old woman in oilskins who comes aboard a dismasted brig in conditions that shouldn't allow boarding, sets the crew to tasks they don't understand until the ship is through, and is gone by the time anyone thinks to ask her name.

What's consistent across the accounts is the result. The ships that follow the Stormwarden's instructions reach the [[Ashwall-Islands|Ashwall]] lee. The ships that don't — because the crew didn't believe it, because the captain refused to take orders from a stranger, because the figure arrived too late — are logged as lost to weather. [[Ashwall-Islands|Ashwall]] crews treat the legend as navigational fact: if something appears during the worst of a crossing and offers guidance, you follow it and you ask questions afterward. ^[inferred]

The shapechange ability is the reason the legend has no single face. Bronze dragons are patient observers who take humanoid form to move among people, gather information, and intervene where they judge it necessary. The Galewall is a crossing that produces exactly the kind of military courage, desperate seamanship, and genuine stakes the dragon finds worth watching. It has been watching the crossing long enough that the Ashwall pilot families have entries in their logs that predate their grandparents' time, all describing the same category of intervention in different hands. Colonial weather-offices have never produced a satisfactory explanation for the survival rate of ships reported as lost but later found at anchor in the Ashwall lee. ^[inferred]

## Related

- [[Shattered-Sea]] — The Shattered Sea
- [[Shattered-Sea]] — The Shattered Sea
- [[Galewall]] — The Galewall

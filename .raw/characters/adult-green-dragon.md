---

title: Adult Green Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-05
summary: CR 15 lawful evil dragon. Cunning manipulator with poison breath, favours forest lairs and long schemes.
tags:
- creature
- dragon
campaign: shattered-sea
subtype: monster
confidence_level: high
aliases:
- Adult Green Dragon
sources: XMM
cha: 18
con: 21
cr: 15
creature_type: dragon
cssclasses:
- wiki-monster
dex: 12
environment: forest
int: 18
page: 153
statblock: inline
str: 23
wis: 15
---

# Adult Green Dragon

```statblock
layout: Basic 5e Layout
name: "Adult Green Dragon"
size: Huge
type: dragon
alignment: Lawful Evil
ac: 19
hp: 207
hit_dice: 18d12 + 90
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [23, 12, 21, 18, 15, 18]
saves:
  - dexterity: 6
  - wisdom: 7
skillsaves:
  - deception: 9
  - perception: 12
  - persuasion: 9
  - stealth: 6
damage_immunities: "poison"
condition_immunities: "poisoned"
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
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast Mind Spike|XPHB (level 3 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +11 to hit, reach 10 ft. Hit: 15 (2d8 + 6) Slashing damage plus 7 (2d6) Poison damage."
  - name: "Poison Breath 5"
    desc: "con 18, each creature in a 60-foot Cone [Area of Effect]|XPHB|Cone. {@actSaveFail} 56 (16d6) Poison damage. {@actSaveSuccess} Half damage."
legendary_actions:
  - name: "Mind Invasion"
    desc: "The dragon uses Spellcasting to cast Mind Spike|XPHB (level 3 version)."
  - name: "Noxious Miasma"
    desc: "con 17, each creature in a 20-foot-radius Sphere [Area of Effect]|XPHB|Sphere centered on a point the dragon can see within 90 feet. {@actSaveFail} 7 (2d6) Poison damage, and the target takes a -2 penalty to AC until the end of its next turn. {@actSaveSuccessOrFail} The dragon can't take this action again until the start of its next turn."
  - name: "Pounce"
    desc: "The dragon moves up to half its Speed|XPHB, and it makes one Rend attack."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 17):"
  - "At will: Detect Magic|XPHB, Mind Spike|XPHB (level 3 version)"
  - "1: Geas|XPHB"
```

## Related

- [[ancient-dragon-turtle]] — Ancient Dragon Turtle

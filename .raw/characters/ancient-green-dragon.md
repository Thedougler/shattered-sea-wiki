---

title: Ancient Green Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-05
summary: CR 22 lawful evil dragon. Master manipulator with devastating poison breath and legendary actions.
tags:
- creature
- dragon
campaign: shattered-sea
subtype: monster
confidence_level: high
sources: XMM
cha: 22
con: 25
cr: 22
creature_type: dragon
cssclasses:
- wiki-monster
dex: 12
environment: forest
int: 20
page: 154
statblock: inline
str: 27
wis: 17
---

# Ancient Green Dragon

```statblock
layout: Basic 5e Layout
name: "Ancient Green Dragon"
size: Gargantuan
type: dragon
alignment: Lawful Evil
ac: 21
hp: 402
hit_dice: 23d20 + 161
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [27, 12, 25, 20, 17, 22]
saves:
  - dexterity: 8
  - wisdom: 10
skillsaves:
  - deception: 13
  - perception: 17
  - persuasion: 13
  - stealth: 8
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 27"
languages: "Common, Draconic"
cr: "22"
traits:
  - name: "Amphibious"
    desc: "The dragon can breathe air and water."
  - name: "Legendary Resistance (4/Day, or 5/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast Mind Spike|XPHB (level 5 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +15 to hit, reach 15 ft. Hit: 17 (2d8 + 8) Slashing damage plus 10 (3d6) Poison damage."
  - name: "Poison Breath 5"
    desc: "con 22, each creature in a 90-foot Cone [Area of Effect]|XPHB|Cone. {@actSaveFail} 77 (22d6) Poison damage. {@actSaveSuccess} Half damage."
legendary_actions:
  - name: "Mind Invasion"
    desc: "The dragon uses Spellcasting to cast Mind Spike|XPHB (level 5 version)."
  - name: "Noxious Miasma"
    desc: "con 21, each creature in a 30-foot-radius Sphere [Area of Effect]|XPHB|Sphere centered on a point the dragon can see within 90 feet. {@actSaveFail} 17 (5d6) Poison damage, and the target takes a -2 penalty to AC until the end of its next turn. {@actSaveSuccessOrFail} The dragon can't take this action again until the start of its next turn."
  - name: "Pounce"
    desc: "The dragon moves up to half its Speed|XPHB, and it makes one Rend attack."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 21):"
  - "At will: Detect Magic|XPHB, Mind Spike|XPHB (level 5 version)"
  - "1e: Geas|XPHB, Modify Memory|XPHB"
```

## Related

- [[ancient-dragon-turtle]] — Ancient Dragon Turtle

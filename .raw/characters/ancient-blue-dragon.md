---

title: Ancient Blue Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Ancient Blue Dragon, a CR 23 dragon in the Shattered Sea bestiary.
tags:
- creature
- dragon
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: medium
aliases:
- Ancient Blue Dragon
sources:
- XMM
- Homebrew
relationships:
- relation: listed_in
  target: Bestiary
- relation: lairs_in
  target: The Outer Reach
cha: 25
con: 27
cr: 23
creature_type: dragon
cssclasses:
- wiki-monster
dex: 10
environment: coastal, desert
int: 18
page: 50
statblock: inline
str: 29
wis: 17
---

# Ancient Blue Dragon

```statblock
layout: Basic 5e Layout
name: "Ancient Blue Dragon"
size: Gargantuan
type: dragon
alignment: Lawful Evil
ac: 22
hp: 481
hit_dice: 26d20 + 208
speed: "40 ft., Burrow 40 ft., Fly 80 ft."
stats: [29, 10, 27, 18, 17, 25]
saves:
  - dexterity: 7
  - wisdom: 10
skillsaves:
  - perception: 17
  - stealth: 7
damage_immunities: "lightning"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 27"
languages: "Common, Draconic"
cr: "23"
traits:
  - name: "Legendary Resistance (4/Day, or 5/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast Shatter|XPHB (level 3 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +16 to hit, reach 15 ft. Hit: 18 (2d8 + 9) Slashing damage plus 11 (2d10) Lightning damage."
  - name: "Lightning Breath 5"
    desc: "dex 23, each creature in a 120-foot-long, 10-foot-wide Line [Area of Effect]|XPHB|Line. {@actSaveFail} 88 (16d10) Lightning damage. {@actSaveSuccess} Half damage."
legendary_actions:
  - name: "Cloaked Flight"
    desc: "The dragon uses Spellcasting to cast Invisibility|XPHB on itself, and it can fly up to half its Fly Speed|XPHB. The dragon can't take this action again until the start of its next turn."
  - name: "Sonic Boom"
    desc: "The dragon uses Spellcasting to cast Shatter|XPHB (level 3 version). The dragon can't take this action again until the start of its next turn."
  - name: "Tail Swipe"
    desc: "The dragon makes one Rend attack."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 22):"
  - "At will: Detect Magic|XPHB, Invisibility|XPHB, Mage Hand|XPHB, Shatter|XPHB (level 3 version)"
  - "1e: Scrying|XPHB, Sending|XPHB"
```

---

## In [[Shattered-Sea|The Shattered Sea]]

The Redwind Isles are described on pilot charts as hot, arid, and barely inhabited. The barely is doing significant work.

The Isles sit in the southeastern [[Outer-Reach|Outer Reach]], named for the seasonal dust that blows in from the south and leaves red grit on every surface. The geology is old sandstone and dry limestone, fractured by the same ancient seismic activity that formed the Maw's trench. Good burrowing ground. Almost no fresh water. Almost nothing worth the voyage — which is the same thing colonial cartographers have written about these islands for two centuries without asking what made them that way. ^[inferred]

The Isles were not always barely inhabited. Old charts from before the colonial era mark permanent settlements on two of the larger islands and seasonal anchorages on three more. Those marks stopped appearing in the records within a generation of each other, without explanation. The gap between the last record of settlement and the first colonial chart labelling them uninhabited is short enough that it has a cause. Something moved in, or something that had always been there finally made its presence felt, and the people on those islands made a reasonable decision. ^[inferred]

An ancient blue dragon does not need to attack frequently. It is patient, methodical, and large enough that a single encounter leaves no ambiguity about whether the Isles have an owner. The few vessels that have anchored in the Redwind harbours and returned describe a stillness that doesn't match the wind — an absence of birds, a quality of silence that has intent in it, and, in one account from a pilgrim ship that cut its visit very short, a shape moving through overcast above the southern cliffs that was too deliberate for weather and too large for anything else. The pilgrim ship did not attempt the anchorage again. The account is careful to describe only what was seen, because the crew understood that what was seen was already more than enough. ^[inferred]

## Related

- [[Shattered-Sea]] — The Shattered Sea
- [[ancient-dragon-turtle]] — Ancient Dragon Turtle

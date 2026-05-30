---

title: Adult Black Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Adult Black Dragon, a CR 14 dragon in the Shattered Sea bestiary.
tags:
- creature
- dragon
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: medium
aliases:
- Adult Black Dragon
sources:
- XMM
- Homebrew
relationships:
- relation: listed_in
  target: Bestiary
- relation: lairs_in
  target: The Doldrums
cha: 19
con: 21
cr: 14
creature_type: dragon
cssclasses:
- wiki-monster
dex: 14
environment: swamp
int: 14
page: 39
statblock: inline
str: 23
wis: 13
---

# Adult Black Dragon

```statblock
layout: Basic 5e Layout
name: "Adult Black Dragon"
size: Huge
type: dragon
alignment: Chaotic Evil
ac: 19
hp: 195
hit_dice: 17d12 + 85
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [23, 14, 21, 14, 13, 19]
saves:
  - dexterity: 7
  - wisdom: 6
skillsaves:
  - perception: 11
  - stealth: 7
damage_immunities: "acid"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 21"
languages: "Common, Draconic"
cr: "14"
traits:
  - name: "Amphibious"
    desc: "The dragon can breathe air and water."
  - name: "Legendary Resistance (3/Day, or 4/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast Melf's Acid Arrow|XPHB (level 3 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +11 to hit, reach 10 ft. Hit: 13 (2d6 + 6) Slashing damage plus 4 (1d8) Acid damage."
  - name: "Acid Breath 5"
    desc: "dex 18, each creature in a 60-foot-long, 5-foot-wide Line [Area of Effect]|XPHB|Line. {@actSaveFail} 54 (12d8) Acid damage. {@actSaveSuccess} Half damage."
legendary_actions:
  - name: "Cloud of Insects"
    desc: "dex 17, one creature the dragon can see within 120 feet. {@actSaveFail} 22 (4d10) Poison damage, and the target has Disadvantage|XPHB on saving throws to maintain Concentration|XPHB until the end of its next turn. {@actSaveSuccessOrFail} The dragon can't take this action again until the start of its next turn."
  - name: "Frightful Presence"
    desc: "The dragon uses Spellcasting to cast Fear|XPHB. The dragon can't take this action again until the start of its next turn."
  - name: "Pounce"
    desc: "The dragon can move up to half its Speed|XPHB, and it makes one Rend attack."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 17, +9 to hit, to hit with spell attacks):"
  - "At will: Detect Magic|XPHB, Fear|XPHB, Melf's Acid Arrow|XPHB (level 3 version)"
  - "1e: Speak with Dead|XPHB, Vitriolic Sphere|XPHB"
```

---

## In [[Shattered-Sea|The Shattered Sea]]

The [[Doldrums|Doldrums]] are the right habitat. Still water, no wind, mangrove shallows, the accumulated rot of anything that blooms or dies in flat heat with nowhere to go. A black dragon laired in the Doldrums' deeper mangrove channels has everything it needs: cover, patience, and prey that cannot run.

A becalmed ship is close to ideal hunting. The crew cannot sail. Towing with boats means people in the water. The Doldrums silence carries the acid breath line clean across a deck with nothing to scatter it. The dragon is amphibious — it can strike from below, surface for one clean pass, and go back under before a crossbow is drawn. Crews that survive describe the attack in very similar terms: something long and dark alongside the hull that they mistook for shadow, then a burning line across the deck that smelled wrong, then a wing-shape dropping back into water that barely registered the impact. ^[inferred]

The account that made it into Midchain pilot circles came from a brig becalmed for three days south of [[Midchain]]'s edge. On the second night, a deckhand checking the stern in the pre-dawn saw a shadow beneath the keel that blotted out the bottom. Nothing else. By morning, one of the stern planks had a seam that hadn't been there at departure — dissolved rather than split. The captain towed out at first light and ran the oars for six hours until the wind found them. His repair log described weather damage. The hull carpenter's private notes said something else. Neither man has sailed the Doldrums since. ^[inferred]

## Related

- [[Shattered-Sea]] — The Shattered Sea
- [[Doldrums]] — The Doldrums
- [[ancient-dragon-turtle]] — Ancient Dragon Turtle

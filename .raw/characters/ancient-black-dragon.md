---

title: Ancient Black Dragon
type: monster
publish: true
created: 2026-04-25
updated: 2026-05-03
summary: The Ancient Black Dragon, a CR 21 dragon in the Shattered Sea bestiary.
tags:
- creature
- dragon
- bestiary
campaign: shattered-sea
audience: players
subtype: monster
confidence_level: medium
aliases:
- Ancient Black Dragon
sources:
- XMM
- Homebrew
relationships:
- relation: listed_in
  target: Bestiary
- relation: lairs_in
  target: Aruhe
cha: 22
con: 25
cr: 21
creature_type: dragon
cssclasses:
- wiki-monster
dex: 14
environment: swamp
int: 16
page: 40
statblock: inline
str: 27
wis: 15
---

# Ancient Black Dragon

```statblock
layout: Basic 5e Layout
name: "Ancient Black Dragon"
size: Gargantuan
type: dragon
alignment: Chaotic Evil
ac: 22
hp: 367
hit_dice: 21d20 + 147
speed: "40 ft., Fly 80 ft., Swim 40 ft."
stats: [27, 14, 25, 16, 15, 22]
saves:
  - dexterity: 9
  - wisdom: 9
skillsaves:
  - perception: 16
  - stealth: 9
damage_immunities: "acid"
senses: "Blindsight 60 ft., Darkvision 120 ft., Passive Perception 26"
languages: "Common, Draconic"
cr: "21"
traits:
  - name: "Amphibious"
    desc: "The dragon can breathe air and water."
  - name: "Legendary Resistance (4/Day, or 5/Day in Lair)"
    desc: "If the dragon fails a saving throw, it can choose to succeed instead."
actions:
  - name: "Multiattack"
    desc: "The dragon makes three Rend attacks. It can replace one attack with a use of Spellcasting to cast Melf's Acid Arrow|XPHB (level 4 version)."
  - name: "Rend"
    desc: "Melee Weapon Attack: +15 to hit, reach 15 ft. Hit: 17 (2d8 + 8) Slashing damage plus 9 (2d8) Acid damage."
  - name: "Acid Breath 5"
    desc: "dex 22, each creature in a 90-foot-long, 10-foot-wide Line [Area of Effect]|XPHB|Line. {@actSaveFail} 67 (15d8) Acid damage. {@actSaveSuccess} Half damage."
legendary_actions:
  - name: "Cloud of Insects"
    desc: "dex 21, one creature within 120 feet. {@actSaveFail} 33 (6d10) Poison damage, and the target has Disadvantage|XPHB on saving throws to maintain Concentration|XPHB until the end of its next turn. {@actSaveSuccessOrFail} The dragon can't take this action again until the start of its next turn."
  - name: "Frightful Presence"
    desc: "The dragon uses Spellcasting to cast Fear|XPHB. The dragon can't take this action again until the start of its next turn."
  - name: "Pounce"
    desc: "The dragon moves up to half its Speed|XPHB, and it makes one Rend attack."
spells:
  - "The dragon casts one of the following spells, requiring no Material components and using Charisma as the spellcasting ability (spell save 21, +13 to hit, to hit with spell attacks):"
  - "At will: Detect Magic|XPHB, Fear|XPHB, Melf's Acid Arrow|XPHB (level 4 version)"
  - "1e: Create Undead|XPHB, Speak with Dead|XPHB, Vitriolic Sphere|XPHB (level 5 version)"
```

---

## In [[Shattered-Sea|The Shattered Sea]]

The oldest Midchain pilots know that [[Aruhe|Aruhe]] is not avoided because of the [[Grung]]. The Grung don't go there either.

The public story — patrol boats, territorial pressure, a settlement that never held — is true as far as it goes. The settlement failed because people started disappearing. Not all at once. One a season, then two, then the kind of rate that makes a community decide it has misread the island and leave while there are still enough of them to sail. The Grung patrol boats came after, and they are a sufficient reason to stay away, which is convenient because the real reason is harder to say out loud.

The water around Aruhe's eastern tip runs a faint brown-gold at low tide. Not silt. Not algae. Old Midchain pilots who have passed close enough know the smell — the same sharp-mineral bite as a hull plank dissolved by acid seep. Something in the flooded interior drains into the sea, and what drains out of something that old, in something that large, in an island it has had to itself for long enough to shape the drainage — that is not weather. The terraces didn't fall from neglect. They dissolved from the base up, slowly, over the kind of time that an ancient black dragon uses the way other things use a season. ^[inferred]

The Grung name for Aruhe doesn't translate, but the [[Sorn]] intermediaries who know enough of the language to trade have described the nearest equivalent as something like *the island that is already eaten*. Nobody from outside has verified this. Nobody from outside has had a reason to get close enough to try. ^[inferred]

## Related

- [[Midchain]] — The Midchain
- [[Shattered-Sea]] — The Shattered Sea
- [[Grung-Clans]] — The Grung Clans
- [[Sorn]] — Sorn
- [[ancient-dragon-turtle]] — Ancient Dragon Turtle

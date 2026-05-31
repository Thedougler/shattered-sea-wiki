---
type: monster
subtype: monster
campaign: shattered-sea
status: unknown
audience: players
publish: true
summary: The Giant Squid, a CR 6 beast in the Shattered Sea bestiary.
created: 2026-04-25
updated: 2026-05-31
tags: []
sources:
  - XMM
confidence_level: high
aliases:
  - Giant Squid
cha: 4
con: 12
cr: 6
creature_type: beast
dex: 14
environment: underwater
int: 5
page: 360
statblock: inline
str: 23
wis: 11
---

# Giant Squid

[[the-drowned-maw|The Drowned Maw]] has the depth for them — no sounding line has found the bottom, and what moves in that dark water is a matter of competing testimony. Giant squid are the practical explanation for a category of Maw encounters that don't require the vocabulary of krakens or leviathans: a dive line going taut without a diver pulling it, a shadow at the edge of darkvision that moves away before it can be named, a rope severed clean below the agreed depth.

At the [[shelfworks|Shelfworks]], the shelf ends twenty metres east of the last visible Antheri wall and drops into black water. Giant squid come up the drop-off at night, occasionally as shallow as the dive floor. One Shelfworks rule — *do not chase something below the agreed depth* — exists because a salvager named Orvalle did. He came back up without his dive partner's line, missing a knife, and described a shape that spread wider than the archway he was working through, which extended a limb the length of a boarding pike, and pulled. His partner's buoy surfaced forty minutes later, alone. Orvalle does not dive anymore. He now works the air pumps and will tell the story once per crew, once per season, and not again. ^[inferred]

```statblock
layout: Basic 5e Layout
name: "Giant Squid"
size: Huge
type: beast
alignment: Unaligned
ac: 12
hp: 120
hit_dice: 16d12 + 16
speed: "5 ft., Swim 80 ft."
stats: [23, 14, 12, 5, 11, 4]
saves:
  - strength: 9
  - dexterity: 5
skillsaves:
  - perception: 6
senses: "Darkvision 120 ft., Passive Perception 16"
languages: "—"
cr: "6"
traits:
  - name: "Water Breathing"
    desc: "The squid can breathe only underwater."
actions:
  - name: "Multiattack"
    desc: "The squid makes one Bite attack and one Tentacle attack."
  - name: "Bite"
    desc: "Melee Weapon Attack: +9 to hit, reach 5 ft. Hit: 28 (4d10 + 6) Piercing damage."
  - name: "Tentacle"
    desc: "Melee Weapon Attack: +9 to hit, reach 15 ft. Hit: 19 (3d8 + 6) Bludgeoning damage. If the target is a Huge or smaller creature, it has the Grappled|XPHB condition (escape 16) from one of two tentacles, and the squid can pull the target up to 10 feet straight toward itself."
reactions:
  - name: "Ink Cloud (1/Day)"
    desc: "{@actTrigger} The squid takes damage while underwater. {@actResponse} The squid releases ink that fills a 15-foot Cube [Area of Effect]|XPHB|Cube centered on itself, and the squid moves up to its Swim Speed|XPHB. The Cube [Area of Effect]|XPHB|Cube is Heavily Obscured|XPHB for 1 minute or until a strong current or similar effect disperses the ink."
```

## Related

- [[antheri-ruins|Antheri Ruins]]
- [[giant-constrictor-snake|Giant Constrictor Snake]]
- [[giant-axe-beak|Giant Axe Beak]]

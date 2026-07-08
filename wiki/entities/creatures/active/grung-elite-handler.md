---
type: monster
subtype: monster
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: CR 3 blue-caste coordinator; commands allied grungs to act on its turn, redirects incoming attacks onto subordinates, and navigates sewers without impediment. Simone's operational backbone — the grung Jean-Claude can read before any local can name it.
created: 2026-06-28
updated: 2026-06-28
tags:
  - grung
  - combat
sources: []
confidence_level: homebrew
aliases:
  - Blue-Caste Elite Handler
statblock: inline
cr: 3
creature_type: humanoid
str: 7
dex: 16
con: 16
int: 14
wis: 13
cha: 13
environment: sewer, urban, swamp
---

# Grung Elite Handler

```statblock
layout: Basic 5e Layout
name: "Grung Elite Handler"
size: Small
type: humanoid
subtype: grung
alignment: Typically Lawful Evil
ac: 13
ac_note: natural armor
hp: 65
hit_dice: 10d6+30
speed: "25 ft., Climb 25 ft."
stats: [7, 16, 16, 14, 13, 13]
saves:
  - dexterity: 5
  - intelligence: 4
skillsaves:
  - athletics: 2
  - perception: 3
  - stealth: 5
  - survival: 3
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Passive Perception 13"
languages: "Grung"
cr: "3"
traits:
  - name: "Amphibious"
    desc: "The grung can breathe air and water."
  - name: "Poisonous Skin"
    desc: "Any creature that grapples the grung or otherwise comes into direct contact with the grung's skin must succeed on a DC 13 Constitution saving throw or become poisoned for 1 minute. A poisoned creature no longer in direct contact with the grung can repeat the saving throw at the end of each of its turns, ending the effect on a success."
  - name: "Sewer Sense"
    desc: "The handler ignores difficult terrain caused by water, mud, or sewage, and cannot be surprised while underground."
  - name: "Standing Leap"
    desc: "The grung's long jump is up to 25 feet and its high jump is up to 15 feet, with or without a running start."
actions:
  - name: "Multiattack"
    desc: "The grung makes two attacks with its dagger or shortbow."
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage plus 5 (2d4) poison damage."
  - name: "Shortbow"
    desc: "Ranged Weapon Attack: +5 to hit, range 80/320 ft., one target. Hit: 6 (1d6 + 3) piercing damage plus 5 (2d4) poison damage."
  - name: "Coordinate Strike (Recharge 5-6)"
    desc: "The handler barks a rapid command at up to two allied grungs it can see within 30 feet. Each target can immediately use its reaction to move up to half its speed and make one weapon attack."
reactions:
  - name: "Redirect"
    desc: "When the handler is targeted by a ranged attack, it can order an adjacent allied grung to step into the path of the blow. The adjacent grung becomes the new target of the attack instead."
```

## Tactical Profile

**Role:** Controller. The handler does not lead with raw damage — it multiplies the action economy of its squad. Every round it survives is a round its subordinates get an extra attack.

**Opening move:** Takes a concealed position within 30 feet of its squad on round 1 and opens with Shortbow. It does not use Coordinate Strike until it has at least two allied grungs in position and a viable target is within their reach — it holds the ability like a second action economy.

**Escalation (~50% HP):** Stops conserving Coordinate Strike and fires it on any recharge. Uses Redirect aggressively, ordering the nearest green-caste laborer to intercept. Tactically, it prioritizes keeping itself alive over preserving subordinates.

**Morale:** Breaks and retreats if it has no allies within 30 feet or if the magazine it guards is compromised. A handler without a squad is functionally dead — its whole value is coordination.

**Tactical personality:** Cunning. Targets casters and concentration-holders first through its directed strikes. If [[perrin-black-jaw|Perrin]] has concentration up, the handler calls him out by silhouette to its squad.

## Encounter Notes

Coordinate Strike fires once per fight on average (Recharge 5-6). The threat it creates is action-economy pressure: two grungs who weren't acting suddenly act, often against a PC who had correctly identified only one as a threat. Delay its use to round 2 so the party doesn't know it's coming — the surprise of two reaction attacks landing simultaneously is the memorable moment.

Redirect feels like a betrayal. When it orders a green-caste laborer to take an arrow meant for it, players understand exactly what kind of creature the handler is. That read lands harder if the laborer dies to it.

Handlers appear in the [[calveno-sewers-grung-magazines|Calveno sewer network]] as coordinators at secondary magazine sites — each running a team of 2–4 green-caste laborers. At the primary Mercatura site, purple-caste warriors replace them; handlers there have been evacuated ahead of detonation day.

## PC Connection

[[jean-claude-tabarnack|Jean-Claude]] recognizes blue-caste handler discipline from years inside Simone's operation: the deference hierarchy, the way a handler places itself behind its squad rather than in front, the specific cadence of a position report. He can identify a handler from body language before the handler speaks. The handler is Simone's work — and Jean-Claude is the only person in the party who knows what that means operationally.

## Related

- [[grung-elite-warrior|Grung Elite Warrior]] — purple-caste warriors stationed at primary and secondary magazine sites
- [[grung-npc|Grung (Green-Caste NPC)]] — laborers the handler coordinates
- [[grung-wildling|Grung Wildling]]
- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]]
- [[calveno-sewers-grung-magazines|Calveno Sewer Magazines]]

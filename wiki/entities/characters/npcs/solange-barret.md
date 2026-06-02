---
type: entity
subtype: npc
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "Red-caste Grung warlock and Simone's ritual specialist — operates the Otar summoning circle beneath the Mercatura. Pact-bound chaos caster with Counterspell and Hold Person."
created: 2026-06-01
updated: 2026-06-01
tags:
  - grung
  - combat
sources:
  - Homebrew
confidence_level: high
species: grung
aliases:
  - Solange
  - The Summoner
  - Red-Caste Summoner
cr: 3
statblock: inline
---

# Solange Barret

| | |
|---|---|
| **Species** | Grung (Red Caste) |
| **Role** | Ritual specialist, warlock; direct subordinate of [[simone-tabarnack\|Simone Tabarnack]] |
| **Location** | [[calveno-sewers-grung-magazines\|Primary detonation chamber]], Mercatura collector system |

## Overview

Solange Barret is the reason [[otar-the-foul|Otar the Foul]] can be summoned at all. She is the only member of Simone's operation with the arcane training to operate the summoning circle beneath the Mercatura — a circle built with techniques the Grung did not develop themselves. Solange learned the binding geometry from her patron, an entity she does not name and refers to only as *le courant* (the current).

She is red caste — the highest operational rank below Simone herself. Where Simone designs operations, Solange executes the parts that require precision no warrior can provide. She has been with Simone since Sorn, and she is the only subordinate Simone trusts with the circle's activation sequence.

## Appearance & Manner

Red-skinned Grung, small even for her kind. Wears no armor — a sleeveless leather harness over bare skin, tools and chalk sticks in belt loops. Her hands are always stained with circle-inscription residue: powdered limestone, charcoal, something iridescent that does not wash off. She works with the focused stillness of someone who knows that one misdrawn line ends the operation. Does not speak unless spoken to. When she does, her voice is flat and certain.

## Roleplay Concept

Seminary dropout meets demolitions engineer. She has real arcane training in a society that does not value it, and she treats the summoning circle with the reverence of someone who understands exactly what she is calling through. Not fanatical — professional. The circle is her craft. Otar is her work product.

> *"The circle is not a weapon. It is an invitation. What arrives does not care about your objections."*

## Proactive Objective

When the party encounters Solange, she is working. Final inscriptions on the summoning circle — calibrating the resonance channels that key the activation to the blackpowder detonation above. She has been at this for hours. She is close to finished. Her attention is split between the circle and the four [[grung-elite-warrior|Elite Warriors]] guarding the chamber. She does not expect intruders at the primary site — it is compartmentalized above green-caste clearance, and the secondary sites should absorb any interference.

## Combat

```statblock
layout: Basic 5e Layout
name: "Solange Barret"
size: Small
type: humanoid
subtype: grung
alignment: Lawful Evil
ac: 13
ac_note: "natural armor (15 within 10 ft. of summoning circle)"
hp: 45
hit_dice: 10d6 + 10
speed: "25 ft., Climb 25 ft."
stats: [7, 16, 12, 14, 12, 16]
saves:
  - wisdom: 3
  - charisma: 5
skillsaves:
  - arcana: 4
  - deception: 5
  - stealth: 5
damage_immunities: "poison"
condition_immunities: "poisoned"
senses: "Darkvision 60 ft., Passive Perception 11"
languages: "Grung, Common, Deep Speech"
cr: "3"
source: "Homebrew — Shattered Sea"
traits:
  - name: "Amphibious"
    desc: "Solange can breathe air and water."
  - name: "Poisonous Skin"
    desc: "Any creature that grapples Solange or comes into direct contact with her skin must succeed on a DC 12 Constitution saving throw or become poisoned for 1 minute. A poisoned creature can repeat the saving throw at the end of each of its turns, ending the effect on a success."
  - name: "Standing Leap"
    desc: "Solange's long jump is up to 25 feet and her high jump is up to 15 feet, with or without a running start."
  - name: "Circle Ward"
    desc: "While within 10 feet of the summoning circle, Solange has advantage on Constitution saving throws to maintain concentration and her AC increases by 2 (to AC 15)."
  - name: "Pact Magic"
    desc: "Solange is a 5th-level warlock. Her spellcasting ability is Charisma (spell save DC 13, +5 to hit with spell attacks). She has the following spells:\n\nCantrips (at will): Eldritch Blast (2 beams), Minor Illusion, Poison Spray\n3rd level (2 slots): Counterspell, Hex, Hold Person, Misty Step\n1/day: Dimension Door"
actions:
  - name: "Eldritch Blast"
    desc: "Ranged Spell Attack: +5 to hit, range 120 ft., two beams. Hit: 8 (1d10 + 3) force damage per beam."
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage plus 5 (2d4) poison damage."
reactions:
  - name: "Counterspell"
    desc: "When Solange sees a creature within 60 feet casting a spell, she can use a spell slot to attempt to interrupt it. The spell fails if it is 3rd level or lower. For a higher-level spell, she must succeed on a Charisma check (DC 10 + spell level)."
```

## Tactical Behavior

**Opening:** Hex on the nearest martial PC (disadvantage on STR checks — anti-grapple), then Eldritch Blast from behind the Elite Warrior line. Stays within 10 feet of the circle (Circle Ward: AC 15, advantage on concentration saves).

**Escalation:** If a spellcaster attempts to disrupt the circle or target the Elite Warriors with control spells, Solange Counterspells. She has two 3rd-level slots — one Counterspell burns half her resources. Force her to choose between maintaining Hex and countering party magic.

**Crisis:** If the chamber is clearly lost (3+ Elite Warriors dead, circle being physically disrupted), Solange uses Misty Step to break line of sight, then Dimension Door on her next turn to escape entirely. She will not die for the circle — she is too important to Simone's future operations.

**Morale:** Retreats when the fight is clearly lost. Does not surrender. If captured, she says nothing about Simone. She gives her name and caste. That is all.

## If She Escapes

Solange reports to Simone: the primary site is compromised, the party includes a Grung defector who identified caste notation (Jean-Claude), and the operation's centrepiece is lost. This confirmation — that Jean-Claude is actively working against the clan — is a major escalation of Simone's awareness. It is also the first intelligence Simone receives about exactly who is interfering.

## Connections

- [[simone-tabarnack|Simone Tabarnack]] — commander, the only person whose orders Solange follows without question
- [[otar-the-foul|Otar the Foul]] — the entity Solange's circle is configured to summon
- [[calveno-sewers-grung-magazines|Calveno Sewer Magazines]] — the primary detonation chamber where Solange operates
- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] — the operation Solange's ritual anchors
- [[jean-claude-tabarnack|Jean-Claude Tabarnack]] — if Solange escapes, she identifies him to Simone

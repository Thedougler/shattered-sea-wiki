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

When the party encounters Solange, she is finishing the summoning ritual. One hand on the stone, the other tracing the final resonance arc. She has been at this for hours and is minutes from completion. She does not fight. She channels — using her action every turn to sustain the ritual, unable to attack or cast offensive spells. The four [[grung-elite-warrior|Elite Warriors]] are her shield, and they are expendable. When half of them fall, she detonates the blackpowder ceiling as a reaction — a command word keyed to alchemical fuses, not a spell, not counterspellable. The summoning circle deflects the blast. Everyone outside the circle takes the full detonation. She finishes the ritual in the settling dust, and Otar manifests through her body. The transformation consumes her.

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
hp: 66
hit_dice: 12d6 + 24
speed: "25 ft., Climb 25 ft."
stats: [7, 16, 14, 14, 12, 16]
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
    desc: "While within 10 feet of the summoning circle, Solange has advantage on Constitution saving throws to maintain concentration and her AC increases by 2 (to AC 15). The active circle sheds bright light in a 10-foot radius and dim light for an additional 10 feet."
  - name: "Pact Magic"
    desc: "Solange is a 5th-level warlock. Her spellcasting ability is Charisma (spell save DC 13, +5 to hit with spell attacks). She has the following spells:\n\nCantrips (at will): Eldritch Blast (2 beams), Minor Illusion, Poison Spray\n3rd level (2 slots): Hex, Hold Person, Misty Step\n1/day each: Dimension Door, Mirror Image"
actions:
  - name: "Eldritch Blast"
    desc: "Ranged Spell Attack: +5 to hit, range 120 ft., two beams. Hit: 8 (1d10 + 3) force damage per beam."
  - name: "Dagger"
    desc: "Melee or Ranged Weapon Attack: +5 to hit, reach 5 ft. or range 20/60 ft., one target. Hit: 5 (1d4 + 3) piercing damage plus 5 (2d4) poison damage."
reactions:
  - name: "Counterspell (Pact Magic Slot)"
    desc: "When Solange sees a creature within 60 feet casting a spell, she can expend a Pact Magic slot to attempt to interrupt it. The spell fails if it is 3rd level or lower. For higher-level spells, she must succeed on a DC 10 + spell level Charisma check (+5)."
```

## Tactical Behavior

**Channeling:** Mirror Image is already active (pre-cast, 3 duplicates — soaks 3 attacks before real damage lands). Solange uses her action every turn to sustain the summoning ritual. She cannot attack or cast offensive spells while channeling. Stays within 10 ft of the circle (Circle Ward: AC 15, advantage on concentration saves). The circle sheds bright light in a 10-ft radius — Jean-Claude's Umbral Sight does not function here.

**Reaction — Counterspell or Detonate:** If a spellcaster targets the circle or casts a control spell threatening her concentration, Solange Counterspells (auto-counters 3rd level or lower, +5 check for higher). She has two 3rd-level slots — each Counterspell burns half her resources and costs her the detonation trigger for that round. **Detonate:** the instant the second Elite Warrior falls, Solange uses her reaction to speak a command word that ignites alchemical fuses in the ceiling scaffolding. This is not a spell — it cannot be counterspelled. The summoning circle deflects the blast in a 10-ft radius; everyone outside takes 8d6 fire + 4d6 bludgeoning (DC 16 DEX/STR).

**Manifestation:** On her next turn after the detonation, Solange completes the ritual. [[otar-the-foul|Otar the Foul]] manifests through her body — shadow, ichor, violent transformation. Solange is consumed. The transformation cannot be reversed.

**If the circle is disrupted before detonation:** Solange loses the summoning but still detonates as a diversion. She escapes via Misty Step (break line of sight) → Dimension Door (to the surface). She will not die for a failed ritual.

**Morale:** If the circle is intact, Solange does not retreat — she is the delivery system and knows it. If the circle is disrupted, she escapes. Does not surrender. If captured before either trigger, she gives her name and caste. That is all.

## If She Escapes

Solange escapes only if the circle is disrupted before the detonation trigger (2 of 4 Elite Warriors down). In that case, she detonates the ceiling as a diversion and Dimension Doors to the surface. She reports to Simone: the primary is compromised, a Grung defector identified caste notation (Jean-Claude), and the summoning failed. This is a major escalation of Simone's awareness — the first intelligence she receives about exactly who is interfering.

If the ritual completes, Solange does not escape. She is consumed by the manifestation. Otar the Foul stands where she was. Simone does not learn about Jean-Claude from this source.

## Connections

- [[simone-tabarnack|Simone Tabarnack]] — commander, the only person whose orders Solange follows without question
- [[otar-the-foul|Otar the Foul]] — the entity Solange's circle is configured to summon
- [[calveno-sewers-grung-magazines|Calveno Sewer Magazines]] — the primary detonation chamber where Solange operates
- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] — the operation Solange's ritual anchors
- [[jean-claude-tabarnack|Jean-Claude Tabarnack]] — if Solange escapes, she identifies him to Simone

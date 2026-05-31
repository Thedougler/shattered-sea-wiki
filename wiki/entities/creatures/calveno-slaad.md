---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "Custom Red Slaad boss for the Calveno raid. Summoned unbound through Simone's circle — chaotic, regenerating, designed to split a Level 4 party's attention between the monster and the extraction running behind it."
created: "2026-05-30"
tags:
  - creature
  - aberration
  - slaad
  - boss
  - cr7
  - calveno
sources:
  - Homebrew
confidence_level: high
cr: 7
aliases:
  - "The Mercatura Slaad"
  - "Simone's Slaad"
---

# Calveno Slaad — The Groundbreaker

![[Calveno-Slaad-Emergence.png|A massive red Slaad hauling itself out of a collapsed plaza crater, dust and rubble cascading off its back, festival cloth tangled around one arm, mouth open in a roar that scatters the crowd]]

This is not a standard Red Slaad. Simone's red-caste operatives bound this creature through a summoning circle keyed to detonation — no control gem, no binding, no leash. It is released into a collapsing plaza full of panicking civilians and tasked with one thing by instinct: destroy whatever is in front of it. The circle's construction used techniques the Grung did not develop themselves; the arcane work was contracted, and the contractor is an open question.

## Design Intent

The party trivialized Barnaby Rook via environmental repositioning (gusts, thrown objects) and the whip shark through concentrated damage output. This Slaad is built to punish both patterns:

- **Chaos Pulse** punishes clustering and concentration, forcing the party to spread.
- **Entropic Regeneration** (15 HP/round, suppressed only by fire or acid) demands sustained pressure — they cannot burst it in two rounds and move on.
- **Tongue Lash** (30 ft. grapple + pull) counters ranged kiting, specifically threatening Jean-Claude's preferred distance.
- **Rubble Surge** uses the collapsed-plaza environment as a weapon, countering flight and repositioning.
- **No legendary actions.** The Slaad is chaotic, not tactical. It doesn't respond to player turns — it acts on its own terms. The lair actions represent the unstable environment, not the Slaad's intelligence.

The fight should feel like containing a disaster, not outmaneuvering a commander. Every round the party spends on the Slaad is a round the extraction at the four secondary sites runs unopposed. The real boss is the clock.

```statblock
layout: Basic 5e Layout
name: "Calveno Slaad"
size: Large
type: aberration
alignment: "chaotic neutral"
ac: 15
ac_class: "natural armor"
hp: 161
hit_dice: "17d10 + 68"
speed: "40 ft., climb 20 ft."
stats: [20, 12, 18, 5, 8, 6]
saves:
  - constitution: 7
  - strength: 8
skillsaves:
  - athletics: 8
  - perception: 2
damage_resistances: "cold, lightning, thunder"
damage_immunities: "none"
condition_immunities: "frightened"
senses: "darkvision 60 ft., passive Perception 12"
languages: "Slaad (does not communicate)"
cr: 7
source: "Homebrew — Shattered Sea"
traits:
  - name: Entropic Regeneration
    desc: "The Slaad regains 15 hit points at the start of its turn if it has at least 1 hit point. If the Slaad takes fire or acid damage, this trait doesn't function at the start of the Slaad's next turn."
  - name: Magic Resistance
    desc: "The Slaad has advantage on saving throws against spells and other magical effects."
  - name: Chaos Embodied
    desc: "The Slaad cannot be charmed, and any creature that starts its turn within 10 feet of the Slaad must succeed on a DC 15 Wisdom saving throw or have disadvantage on its next attack roll. Creatures immune to the frightened condition are immune to this effect."
  - name: Unstable Form
    desc: "When the Slaad is reduced to half its hit points (80 HP) or fewer, its skin splits and weeps iridescent fluid. Its melee attacks deal an additional 1d6 acid damage, and any creature that hits it with a melee attack within 5 feet takes 5 (1d10) acid damage."
actions:
  - name: Multiattack
    desc: "The Slaad makes three attacks: one Bite, one Claw, and one Tongue Lash. It can replace the Tongue Lash with a second Claw attack."
  - name: Bite
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) piercing damage. On a hit, the target must succeed on a DC 15 Constitution saving throw or be infected with a Slaad egg (Slaad Tadpole disease — no immediate effect; 3 months to manifest)."
  - name: Claw
    desc: "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 12 (2d6 + 5) slashing damage."
  - name: Tongue Lash
    desc: "Melee Weapon Attack: +8 to hit, reach 30 ft., one target. Hit: 9 (1d8 + 5) bludgeoning damage, and the target must succeed on a DC 16 Strength saving throw or be pulled up to 25 feet toward the Slaad and grappled (escape DC 16). While grappled, the target is restrained. The Slaad can grapple one creature this way at a time."
  - name: "Chaos Pulse (Recharge 5-6)"
    desc: "The Slaad slams both fists into the ground. Each creature within 20 feet must make a DC 15 Dexterity saving throw. On a failure, a creature takes 22 (4d10) force damage and is knocked prone. On a success, a creature takes half damage and isn't knocked prone. Rubble and debris in the area become difficult terrain."
reactions:
  - name: Rubble Surge
    desc: "When a creature the Slaad can see moves more than 15 feet in a single turn while within 30 feet of the Slaad, the Slaad can use its reaction to hurl a chunk of plaza rubble. The target must succeed on a DC 15 Dexterity saving throw or take 11 (2d10) bludgeoning damage and have its speed reduced to 0 until the end of its current turn. This reaction can target flying creatures."
```

## Encounter Notes

**Environment:** Collapsed Mercatura plaza. 20-ft-diameter crater at centre, 10 ft deep. Rubble and broken stone in a 40-ft radius. Festival cloth, splintered registration desks, dust. Dim light from the dust cloud for 2–3 rounds after detonation.

**Civilians:** 2d6 injured civilians are trapped in rubble within 30 feet of the crater at the start of combat. The Slaad attacks them if no PC is within reach. Each round a civilian is adjacent to the Slaad, roll a d6: on a 1–2, the Slaad targets that civilian instead of a PC. Rescuing a civilian from rubble takes one action and a DC 12 Athletics check.

**The Clock:** Every round of combat at the Mercatura is a round the extraction runs at the four secondary sites. After round 3, a PC who succeeds on a DC 12 Perception check hears screams from the Bridge district — a second strike point is active. After round 5, smoke is visible from Le Paludi. The party must decide: stay and kill the Slaad, or split and save people.

**Weakness — Fire/Acid:** Suppressing the regeneration is the tactical key. Jean-Claude's ranger toolkit does not include fire by default. The party needs to find it — a festival torch, a lantern, Perrin's spells if he has any fire options, or an alchemical solution from the rubble (DC 14 Investigation to find a chandler's oil stock scattered by the blast — improvised fire damage 1d6, bonus action to ignite). Reward creative fire use.

**Scaling:**
- **If the fight is too hard:** Ruk arrives after round 5 with a festival torch and a cleaver, dealing 2d6+4 slashing + 1d6 fire per round. He does not speak. He hits the thing.
- **If the fight is too easy:** the Slaad targets a cluster of trapped civilians in the rubble, forcing the party to reposition rather than focus-fire. It also uses Tongue Lash to pull a PC into the crater, creating a bad position.
- **If the party splits early:** the Slaad pursues the nearest target for 2 rounds, then loses interest and attacks civilians. It does not chase strategically — it is chaos, not tactics.

**Death:** When the Slaad dies, it does not dissolve or vanish. It falls. It bleeds iridescent fluid into the rubble. The body is real, heavy, and wrong — something from outside the planes, dead in the middle of a Tessarine commercial plaza. The summoning circle beneath the rubble is still faintly visible. Someone brought this here on purpose.

## Connections

- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] — the operation that summoned it
- [[session-04-day-5|Session 04 — Day 5]] — encounter context
- [[warren-grung-sewers|Warren — Grung in the Sewers]] — the summoning circle

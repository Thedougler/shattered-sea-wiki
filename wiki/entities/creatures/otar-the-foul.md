---
type: entity
subtype: creature
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "Otar the Foul — named Red Slaad boss (CR 8) for the Calveno raid. A red-caste slaad whose transformation stalled centuries ago, leaving him rotting and toxic. Summoned unbound through Simone's keyed circle as a chaotic distraction while the extraction runs."
created: "2026-05-30"
updated: 2026-06-02
tags:
  - combat
  - homebrew
sources:
  - Homebrew
confidence_level: high
cr: 8
aliases:
  - "Otar the Foul"
  - "The Mercatura Slaad"
  - "Simone's Slaad"
  - "Calveno Slaad"
  - "The Groundbreaker"
statblock: inline
---

# Otar the Foul

| **Named Antagonist** | **Otar** *(OH-tar)* — Red Slaad, Slaad-tongue root, guttural and blunt |

![[Otar-the-Foul.webp|Archer-style adult animated illustration, clean vector-like linework, strong ink contours, cel-shaded lighting, saturated adventure palette. Portrait, vertical composition, chest up, dramatic side-light. A massive red Slaad — a toad-like aberration with dull predatory eyes and a wide mouth of blunt teeth. Its cracked hide is perpetually mid-molt, slick with iridescent fluid seeping from deep fissures. Wisps of sickly green toxic miasma curl from the splits in its skin. The creature looks ancient and rotting — a metamorphosis that started centuries ago and never finished. Background: muted suggestion of dust, rubble, and broken stone. No text, no watermarks, no logos, no gore, no photorealism, no anime/chibi, no pixel art, no stock-photo aesthetic.]]

![[calveno-slaad-emergence-stylefix.webp|Archer-style adult animated illustration, clean vector-like linework, strong ink contours, cel-shaded lighting, poster-composition staging, expressive grounded faces, saturated adventure palette. Combat art, 16:9 widescreen cinematic. A massive red Slaad hauls itself out of a collapsed plaza crater in the Mercatura, dust and rubble cascading off its back, festival cloth tangled around one arm, mouth open in a roar that scatters a majority-human Calveno crowd with visible minority populations of Rattkin, lizardfolk, aarakocra, elves, dwarves, and orcs. Show the crater, broken cobblestones, festival lanterns, and civilians fleeing at the edges; no gore. No written symbols or labels. Negative constraints: no text, no watermarks, no logos, no gore, no photorealism, no anime/chibi, no pixel art, no stock-photo aesthetic.]]

Not a nameless Red Slaad pulled from Limbo at random. Simone's summoning circle was keyed to a specific resonance — what it called through has a name among the few planar scholars who catalogue individual slaadi: Otar the Foul.

Otar is a red slaad whose caste transformation stalled centuries ago. The progression — red to blue to green to grey — never completed. He stayed red, and he rotted. The foulness is literal: a miasma of toxic gas, the byproduct of a metamorphosis that started and never finished. His skin is cracked and perpetually mid-molt. His blood runs thicker and more corrosive than any standard red slaad's.

No control gem, no binding, no leash. Released into a collapsing plaza full of panicking civilians. The circle's construction used techniques the Grung did not develop themselves; the contractor who built it knew exactly what they were summoning. That contractor is an open question.

## Design Intent

The party trivialized Barnaby Rook via environmental repositioning (gusts, thrown objects) and the whip shark through concentrated damage output. Otar is built to punish both patterns:

- **Foul Miasma** makes melee range costly — 1d6 poison per turn just for standing near him. Melee-heavy parties pay a tax; ranged parties lose nothing, which is why Tongue Lash exists.
- **Entropic Regeneration** (10 HP/round, suppressed only by fire or acid) demands sustained pressure — they cannot burst him in two rounds and move on.
- **Tongue Lash** (30 ft. grapple + pull) counters ranged kiting, specifically threatening Jean-Claude's preferred distance.
- **Chaos Pulse** punishes clustering and concentration, forcing the party to spread.
- **Legendary actions (2/round)** give Otar between-turn reactivity without making him tactical. Lash pulls someone in, Thrash clears melee, Bile Spray punishes clustering — all reflexive, none smart.
- **Lair actions** represent the unstable plaza, not Otar's intelligence.

The fight should feel like containing a disaster, not outmaneuvering a commander. Every round the party spends on Otar is a round the extraction at the four secondary sites runs unopposed. The real boss is the clock.

## Behavioral Profile

- **Opening move:** Emerges from crater. Tongue Lash the nearest visible creature, pull into melee range, then close. If 3+ creatures cluster within 20 feet, opens with Chaos Pulse instead.
- **Escalation (75 HP):** Unstable Form activates — skin splits, melee attacks gain acid, attackers take acid splash. Combined with Foul Miasma, melee range now costs ~9 damage per round passively. Otar becomes more erratic, moving toward the largest cluster of creatures.
- **Legendary actions:** Not tactical choices. Otar lashes reflexively at motion (Lash), thrashes when surrounded (Thrash), and vomits when pressured (Bile Spray). The DM picks whichever feels most chaotic.
- **Morale:** None. Does not retreat, surrender, or reason. Fights until dead.
- **Role:** Brute / hazard. Tactical personality: Chaotic — an obstacle, not an opponent.

![[otar-action.webp|Archer-style adult animated illustration, clean vector-like linework, strong ink contours, cel-shaded lighting, poster-composition staging, saturated adventure palette. Full body action shot, widescreen cinematic composition. A massive red Slaad mid-rampage in a collapsed Mediterranean-style plaza — full body visible, toad-like hulking form, cracked hide perpetually mid-molt with iridescent fluid weeping from deep fissures. Its impossibly long tongue lashes out toward a fleeing figure in the distance. Sickly green toxic miasma billows from splits in its skin, pooling at its feet. Broken cobblestones, splintered festival stalls, and dust clouds surround it. One clawed foot planted on a crushed registration desk. The creature is ancient, rotting, and unstoppable — chaos incarnate, not intelligent. Dramatic low-angle perspective emphasizing its bulk. No text, no watermarks, no logos, no gore, no photorealism, no anime/chibi, no pixel art, no stock-photo aesthetic.]]

```statblock
layout: Basic 5e Layout
name: "Otar the Foul"
size: Large
type: aberration
alignment: "chaotic neutral"
ac: 15
ac_note: "natural armor"
hp: 152
hit_dice: "16d10 + 64"
speed: "40 ft., climb 20 ft."
stats: [20, 12, 18, 5, 8, 6]
saves:
  - constitution: 7
  - strength: 8
skillsaves:
  - athletics: 8
  - perception: 2
damage_resistances: "cold, lightning, thunder"
condition_immunities: "charmed, frightened"
senses: "darkvision 60 ft., passive Perception 12"
languages: "Slaad (does not communicate)"
cr: 8
source: "Homebrew — Shattered Sea"
traits:
  - name: Foul Miasma
    desc: "Otar exudes a 10-foot radius of noxious fumes — the byproduct of a stalled caste transformation. The area is lightly obscured. Creatures other than Otar that start their turn in the miasma take 3 (1d6) poison damage."
  - name: Entropic Regeneration
    desc: "Otar regains 10 hit points at the start of its turn if it has at least 1 hit point. If Otar takes fire or acid damage, this trait doesn't function at the start of its next turn."
  - name: Legendary Resistance (1/Day)
    desc: "If Otar fails a saving throw, it can choose to succeed instead."
  - name: Magic Resistance
    desc: "Otar has advantage on saving throws against spells and other magical effects."
  - name: Unstable Form
    desc: "When Otar is reduced to half its hit points (75 HP) or fewer, its skin splits and weeps iridescent fluid. Its melee attacks deal an additional 1d6 acid damage, and any creature that hits it with a melee attack within 5 feet takes 5 (1d10) acid damage."
actions:
  - name: Multiattack
    desc: "Otar makes three attacks: one Bite, one Claw, and one Tongue Lash. It can replace the Tongue Lash with a second Claw attack."
  - name: Bite
    desc: "Melee Weapon Attack: +8 to hit, reach 5 ft., one target. Hit: 14 (2d8 + 5) piercing damage. On a hit, the target must succeed on a DC 15 Constitution saving throw or be infected with a Slaad egg (Slaad Tadpole disease — no immediate effect; 3 months to manifest)."
  - name: Claw
    desc: "Melee Weapon Attack: +8 to hit, reach 10 ft., one target. Hit: 12 (2d6 + 5) slashing damage."
  - name: Tongue Lash
    desc: "Melee Weapon Attack: +8 to hit, reach 30 ft., one target. Hit: 9 (1d8 + 5) bludgeoning damage, and the target must succeed on a DC 16 Strength saving throw or be pulled up to 25 feet toward Otar and grappled (escape DC 16). Otar can grapple one creature this way at a time."
  - name: "Chaos Pulse (Recharge 5-6)"
    desc: "Otar slams both fists into the ground. Each creature within 20 feet must make a DC 15 Dexterity saving throw. On a failure, a creature takes 22 (4d10) force damage and is knocked prone. On a success, a creature takes half damage and isn't knocked prone. Rubble and debris in the area become difficult terrain."
reactions:
  - name: Rubble Surge
    desc: "When a creature Otar can see moves more than 15 feet in a single turn while within 30 feet of it, Otar can use its reaction to hurl a chunk of plaza rubble. The target must succeed on a DC 15 Dexterity saving throw or take 11 (2d10) bludgeoning damage and have its speed reduced to 0 until the end of its current turn. This reaction can target flying creatures."
legendary_actions:
  - name: ""
    desc: "Otar can take 2 legendary actions, choosing from the options below. Only one legendary action can be used at a time and only at the end of another creature's turn. Otar regains spent legendary actions at the start of its turn."
  - name: Lash
    desc: "Otar makes one Tongue Lash attack."
  - name: Thrash
    desc: "Otar thrashes violently. Each creature within 5 feet must succeed on a DC 16 Strength saving throw or be pushed 10 feet and knocked prone."
  - name: Bile Spray (Costs 2 Actions)
    desc: "Otar vomits a 15-foot cone of caustic bile. Each creature in the cone must succeed on a DC 15 Constitution saving throw or take 10 (3d6) acid damage."
```

## Lair Actions — The Shattered Plaza

The summoning circle's detonation left the Mercatura plaza structurally unsound. These effects are not controlled by Otar — they happen because the ground is falling apart. On initiative count 20 (losing ties), one of the following effects occurs. The same effect can't occur two rounds in a row.

- **Aftershock.** The crater groans and shifts. Each creature on the ground within 15 feet of the crater edge must succeed on a DC 13 Dexterity saving throw or fall prone.
- **Choking Dust.** A plume of pulverized stone erupts from the rubble. A 15-foot-radius sphere centered on a point within the plaza becomes heavily obscured until initiative count 20 of the next round.
- **Masonry Collapse.** A section of wall or archway gives way. One creature within 40 feet of the crater (DM's choice) must succeed on a DC 13 Dexterity saving throw or take 7 (2d6) bludgeoning damage and be restrained by rubble (escape DC 13, or another creature can use an action to free them).

## Encounter Notes

**Environment:** Collapsed Mercatura plaza. 20-ft-diameter crater at centre, 10 ft deep. Rubble and broken stone in a 40-ft radius. Festival cloth, splintered registration desks, dust. Dim light from the dust cloud for 2–3 rounds after detonation.

**Civilians:** 2d6 injured civilians are trapped in rubble within 30 feet of the crater at the start of combat. Otar attacks them if no PC is within reach. Each round a civilian is adjacent to Otar, roll a d6: on a 1–2, Otar targets that civilian instead of a PC. Rescuing a civilian from rubble takes one action and a DC 12 Athletics check. Foul Miasma affects civilians too — a trapped civilian inside the 10-foot radius takes 1d6 poison per round.

**The Clock:** Every round of combat at the Mercatura is a round the extraction runs at the four secondary sites. After round 3, a PC who succeeds on a DC 12 Perception check hears screams from the Bridge district — a second strike point is active. After round 5, smoke is visible from Le Paludi. The party must decide: stay and kill Otar, or split and save people.

**Lair Actions:** Run one lair action per round on initiative 20. Don't repeat the same effect two rounds in a row. Choking Dust is the most tactically interesting — it blocks Jean-Claude's sight lines and can obscure civilians the party is trying to rescue. Aftershock punishes melee PCs near the crater. Masonry Collapse creates rescue-or-fight tension (a restrained PC needs help). All three are mild enough to run without slowing the fight.

**Legendary Actions:** Otar gets 2 per round. These are reflexive, not tactical — use Lash when a PC moves to range, Thrash when surrounded in melee, Bile Spray when pressured and a cluster presents itself. Never use them strategically. Otar is not smart enough to optimize.

**Weakness — Fire/Acid:** Suppressing the regeneration is the tactical key. The party has no innate fire or acid damage. They need to find it — a festival torch, a lantern, Perrin's spells if he has any fire options, or an alchemical solution from the rubble (DC 14 Investigation to find a chandler's oil stock scattered by the blast — improvised fire damage 1d6, bonus action to ignite). Otar's own Bile Spray deals acid damage — if it hits a PC near Otar, the splash suppresses Otar's own regen. He's too dumb to avoid this. Reward creative fire use. With fire, the fight takes 5–6 rounds. Without it, 6–7.

**Scaling:**

- **If the fight is too hard:** Ruk arrives after round 4 with a festival torch and a cleaver, dealing 2d6+4 slashing + 1d6 fire per round. He does not speak. He hits the thing.
- **If the fight is too easy:** Otar targets a cluster of trapped civilians in the rubble, forcing the party to reposition rather than focus-fire. Uses Tongue Lash to pull a PC into the crater, creating a bad position. Uses Thrash legendary action to clear melee and charge toward civilians.
- **If the party splits early:** Otar pursues the nearest target for 2 rounds, then loses interest and attacks civilians. It does not chase strategically — it is chaos, not tactics.

**Death:** When Otar dies, the lair actions cease. It does not dissolve or vanish. It falls. It bleeds iridescent fluid into the rubble. The body is real, heavy, and wrong — something from outside the planes, dead in the middle of a Tessarine commercial plaza. The summoning circle beneath the rubble is still faintly visible. Someone brought this thing here on purpose, and they knew its name.

## Connections

- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] — the operation that summoned Otar
- [[session-04-day-5|Session 04 — Day 5]] — encounter context
- [[warren-grung-sewers|Warren — Grung in the Sewers]] — the summoning circle
- [[simone-tabarnack|Simone Tabarnack]] — contracted the summoning
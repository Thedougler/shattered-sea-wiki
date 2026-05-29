---
title: Ridgeback
statblock: inline
name: Ridgeback
type: monster
subtype: boss
publish: false
created: 2026-05-16
updated: 2026-05-16
summary: "CR 8 elemental serpent from the Plane of Water — the second entity through the Maw fissure. Territorial tribute-warden: attacks vessels that cross its claimed water without offering. Ship-scale grappler and hull-wrecker. Announces approach via visible rolling humps. Players have no knowledge of it yet."
aliases:
  - The Ridgeback
  - The Roller
  - The Hump
tags:
  - creature
  - elemental
  - aquatic
  - boss
  - bestiary
  - cr8
  - planar
campaign: shattered-sea
audience: dm
cr: 8
confidence_level: high
region: maw
sources:
  - Homebrew
relationships:
  - relation: entered_through
    target: Maw Fissure
  - relation: hunts_in
    target: The Drowned Maw
  - relation: known_to
    target: Auralis
  - relation: distinct_from
    target: Leviathan
---

# Ridgeback

![[Ridgeback.webp|Ridgeback rolling toward a ship, three matte-black humps breaking the Shattered Sea surface]]

> See [[content/shattered-sea/situations/active/Pearl-of-Souls|Maw Fissure]] for the planar context of this creature's arrival.

```statblock
layout: Basic 5e Layout
name: Ridgeback
size: Huge
type: elemental
subtype: ""
alignment: unaligned
ac: 15
ac_class: natural armour
hp: 138
hit_dice: "12d12 + 60"
speed: "10 ft., swim 50 ft."
stats: [24, 8, 20, 4, 14, 5]
saves:
  - strength: 10
  - constitution: 8
skillsaves:
  - perception: 5
  - stealth: 2
damage_resistances: "cold, lightning"
condition_immunities: "prone, exhaustion"
senses: "blindsight 60 ft., passive Perception 15"
languages: "—"
cr: 8
source: "Homebrew"
traits:
  - name: "Planar Camouflage"
    desc: "The naitaka's scales are non-reflective jet black. While fully submerged, it has advantage on Dexterity (Stealth) checks. Creatures without darkvision or blindsight have disadvantage on Wisdom (Perception) checks to locate it in deep water."
  - name: "Rolling Wake"
    desc: "When the naitaka moves at its full swim speed while within 30 feet of the water's surface, its undulating body creates a series of arching humps that break the surface. Any creature with line of sight to the water can spot this from up to 1 mile away in clear conditions. The naitaka cannot suppress this while moving at speed."
  - name: "Deep Warden"
    desc: "The naitaka senses vibrations through water with preternatural precision. It is aware of any vessel larger than a rowboat moving through water within 500 feet of it. If a vessel passes through this range without tribute being offered to the deep — objects of meaningful weight dropped deliberately into the water — the naitaka pursues that vessel as prey until it clears the claimed area or offers tribute."
  - name: "Siege Monster"
    desc: "The naitaka deals double damage to objects and structures."
  - name: "Water Breathing"
    desc: "The naitaka can breathe only underwater."
actions:
  - name: Multiattack
    desc: "The naitaka makes one Bite attack and one Tail Slam attack."
  - name: Bite
    desc: "Melee Weapon Attack: +10 to hit, reach 15 ft., one target. Hit: 25 (4d8 + 7) piercing damage. The target is Grappled (escape DC 18). Until this grapple ends, the naitaka cannot use Bite against another target."
  - name: Tail Slam
    desc: "Melee Weapon Attack: +10 to hit, reach 20 ft., one target. Hit: 20 (3d8 + 7) bludgeoning damage. If the target is a creature, it must succeed on a DC 17 Strength saving throw or be knocked prone."
  - name: "Crushing Coil (Recharge 5–6)"
    desc: "The naitaka wraps its body around a vessel section or one creature within 20 feet. A targeted creature must succeed on a DC 17 Strength saving throw or take 35 (10d6) bludgeoning damage and be Restrained until the start of the naitaka's next turn; on a success, the creature takes half damage and is not Restrained. A targeted vessel section takes 35 bludgeoning damage (70 as a siege monster)."
legendary_actions:
  - name: ""
    desc: "The naitaka can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. Spent legendary actions are regained at the start of each turn."
  - name: "Detect"
    desc: "The naitaka makes a Wisdom (Perception) check."
  - name: "Thrash"
    desc: "One creature currently Grappled by the naitaka takes 14 (2d6 + 7) bludgeoning damage."
  - name: "Broach (Costs 2 Actions)"
    desc: "The naitaka surges upward, arching its full body out of the water. Each creature within 20 feet must succeed on a DC 17 Dexterity saving throw or take 14 (4d6) bludgeoning damage and be knocked prone. The naitaka can then move up to half its swim speed."
```

---

## Overview

The ridgeback is the second entity to follow the Pearl of Souls signal through the Maw fissure. Its type, behaviour, and origin are unknown to anyone in the Shattered Sea. Auralis knows something crossed. The High Eyrie instruments logged an anomaly. The two missing Sentinels did not report in. Beyond that, nothing is established above the waterline.

It is a Huge elemental serpent from the Plane of Water. At CR 8 it is designed as a solo boss encounter for a party of four level 5 characters on their ship. It fights on the surface, threatens hull integrity directly, and grapples crew while damaging the vessel simultaneously. Its key departure from the Leviathan: it does not ambush and it does not stay deep. It approaches on the surface, visible, and it expects crossing vessels to pay.

---

## Appearance

*Use this section as a ready-made NPC voice if the party locates Corris. He doesn't volunteer the story. Wibowo's, late, after enough drinks that the memory feels distant but not yet safe — that's when you get it.*

The man doesn't look like someone who survived something. He looks like someone who is surviving it, present tense, every day. When you ask what it looked like, he sets his cup down and takes a slow breath.

"The humps," he says. "That's what you see first. Three of them, rolling up out of the water one after the next, like the spine of something enormous breaking the surface. Each one wide as this room across. Moving toward you. Slow." He doesn't drink. Just holds the cup. "It didn't need to hurry."

"You stand at the rail and you do the math. How long does something have to be to put up three of those, spaced that far apart. The math keeps coming back wrong."

A pause.

"Black. Not dark — black. The kind that doesn't give anything back. You look right at it and there's just nothing there. Like someone cut a hole in the water and the hole decided to move."

Another pause. Longer.

"I didn't see the head clearly. I saw something. Wide. Wider than it was tall, and lower in the water than you'd expect. Things hanging off the front of it, like weed trailing in a current, except they weren't moving like weed." He finally drinks. "I didn't look long. By the time it was close enough to see clearly, I was watching the midship rail bend inward. Planks don't do that. Rails don't do that. Not from a wave. Not from an impact. Something held on and pushed."

---

## Behavior

It does not ambush. It announces itself. The humps appear on the horizon, roll toward the ship, and close the distance at a pace that is neither slow nor panicked. There is time to make a decision before it arrives. That is part of what it is.

Nobody in the Shattered Sea knows yet what the correct response is. The one ship that survived did so because a terrified deckhand started throwing valuables into the water in a panic, and the creature let go. Whether that was the cause or a coincidence has not been established. The DM should treat tribute as mechanically real while keeping the world's understanding of it at zero.

In combat it grapples first. The bite is for holding; the Crushing Coil is for hull seams. It can wrap itself around the midship section of a brig and apply the kind of pressure that separates planks. If the vessel starts taking structural damage, crew behaviour becomes easier to predict. Crew who jump overboard are already in the water with it.

It will disengage if reduced below 40 HP, diving and not returning. It does not chase ships that flee at speed once they clear its claimed water.

**Tribute mechanic**: If a creature aboard a targeted vessel throws an object of meaningful weight (weapons, tools, coinage, livestock) into the water, the ridgeback stops its approach for 1d4 rounds and reassesses (Wisdom DC 14). On a success it disengages. On a failure it resumes. The DM decides what counts as sufficient — a copper piece is not the same as a sword.

---

## Lore

The name comes from the *Pale Commission*, a Midchain packet that made it back to Kalowe with four survivors and a story that has been moving through the harbour taverns for the past several weeks. They describe rolling dark arches on the water — one, then another thirty feet behind, then a third — moving toward them across the Maw crossing. The crew were calling it the ridgeback before they understood what they were looking at. The name stuck because nobody who heard the story wanted to get closer to it than a name.

The *Pale Commission* account is the only one with survivors.

The *Oaken Till* went down in the outer Maw six weeks prior, inbound from the Outer Reach. Last sighted by the crew of the *Narrow* making good speed in clear weather. The *Narrow*'s log notes "a series of dark shapes on the horizon, possibly debris, possibly animals, moving against the wind." The *Oaken Till* was never sighted again. No wreckage recovered.

The *Halcrow* and *Pellin's Hand* both went down within a fortnight of each other on the western Maw approach. Different routes, different weather, no connection between the vessels or their crews. Both were routine crossings. Neither sent up signals that anyone reported hearing. The *Halcrow* had made the Maw crossing a dozen times in the past three years.

The *Sorn Packet* is the most recent and the least certain. It is possible it ran aground on the Maw rim in poor visibility and has nothing to do with any of this. It is also possible it did not.

What the *Pale Commission* crew actually describe: the humps circled the vessel at distance for several minutes before closing. The hull began to creak. One section of the midship rail was pushed inward by something below — not a wave strike, a sustained squeeze that popped two hull planks before it stopped. A deckhand named Corris — described by the other survivors as not entirely coherent at this point — began screaming pledges to a god he had apparently decided to adopt on the spot, throwing everything loose into the water. His coins first. His boots. A bronze fitting he tore off the compass housing. The constriction stopped. Whatever was in the water disappeared.

The *Pale Commission* made Kalowe in twelve hours on a following wind, short two planks and a deckhand who has not spoken publicly about the experience since.

Whether it was the offerings, the noise, the god, or something else entirely that caused the creature to release them is not established. Corris himself does not claim to know.

---

## Related Pages

- [[content/shattered-sea/situations/active/Pearl-of-Souls|Maw Fissure]]
- [[content/shattered-sea/beastiary/sea-life/Leviathan|The Leviathan]]
- [[content/shattered-sea/places/tail/Drowned-Maw|The Drowned Maw]]
- [[Auralis]]
- [[content/shattered-sea/situations/active/Pearl-of-Souls|Pearl of Souls]]
- [[content/shattered-sea/items/Clydes-Bestiary-of-Oceanic-Creatures|Clyde's Bestiary of Oceanic Creatures]] — Ch. 9

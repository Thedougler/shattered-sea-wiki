---
title: Moucheron
type: monster
publish: false
created: 2026-05-15
updated: 2026-05-16
summary: A Pointy Hat fey mercenary from the Plane of Faerie that feeds exclusively on blood — pays are negotiated in bloodletting, not gold; highly social when fed, vicious when starved.
tags:
  - creature
  - fey
  - bestiary
campaign: shattered-sea
audience: dm
subtype: monster
confidence_level: high
aliases:
  - Moucheron
sources:
  - Homebrew
  - Pointy Hat
cr: 8
creature_type: fey
cssclasses:
  - wiki-monster
relationships:
  - relation: listed_in
    target: Bestiary
  - relation: native_to
    target: Murrat
  - relation: hires_from
    target: Kalowe
  - relation: classified_pest_by
    target: Dravosi Crown
---

# Moucheron

![[Moucheron.webp|A mosquito-like fey mercenary with four blades and a blood-drawing proboscis]]

```statblock
layout: Basic 5e Layout
name: "Moucheron"
size: Small
type: fey
alignment: Any
ac: 16
hp: 130
hit_dice: 20d6 + 60
speed: "30 ft., fly 60 ft."
stats: [12, 19, 17, 14, 14, 13]
saves:
  - dexterity: 7
  - constitution: 6
skillsaves:
  - acrobatics: 7
  - perception: 5
senses: "Darkvision 60 ft., Passive Perception 15"
languages: "Common, Sylvan"
cr: "8"
traits:
  - name: "Magic Resistance"
    desc: "Advantage on saving throws against spells and other magical effects."
  - name: "Sanguivore — Satiated"
    desc: "If the Moucheron hit with its Stinger last turn: no opportunity attacks against it, and AC becomes 17."
  - name: "Sanguivore — Voracious"
    desc: "If the Moucheron did not hit with its Stinger last turn: +1 bonus to all attack and damage rolls."
actions:
  - name: "Multiattack"
    desc: "Four Fey Blade attacks. Can replace one with a Stinger attack."
  - name: "Fey Blade"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 14 (3d6+4) piercing damage."
  - name: "Stinger"
    desc: "Melee Weapon Attack: +7 to hit, reach 5 ft. Hit: 11 (2d6+4) piercing damage."
  - name: "Feeding Frenzy (2/Day, Bonus Action)"
    desc: "After hitting a Bloodied creature with Stinger, gain both Satiated and Voracious benefits simultaneously until the end of next turn."
```

---

## Lore

Native to [[Murrat|Murrat]] and the surrounding reef islands in the [[Midchain|Midchain]]. Villages are built into cliff faces and canopy — several per island, each a separate kin-group running its own blood economy. Within the community, bloodletting is formal and consensual: it settles debts, pays for skilled work, and marks agreements. A Moucheron who takes from a non-consenting creature has broken social law, not just etiquette, and they take that seriously.

Murrat itself is hostile to outsiders — the island Moucherons attack anything that lands and don't distinguish between fauna and people. The ones who leave and work as mercenaries in the wider Midchain are the same creature. They've just learned that fighting other people's wars pays better than hunting.

**Mercenary work.** Moucheron squads hire out of [[Kalowe|Kalowe]] in groups of three to six. They are reliable: they don't break contracts, they don't abandon clients under fire, and the feeding terms are stated upfront. The caveat is the bloodless job — if a fight doesn't materialize, the feeding clause still stands. A good contract specifies what happens in that case. Captains who skip that line item find out why it matters.

**Dravosi classification.** The [[Dravosi-Crown|Dravosi Crown]] classifies Moucherons alongside [[Rattkin|Rattkin]] under species bounty in Crown territories, but files them separately as hazardous wildlife removal at a higher rate. The Crown has not successfully collected on Murrat.

---

## Blood Requirements

**What counts as a feeding:**
- **Full feed** — drawing blood in combat (at least one Stinger hit connecting), or a consensual draw from a willing Medium or larger creature (~10 hp blood loss). Satisfies the daily requirement.
- **Keep** — one sealed clay vessel of preserved blood. Counts as a full feed for the day. A Moucheron with keeps on hand can go that many days without a live source before the clock starts.
- **Partial feed** — blood-based drinks like the Red Flat or Shark Pull. Does not satisfy the daily requirement but delays progression by one day if consumed that day.

**The clock — consecutive days without a full feed or keep:**

| Days unfed | State | Behavior | Mechanical |
|---|---|---|---|
| 0 | **Satiated** | Fed today. Normal, sociable, professional. | Sanguivore — Satiated active in combat. |
| 1 | **Hungry** | Irritable. Pushing for a job. Will ask for a willing draw. | Sanguivore — Voracious active. Satiated lost. |
| 2 | **Difficult** | Contract discipline straining. Lingers near wounded creatures. Will feed on animals without asking. Visible to everyone in the room. | Voracious only. −2 to all Charisma checks. |
| 3 | **Desperate** | Biology overrides contract. Will feed on any available creature. Will not attack a client first but will not stop if one bleeds in front of them. | Voracious only. Disadvantage on Wisdom saves. Advantage on attacks against any bloodied creature. |
| 4+ | **Starving** | No control. Attacks to feed. Takes 1d8 necrotic per day. Dies at 0 hp. | All above, plus 1d8 necrotic/day. |

**Keeps.** Moucherons carry small sealed clay vessels called keeps — a Murrat-derived term, used in Common by any integrated Moucheron. Before sealing, they add a drop of fluid from the stinger, which carries the same anticoagulant property that prevents blood from clotting during a live feed. This keeps the contents liquid and viable for **2 days at ambient temperature, 3 if kept cool**. A keep holds roughly one partial feed's worth of blood. Integrated Moucherons typically carry 2–3 on their person. A full feed requires two keeps consumed together, or one keep plus a live draw.

Keeps are how the [[Five-Blades|Five Blades]] bridge gaps between contracts. Reweti's clay pot behind the bar is essentially a large, un-stoppered keep that she refreshes regularly from the butcher on the second island. It's not a trade good and not sold, but a Moucheron who is a known regular can ask.

**Notes for the DM:**
- The Five Blades carry 2–3 keeps each, meaning they can go 2–3 days without a contract before hitting Hungry. Varet's job is ensuring keeps are stocked and jobs don't run out simultaneously.
- Partial feeds from the Red Flat and Shark Pull are why Reweti stocks them — it's harm reduction, not hospitality.
- A Moucheron at Difficult or worse will not lie about their state if asked directly. They consider it a contractual disclosure.
- Death at the Starving stage is real. A Moucheron that goes 9+ days without blood and has no keeps dies. It happens on Murrat occasionally, during lean seasons.

---

## Related

- [[content/shattered-sea/beastiary/fey/index|Fey Bestiary]]
- [[Kalowe|Kalowe]] — primary Midchain hiring port for Moucheron mercenary groups
- [[Dravosi-Crown|The Dravosi Crown]] — classifies Moucherons under hazardous wildlife removal bounty
- [[Rattkin|Rattkin]] — similarly classified by the Crown; lower bounty tier

## Source

- Pointy Hat — The Moucheron

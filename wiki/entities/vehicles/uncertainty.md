---
type: entity
subtype: vehicle
campaign: shattered-sea
status: active
audience: dm
publish: false
title: Uncertainty
summary: "Tier 1 patrol cutter, formerly HCS Surety — repainted, renamed, and refitted at La Vasca by Cobb on Nona Black-Jaw's account. Ram bow, shallow keel (4 ft draft), all facilities installed. Captained by Delmar Fisk. Currently in dry dock."
created: 2026-05-28
updated: 2026-05-28
tags: [vehicle, ship, tier-1, prize, active_arc]
sources: ["Inbox/Uncertainty.md", "Inbox/Session-01-Recap.md", "Inbox/Session-03-Recap.md"]
confidence_level: high
relationships:
  - relation: formerly_was
    target: "[[hcs-surety|HCS Surety]]"
  - relation: captained_by
    target: "[[delmar-fisk|Delmar Fisk]]"
  - relation: refitted_by
    target: "[[cobb|Cobb]]"
  - relation: commissioned_by
    target: "[[nona-black-jaw|Nona Black-Jaw]]"
ship_class: patrol cutter (private registry)
captain: "[[delmar-fisk|Delmar Fisk]]"
home_port: "[[la-vasca|La Vasca]], Calveno"
current_location: "[[la-vasca|La Vasca]], Calveno — refit complete, dry dock"
tier: 1
hull_points: 130
hull_ac: 11
cssclasses:
  - wiki-ship
---

# Uncertainty

> [!read-aloud]
> She rides level in the water — freshly caulked, brown-black paint from cap rail to copper, no flag flying. The bow carries a ram plate fitted flush with the waterline, iron-edged, and above it a carved hardwood figure: a woman mid-stride, hands empty, face forward. Two cannon sit amidships, swivel guns fore and aft. From a distance she reads as a working coastal vessel. That is the point.

---

## Overview

The *Uncertainty* is the former [[hcs-surety|HCS Surety]] — a Dravosi Crown patrol cutter taken as a prize in Session 01, damaged by a whip shark in Session 03, and fully refitted at [[la-vasca|La Vasca]] under [[cobb|Cobb]]'s direction on [[nona-black-jaw|Nona Black-Jaw]]'s account. All Crown identity has been removed. Repainted, renamed, fitted with a ramming prow, equipped with a new figurehead, and stocked for extended operation.

Nona's standing instruction: *the ship leaves La Vasca complete or it does not leave.* After her grandson nearly died on the last run, she is not interested in moderation.

She is fast for her size, nimble in reef passages, and can operate in four feet of water — shallower than any Crown vessel of her class. The ram is not subtle. Everything else is.

---

## Stats

| Stat | Value |
|---|---|
| **Tier** | 1 |
| **Type** | Patrol cutter (private registry) |
| **Variant** | Armed + Ram Bow + Shallow Keel |
| **Hull Points** | 130 |
| **Hull AC** | 11 (forward hull vs. head-on strikes: 13) |
| **Condition** | Pristine |
| **Speed (good wind)** | 70 miles/day |
| **Speed (poor wind)** | 30 miles/day |
| **Draft** | 4 ft minimum (standard cutter: ~8 ft) |
| **Speed (calm, oars)** | 15 miles/day |
| **Maneuverability** | Average |
| **Profile** | Low |
| **Cargo** | 15 tons rated |
| **Crew (min / full)** | 4 / 10 |
| **Gun Mounts** | 4 (2 per side) |
| **Weapons** | 2 × cannon (amidships); 2 × swivel gun (bow, stern); Ram |
| **Weekly Upkeep** | ~32 gp |
| **Facility Space** | 4 / 4 units used (Tier 1 maximum) |

> [!dm]
> HP increase from 120 → 130 reflects reinforced forward section — doubled planking and iron framing forward of the beam. Structural, not magical.

---

## Refit Modifications

### Identity Erasure

All Crown identity removed or destroyed:
- **Registry plate** cut and melted down at La Vasca
- **Stern board** re-carved: *Uncertainty* in Calveno Roman script
- **Paint** stripped and repainted: weathered brown-black, no markings, no waterline stripe
- **Pennant and signal flags** locked away below; nothing flies
- **Interior markings** scraped; Crown charts redrawn with Calveno notation

What cannot be fully hidden: the hull silhouette. A Crown cutter's profile is distinctive to anyone who served on this class. Paint and name handle port authority at a glance. They do not handle a Dravosi naval officer who knows what to look for. See [[hcs-surety-dm-guide|DM Guide]] for Crown recognition timeline.

### Ram Bow

Forward hull rebuilt with doubled planking, iron-pin cross-bracing, and an iron-capped ram plate running three feet along the keel.

> [!mechanic]
> **Ram Attack.** Helmsman's action. Ship must move 20+ feet in a straight line before the strike. Both ships take **2d10 bludgeoning**; *Uncertainty* takes half (reinforced bow). Tier 1 or smaller target: **DC 13 Strength save** or pushed 15 ft and next turn's movement halved. Forward hull has **AC 13** vs. head-on strikes only.

### Shallow Keel

Keel depth reduced by 18 inches — ballast redistributed, garboard strakes faired back.

> [!mechanic]
> **Shallow Draft.** Can operate in water as shallow as **4 feet** (standard cutter minimum: ~8 ft). Opens river mouths, tidal flats, lagoon approaches, and Calveno's inner canal network. Helmsman has **advantage** on Dex checks to navigate reef channels. Trade-off: Speed (poor wind) 30 miles/day instead of 35.

### Figurehead

Lost to the whip shark in Session 03. Replaced by a Le Paludi canal-ship carver on Nona's account. A woman, mid-stride, hands open at her sides. Calveno features. No expression of hope or fear. She is simply going. She is not named.

---

## Crew

| Role | Filled By | Notes |
|---|---|---|
| Captain | [[delmar-fisk\|Delmar Fisk]] | PC |
| Bosun | [[old-faas\|Old Faas]] | Rated bosun. Two peg legs. Faster on the rigging than before. |
| Gunner | [[thunk\|Mr. Thunk]] | Rated gunner. Counts as two crew when manning a weapon. |
| Carpenter | [[sem-holst\|Sem Holst]] | Promoted from Carpenter's Mate after supervising the refit. |
| Carpenter's Apprentice | [[geoffrey-draves\|Geoffrey Draves]] | Defected from Surety crew Session 01; retained under Sem. |
| Navigator | — | Unfilled. Crissdalynn partially covers on known routes. |
| Cook | — | Unfilled. No long-rest HP recovery bonus at sea. |
| Surgeon | — | Unfilled. [[alys-kuiper\|Alys Kuiper]] did not return from shore leave. Berth installed; benefits locked. |

> [!dm]
> Immediate gaps: Cook (cheap at 4 gp/week, closes a real gap), Surgeon (unlocks Surgeon's Berth), Navigator (partially covered). [[oleandro-fuschi\|Oleandro]] at Ponte Bassa knows every working sailor who has eaten there. [[cobb\|Cobb]] can provide Passage-vouched candidates if Perrin asks.

---

## Facilities

All four Tier 1 facility slots installed on Nona's account.

| Facility | Space | Notes |
|---|---|---|
| Surgeon's Berth | 1 | Forward of officer cabin. Needs hireling Surgeon for full Hospital benefits; PC with Medicine proficiency can use for DC 10 treatment checks. 3 Potions of Healing from Passage supply (not restockable from standard chandlery). |
| Weapons Locker | 1 | Crown gear replaced: 8 boarding axes, 4 crossbows (20 bolts each), 6 grapple lines, 3 smoke grenades, 2 incendiary flasks. |
| Provisions Store | 2 | Stocked 30 days at full crew: salt fish, rice, dried beans, fresh citrus, water casks ×4, small beer ×2 barrels, cooking oil. Emergency ration chest (7 days for 10) — Cobb enforces it is not opened except at Nona's say-so. |

No space units remain. Tier 2 required for further facility expansion.

---

## Equipment (Non-Facility)

| Item | Notes |
|---|---|
| Signal Lantern (paired) | One mounted aft rail; partner below. 25-word messages up to 30 miles to Warren's Calveno shore contact. Passage communication standard. |
| Mending Resin ×2 | Carpenter's locker. Each repairs 2d8 Hull HP over 8 hours. Does not repair structural damage. |
| Navigational chart set | Old Crown charts of Central Strait and eastern Crown Islands. Admiralty markings scraped, Calveno notation overlaid. Coverage good; provenance gone. |
| Sem's tool kit | Carpenter's full kit. Not party property. |

---

## Crew Departures (Post-Session 03)

**Shepherd Grigori** — Departed in Calveno as planned. Within a day, two rumours circulate:

> *A dying Tessarine heir — bedridden three weeks, the family already measuring for the funeral — recovered overnight. A man came to the house after dark, drunk enough the door guard almost turned him away, and was with the patient for twenty minutes. When he left, the patient was sitting up asking for food. Nobody got a clear look. Someone says he smelled like wine and something else. Someone else says he was singing under his breath the whole time.*

The family is not publicizing this. The rumours come from the servants.

> [!dm]
> Grigori's target was the hemophiliac Tessarine heir — his Calveno business from the moment he came aboard. The healing is real; the drunk monk act is performance. See [[wiki/situations/islands/shepherd-grigori|Shepherd Grigori — DM]].

**Alys Kuiper** (Ship's Surgeon) — Did not return from shore leave. No note, no message. Berth cleared of personal effects. A Le Paludi boarding house records her checking out after a man visited on the second evening. This is the full extent of what is findable.

---

## History

Launched as **HCS Surety** under Crown registry CS-1147. Commanded by Lieutenant Barnaby Rook. Taken as a prize by the party in Session 01. Sustained significant hull damage from a whip shark in Session 03. Renamed *Uncertainty* by party decision. Dry-docked at [[la-vasca|La Vasca]], Calveno, under Cobb's supervision on Nona Black-Jaw's account. Refit completed in 5 days.

Full prior history and session log: [[hcs-surety|HCS Surety]].

---

## Connections

- [[hcs-surety|HCS Surety]] — prior identity; full session history retained there
- [[hcs-surety-layout|Deck Layouts]] — unchanged from Surety
- [[hcs-surety-owners-manual|Owner's Manual]] — player-facing rules reference
- [[hcs-surety-dm-guide|DM Guide]] — Crown recognition timeline, chase tooling, crew casualties
- [[delmar-fisk|Delmar Fisk]] — captain
- [[nona-black-jaw|Nona Black-Jaw]] — commissioned and funded the refit
- [[la-vasca|La Vasca]] — current berth and refit location
- [[cobb|Cobb]] — refit supervisor
- [[wiki/situations/islands/shepherd-grigori|Shepherd Grigori]] — former passenger; departed Calveno
- [[surety-missing|Crown Search]] — recognition clock

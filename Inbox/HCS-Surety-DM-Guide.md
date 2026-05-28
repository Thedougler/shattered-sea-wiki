---
title: HCS Surety — DM Guide
type: reference
publish: false
audience: dm
campaign: shattered-sea
created: 2026-05-19
updated: 2026-05-19
summary: DM-facing operational guide for running the HCS Surety — navigation consequences, chase tooling, crew casualties, bastion events, defence mechanics, and Crown response timeline.
tags:
  - reference
  - ship
  - mechanics
  - dm-only
sources:
  - "[[HCS-Surety]]"
  - "[[HCS-Surety-Owners-Manual]]"
  - "[[Ship-Combat]]"
  - "[[Ship-Bastion]]"
---

# HCS Surety — DM Guide

Companion to [[HCS-Surety-Owners-Manual|the player-facing Owner's Manual]]. The Manual tells players what to roll; this tells you what happens when they do.

---

## Navigation Failures

Players roll **Intelligence (Navigator's Tools)** against a DC you set. The DC table is in the Manual (10 / 14 / 18). On a failure, delay the voyage by **1d4 days** and introduce a complication scaled to the waters:

| Waters | Complication Ideas |
|---|---|
| Charted, calm (DC 10) | Minor course deviation. Bad weather front adds a day. Missed a supply stop. |
| Unfamiliar, reef approaches (DC 14) | Grounded on a sandbar (Carpenter's DC 14 to free, half-day lost). Hostile vessel spotted. A port the party intended to bypass gets threaded too close — awkward questions. |
| Maw approaches, active storm (DC 18) | Separated from landmarks in fog for 1d4 days. Emergency hull damage (**2d10**). A crew member overboard (DC 13 Athletics or lost). The compass starts behaving strangely even after the Maw. |

Don't use the same complication twice in a row. Failures in charted waters should feel inconvenient; failures in the Maw should feel dangerous.

**Crown charts and advantage.** Central Strait and Crown Islands charts are reliable — the advantage is real. Midchain charts are contradictory; grant no advantage and feel free to introduce complications even on a success if the charts are the source of the route.

---

## Chase Complications

Chases use range bands (Boarding / Cannon / Distant). Two rounds at Distant = quarry escapes. The party controls whether they're faster — if they have the faster ship, the complication is your only lever.

**Call one complication per chase.** Wait for a dramatically appropriate moment — when the gap has just closed or when escape looks certain. Don't front-load it.

| Complication Type | Check Called | Failure Result |
|---|---|---|
| Fog bank | **DC 14 Perception** (Navigator or lookout) | Both ships move to Distant regardless of speed this round; quarry may escape |
| Reef channel | **DC 14 Intelligence (Navigator's Tools)** | Pursuing ship's speed drops one band for **1d4** rounds (hull scraping) |
| Wind shift | **DC 12 Dexterity (Bosun)** | Pursuing ship loses one band of movement this round |
| Shallow draft warning | **DC 14 Intelligence (Navigator's Tools)** | Larger vessel runs aground; pursuit ends or continues by jolly boat |

For a fleeing party, the complication hits their pursuer. For a pursuing party, it hits them. Apply it where the drama is.

---

## Crew Casualties

When the ship's Hull Integrity crosses these thresholds during combat, roll for crew losses. Track which threshold has been crossed — each fires once per engagement.

| Hull Integrity Remaining | Roll |
|---|---|
| First time below 90 HP | 1 NPC crew member incapacitated |
| First time below 60 HP | **1d4** NPC crew incapacitated |
| First time below 30 HP | **2d4** NPC crew incapacitated or killed |

**PCs are never on the casualty table.** They take damage from specific attacks only, not attrition rolls.

**Announcing casualties.** Narrate the result dramatically — a cannon round through the gun deck, a swivel blast scattering the forward watch. Don't just report a number. If a named NPC crew member is involved, pull from the ship's muster. If the party has hired specific hirelings to fill roles, a casualty can take that role offline mid-fight.

**Minimum complement impact.** If casualties drop the vessel below 4 crew, all ship checks go to disadvantage and speed drops 20%. If a specific role goes unfilled mid-combat (Gunner down), apply the no-Gunner rule from the Manual immediately.

---

## Bastion — Facility Events

When a facility is assigned **Maintain**, roll a Facility Event. At sea, use the shipboard event table. In port, use the standard 2024 Bastion Events table.

| Roll (d6) | Shipboard Event |
|---|---|
| 1 | **Hostile contact.** A vessel has been tracking the Surety. Run as an encounter or have it surface at a dramatically appropriate moment. |
| 2 | **Beneficial contact.** A passing ship offers trade, intelligence, or an unexpected opportunity. |
| 3 | **Facility damage.** A storm or rough seas damage one facility. Repair requires a Carpenter's check and one day. |
| 4 | **Windfall.** Favourable current — voyage shortened by **1d4** days. |
| 5 | **Hireling issue.** A hireling has a matter requiring officer attention — a dispute, a health issue, a demand for back pay, a rumour they want to act on. |
| 6 | **Clear sailing.** No event this week. |

You can pre-roll events for a long voyage and reveal them as they occur, or roll live. The "hostile contact" result doesn't have to trigger immediately — let it surface when the timing is right.

---

## Bastion — Defence of the Vessel

When the Officer Complement is absent and a hostile action event occurs, resolve it with dice rather than play.

Roll **6d6**. Each result of **1** kills one Defender. If all Defenders are lost, one facility (your choice — pick the most narratively interesting) goes dormant for the following week.

| Vessel Condition | Defence Modifier |
|---|---|
| Officer Complement aboard | Don't roll — play it out |
| Vessel in port, complement absent | Standard 2024 bastion defence |
| Underway, full experienced crew | +3 to each die (results of 1–3 don't kill) |
| Underway, skeleton crew | No modifier |
| Underway, below minimum complement | −1 to each die (results of 1–2 kill) |

The Weapons Locker upgrades Defender dice from **d6 to d8** while stocked. Roll d8s instead when it's active.

**Keeping Defenders stocked.** A single Recruit order fills up to 12 Defenders. Don't let the party forget this — it's cheap insurance and the one rule that prevents a bad event roll from cascading. If they haven't done a Recruit order and something goes wrong while they're away, that's fair consequences.

---

## Crown Registration — Timeline

The *Surety* is registered as an active Crown patrol vessel out of [[Port-Tidefall]], under Lieutenant B. Rook, Crown commission.

- **Week 1–2:** No action. Patrol cutters sometimes run long without check-in.
- **Week 3:** Harbourmaster's Register flags the vessel as overdue. A query is sent to the nearest Crown waypoint.
- **Week 4–5:** Vessel listed as missing. Description circulated to Crown ports in the Eastern Crown Islands.
- **Week 6+:** If the ship is spotted operating under Crown colours, boarding and inspection is authorised. If operating under different colours or no colours and identified by hull or crew, it becomes a wanted vessel at Crown ports.

The party can delay this clock by operating far from Crown waters, stripping Crown markings (takes two full days in port with tools), or acquiring false papers through [[Port-Kalowe|Kalowe]] or similar channels. See [[content/shattered-sea/situations/active/Kalowe|Ship Disguise — Kalowe]].

---

## Running Notes

**When to abstract vs. play out.** Routine passages don't need navigation rolls — call for one when the waters are actually dangerous or unfamiliar, when failure would be interesting, or when the party has made a choice that deserves a consequence. Rolling to cross the Central Strait in good weather is just paperwork.

**Ship combat pacing.** Ship combat works best when boarding is the goal, not the sinking. The *Surety* at Tier 1 can't absorb extended broadside exchange with anything larger than herself — position her enemies accordingly. If the party is trying to take a prize, chain shot to slow them + grapeshot to suppress the deck + board is the intended tactical loop.

**Crew personalities.** The Surety's hired crew are not anonymous dice-absorbers. Give at least two of them names and a single trait. When casualties happen, name the ones who go down. It matters more.

**Upkeep as pressure.** The ~28 gp/week figure is a soft pressure tool, not a hard mechanic. Use it to motivate trade runs, prize-taking, and faction work. Miss a week — fine. Miss three — someone isn't getting paid and the party hears about it.

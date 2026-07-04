---
type: entity
subtype: dungeon
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: Grung blackpowder magazines and summoning circle in the sewer collectors beneath Calveno's festival districts — five detonation sites, accelerated timeline, hidden primary beneath the Mercatura.
created: 2026-06-01
updated: 2026-06-12
tags:
  - grung
  - combat
  - poison
  - dungeon
sources:
  - Homebrew
confidence_level: high
relationships: []
verb: Conceal
unstable_condition: The Le Paludi compromise accelerated the timeline — handlers are rushing final powder-packing with tighter sentry rotations, and one secondary site's scaffolding is incomplete.
consequence: If intact, all five detonations fire at crowd peak; the Mercatura plaza collapses; Otar the Foul emerges; extraction teams seize 200-300 captives, reduced by each neutralized lane.
link_of_relevance: Jean-Claude — his sister Simone built this operation; he is the only party member who can read Grung trail notation and identify caste discipline at work.
rooms: 10
cr_range: "1/4–8"
topology: loop
region: calveno
---

# Calveno Sewer Magazines — Grung Raid Infrastructure

> [!read-aloud]
> The maintenance hatch is iron, set flush with the cobblestones in a Le Paludi side street. Nona's charcoal mark stains the frame, and iron rungs fall fifteen feet into black water. Fish-oil lantern light catches wet limestone below — and something else, a faint iridescent smear on the topmost rungs, not quite oil, not quite water. The smell rises first: old brine, wet vegetation, mineral stone, and underneath all of it, something sweetly chemical that is neither canal nor rat.

![[wiki/assets/sessions/session-05/maps/session-05-calveno-sewer-magazines-overview-battlemap-realistic.png|Session 05 connected dungeon overview battlemap — all sewer magazine rooms connected through the keyed topology with a 5-foot tactical grid.]]

> [!dm]
> **Battlemap note:** The realistic Session 05 battlemap PNGs are the canonical tactical maps. One grid square is 5 feet. Dark padding is non-playable. Short corridor, pipe, hatch, and vent stubs show keyed exits; they are not additional rooms.

## Overview

[[simone-tabarnack|Simone Tabarnack]]'s Grung operatives have converted five structural weak points in Calveno's sewer collector system into blackpowder magazines, timed to detonate simultaneously during the final day of [[il-gioco-delle-beffe|La Finestra]]. Four secondary sites will buckle the ground and open extraction breaches. The primary site beneath the [[calveno|Mercatura]] will collapse the plaza and summon [[otar-the-foul|Otar the Foul]] through the rubble. The party knows about the four secondary sites from [[felix-aho|Felix Aho]]'s interrogation. The primary site is compartmentalized above his clearance.

> [!dm]
> **Session 06 framing (see [[session-06-run-guide|Session 06 Run Guide]] for the full script).** This dungeon is the back half of the campaign's current arc; the party is resuming from Room 6 after Session 05. Session 06 adds [[catarina-davirelli|Catarina Da'Virelli]] as a temporary 5th PC. She is **not** placed in a room here — she arrives via a **staggered entry** (clockwork owl + Eldritch Cannon on site first, she follows 2–3 rounds later) at *whichever site the party commits to first*. The run guide opens that arrival with one of four location-specific investigation-flashback trails — Le Paludi yards (Beta), the Bridge (Gamma), the outer quay (Delta), or the Mercatura (primary) — and runs only the one matching the party's chosen door. **Because the party is now five, the primary-chamber Otar uses the recalibrated CR 12 build — run him straight from [[otar-the-foul|Otar the Foul]].** Catarina is also unaware, on arrival, that [[jean-claude-tabarnack|Jean-Claude]] (disguised Grung defector) is a party ally; treat that as a live pressure, not a scripted reveal.

## Intel Baseline

| Source | Table-use facts |
|---|---|
| Felix, already earned | 4 secondary sites, blackpowder scaffolding, wrong 2-day estimate, purple garrisons/red leaders, 6 ships |
| Felix second pass | 32 barrels transported, 22 placed, 10 missing; exact sentry pattern; purple-only boats; "circle site" scream |
| Ruma / relay | Accelerated timeline, fifth red-caste authority marker, egress vents, sentry rotations, check-in clock |

## Access

Three entry points into the collector system:

- **Le Paludi maintenance hatch** (Room 1): The entry [[nona-black-jaw|Nona]]'s runner marked. Iron ladder, 15-ft descent. Most direct route into the network.
- **Bridge district far hatch** (connects to Room 3): At the Bridge end of the connector tunnel. Silt around the base is disturbed on both sides. Opens onto the Bridge approach of the collector system.
- **La Vasca tidal passage** (connects to Room 7): Accessible at low tide through the covered basin at [[la-vasca|La Vasca]]. Narrow, partially flooded, and slow — but bypasses the entire upper network and enters the main collector directly.

## General Features

Unless noted otherwise in a room key, these apply throughout:

- **Light:** Dim. Oil lamps behind glass at junctions (canal commission standard). Bioluminescent algae on wet stone provides faint green light. No natural light below the access shafts.
- **Ceilings:** 5–6 ft in collector tunnels (Medium creatures move normally but cannot jump). Rises to 8 ft in the main collector and 15 ft in the primary chamber.
- **Walls:** Limestone and old brick. Canal commission chalk markings at intersections (faded, maintenance notation). Grung trail notation at knee height (recent, cut into stone).
- **Sound:** Water echo carries. Combat noise in any room is audible in adjacent rooms. Stealth-critical encounters note specific DCs.
- **Smell:** Tidal brine, old stone, fish oil from the lamps. The Grung chemical signature — sweetly acrid, like overripe fruit and ammonia — increases deeper in the network. Faint in Room 1, present in Room 2, obvious by Room 4, oppressive by Room 7. Jean-Claude identifies it automatically as concentrated skin secretion runoff.
- **Water:** Ankle-deep standing water in most tunnels (difficult terrain for creatures without swim speed). Old collector sumps and channels are 2–4 ft deep where noted.
- **Grung saturation.** The Grung have lived and worked these tunnels for days. Their skin secretions coat every surface they've touched — ladder rungs, barrel lashings, rope handles — leaving a faint iridescent residue that catches lamplight. The standing water carries their chemical runoff: an oily film and a sweetly acrid smell, like overripe fruit soaked in ammonia, that worsens with depth. By Room 4 the air tastes of it — sweet, acrid, clinging to the back of the throat. By Room 7 it burns.

> [!mechanic]
> **Contact poison (environmental).** Grung-touched surfaces (rungs, ropes, barrel handles) — DC 12 CON on bare-skin contact or poisoned for 10 minutes. Gloves or cloth wrapping negates. Jean-Claude is immune (Grung physiology). Call for one roll per room when a PC handles something, not on every rung.

**Three Grung poison types (quick reference):**

| Type | Delivery | Effect | DC | Used by |
|---|---|---|---|---|
| **Contact secretion** | Bare skin on coated surface | Poisoned 10 min | 12 CON | Environmental, retreating greens |
| **Torpor extract** | 5-ft cloud (vial crack) | Speed halved 1 min | 12 CON | Elite handlers, cornered |
| **Weapon poison** | Arrow/dagger hit | +2d4 poison damage + poisoned 1 min | 12 CON | All Grung combatants |

<div style="page-break-before: always;"></div>

## Map Key

```text
Room 1 (Le Paludi Access Shaft)
  → Room 2: short service landing, 15 ft ladder up to street hatch

Room 2 (Y-Junction)
  → Room 1: north landing and ladder up
  → Room 3: right/east branch, narrowing low corridor (4 ft ceiling after 35 ft)
  → Room 4: left/southwest branch, heavier silt disturbance

Room 3 (Bridge Connector)
  → Room 2: back toward Le Paludi
  → Room 7: stone archway, tunnel widens into the main collector
  → T1: barred side culvert to Bridge district magazine

Room T1 (Magazine Gamma)
  → Room 3: barred side culvert
  → Bridge street drain: rusted grate to maintenance alcove

Room 4 (Magazine Alpha)
  → Room 2: back toward Y-junction
  → Room 6: drainage overflow pipe (4 ft diameter — crawl for Medium, walk for Small)

Room 5 (Magazine Beta)
  → Room 6: mortared breach in wall (recent — picks and dust visible)

Room 6 (Handler Relay)
  → Room 4: drainage overflow pipe
  → Room 5: mortared breach
  → Room 7: canal service corridor (6 ft ceiling, raised dry lip)
  → Room 8: hidden passage behind false wall (DC 16 Investigation behind stacked barrels; Ruma does not know it exists)

Room 7 (Main Collector)
  → Room 3: stone archway, back toward Bridge connector
  → Room 6: canal service corridor
  → Room 8: vaulted passage, descending grade
  → T2: flood overflow vent toward harbour approach magazine

Room T2 (Magazine Delta)
  → Room 7: flood overflow vent
  → Outer quay: 3-ft egress vent above waterline

Room 8 (Primary Detonation Chamber)
  → Room 7: ascending passage (main approach — the garrison watches this)
  → Room 6: hidden passage (the approach they do not watch)
```

**Common routes to the Primary Chamber:**

- **Route A — Bridge hatch:** 3 → 7 → 8 (fastest, bypasses magazines, weakest intel)
- **Route B — Le Paludi:** 1 → 2 → 4 → 6 → 7 → 8 (investigation route, finds Ruma)
- **Route C — Hidden:** 1 → 2 → 4 → 6 → 8 (direct, unguarded approach)
- **Route D — La Vasca:** 7 → 8 (slow/flooded, bypasses upper network)

---

## Map Assets

Print at 100%. Session 05 battlemap PNGs are 150 DPI; one grid square is 5 ft. Printshop packet: `.raw/sessions/session-05/session-05-calveno-sewers-printshop-packet.zip`.

| Use | Canonical file |
|---|---|
| Overview | `wiki/assets/sessions/session-05/maps/session-05-calveno-sewer-magazines-overview-battlemap-realistic.png` |
| Room 1 | `wiki/assets/sessions/session-05/maps/session-05-room-01-le-paludi-access-shaft-battlemap-realistic.png` |
| Room 2 | `wiki/assets/sessions/session-05/maps/session-05-room-02-y-junction-battlemap-realistic.png` |
| Room 3 | `wiki/assets/sessions/session-05/maps/session-05-room-03-bridge-connector-battlemap-realistic.png` |
| Room 4 | `wiki/assets/sessions/session-05/maps/session-05-room-04-magazine-alpha-battlemap-realistic.png` |
| Room 5 | `wiki/assets/sessions/session-05/maps/session-05-room-05-magazine-beta-battlemap-realistic.png` |
| Room 6 | `wiki/assets/sessions/session-05/maps/session-05-room-06-handler-relay-battlemap-realistic.png` |
| Room 7 | `wiki/assets/sessions/session-05/maps/session-05-room-07-main-collector-battlemap-realistic.png` |
| Room 8 | `wiki/assets/sessions/session-05/maps/session-05-room-08-primary-detonation-chamber-battlemap-realistic.png` |
| Room T1 (Gamma) | `wiki/assets/sessions/session-05/maps/session-05-room-t1-magazine-gamma-battlemap-realistic.png` |
| Room T2 (Delta) | `wiki/assets/sessions/session-05/maps/session-05-room-t2-magazine-delta-battlemap-realistic.png` |

---

<div style="page-break-before: always;"></div>

## Room 1 — Le Paludi Access Shaft

![[wiki/assets/sessions/session-05/maps/session-05-room-01-le-paludi-access-shaft-battlemap-realistic.png|Room 1 battlemap — Le Paludi Access Shaft with iron ladder, wet limestone, standing water, and 5-foot tactical grid.]]

**Dimensions:** 15 × 20 ft lower service landing beneath a 5 × 5 ft shaft. Hatch at street level, ladder descends 15 ft. Exit to Room 2 through a low south arch.

> [!read-aloud]
> The ladder is iron, bolted into limestone, and each rung is slick — not just with moisture. Something iridescent catches the light where hands have gripped the metal, a faint chemical film that is not rust. Fifteen feet down, your boots find standing water and a maintenance landing wider than the hatch above. The air changes at the bottom: brine and old stone, yes, but threaded through with something sweetly acrid, like fruit left to ferment in mineral water. A low arch leads south. Scrape marks run along the stone at knee height, recent enough that the dust has not settled back into them.

**Features:**

- **Iron ladder**: Corroded rungs. (DC 10 Athletics to descend quietly. Failure: metallic clang audible in Room 2.)
- **Lower landing**: Slick limestone around a shallow drain. (One creature can take half cover behind the raised hatch curb or stacked maintenance stones.)
- **Scrape marks**: Knee-height gouges in the limestone. Equipment was carried down this shaft recently — barrels, timber. (DC 12 Investigation: the marks are consistent with barrel staves dragged against the wall.)
- **Maintenance hatch**: Can be wedged open or sealed. If sealed behind the party, no one follows — but no one leaves this way either.

> [!dm]
> Orientation room. Let the party absorb the sensory shift from festival streets to underground. The scrape marks are the first physical evidence that something heavy has been moved through here recently.

---

## Room 2 — Y-Junction

![[wiki/assets/sessions/session-05/maps/session-05-room-02-y-junction-battlemap-realistic.png|Room 2 battlemap — Y-Junction with three exits, standing water, collapsed masonry, trail marks, and 5-foot tactical grid.]]

**Dimensions:** Roughly 35 × 30 ft irregular collector junction. Ceiling 6 ft. Three exits: north to Room 1, east/right branch to Room 3, southwest/left branch to Room 4. Sunken middle sump, raised edges, standing water throughout.

> [!read-aloud]
> The landing opens into a junction where three collector lines meet around a sunken sump. Water gathers in the middle, dark and still, with an oily film that catches lamplight in iridescent streaks. The chemical smell from the shaft is stronger here — thicker, wetter, clinging to the back of the throat. To the right, the tunnel narrows into shadow, while to the left the silt is churned with prints and drag marks. Low on the left wall: three cuts in the limestone, small, clean, deliberate.

**Features:**

- **Sunken sump**: 15-ft-wide pool, 2 ft deep at the centre; ankle-deep water elsewhere. Difficult terrain for creatures without swim speed. (2 Crocodiles submerged here — optional encounter, see below.)
- **Silt disturbance**: Left branch has heavier foot traffic. (DC 10 Survival: multiple individuals, multiple passes, within the last 48 hours. DC 15 Nature: the prints aren't human — the weight sits too far forward and the toes splay wide.)
- **Trail markers**: Three cuts in the limestone, knee-height, left wall. Plus a separate set — older, deeper — pointing down the right branch toward the Mercatura. (Jean-Claude identifies automatically: the three cuts are green/blue-caste directional markers. The older set uses red-caste priority notation — a different authority level, pointing a different direction. **Three Clue #3.**)
- **Collapsed masonry**: Right wall and sump edge. (Half cover for two creatures; climbing over costs 5 ft extra movement.)

> [!dm]
> Hub room. The trail markers are the earliest clue to the primary site — but only Jean-Claude can read them. If Jean-Claude is not present or does not examine them, this clue is invisible.

> [!mechanic]
> **Optional Encounter — Canal Crocodiles.** 2 Crocodiles (CR 1/2 each). AC 12, HP 19. Bite: +4 to hit, 1d10+2 piercing, target grappled (escape DC 12). Stealth +2 (advantage submerged). Attack on vibration, not sight. One lunges from the left branch, the second from the flooded drain on the right — flanking the point person across the sump. A grappled creature in the sump must also beat DC 10 Athletics to climb onto the raised lip. Flee if both bloodied. Do not pursue past the junction. **Difficulty: Easy (300 adj. XP).**

---

## Room 3 — Bridge Connector

![[wiki/assets/sessions/session-05/maps/session-05-room-03-bridge-connector-battlemap-realistic.png|Room 3 battlemap — Bridge Connector with low ceiling, narrowed chokepoint, far hatch, side passage, and 5-foot tactical grid.]]

**Dimensions:** 70 × 20 ft connector, narrowing to a 5-ft-wide low crawl for 20 ft near the middle. Ceiling drops from 6 ft to 4 ft after 35 ft. Far hatch at the Bridge end. Barred side culvert to T1.

> [!read-aloud]
> The ceiling drops in steps, each arch lower than the last. The chemical smell concentrates as the stone closes in — your face is closer to the waterline here, closer to whatever is coating the walls at knee height. The passage widens into maintenance pockets, then pinches to a crawl where old stone has settled. Silt crunches underfoot. Ahead, a pale square of light marks the far hatch, and a barred culvert breathes cold air from the Bridge side.

**Features:**

- **Low ceiling**: 4 ft after the first 35 ft. Medium creatures move at half speed (crouching). Disadvantage on melee attacks with two-handed or heavy weapons. Small creatures move normally.
- **Silt floor**: Loose stone and packed silt. (DC 12 Acrobatics to move at full speed while crouched. Failure: stumble, noise audible in Rooms 2 and 7.)
- **Far hatch**: Bridge district access. Silt disturbed on both sides — used from below. (Opens into a Bridge district maintenance alcove, street level.)
- **Narrow passage**: 5-ft-wide chokepoint at the midpoint (20-ft stretch). Forced single-file for the tightest section.
- **Barred side culvert**: Leads toward T1, the Bridge district magazine. (The bars are loose enough for Small creatures; Medium creatures need DC 13 Athletics or thieves' tools to bend or remove them.)

> [!dm]
> Transition room and potential chase encounter. The tight quarters punish the party's mobility advantages (no flight, no leaping, cramped melee). If the fleeing handler is here, the chase rewards speed and reach over raw damage.

> [!mechanic]
> **Optional Encounter — The Late Handler.** 1 [[grung-elite-warrior|Grung Elite Warrior]] (CR 2 — stat block on the page), a blue-caste handler finishing a late route check. She moves toward the far hatch at full speed. Attacks only if blocked or grappled. Does not speak. If Jean-Claude addresses her in Grung, she stops for one beat — recalibrating — then continues. **If she escapes:** all sentry teams go to heightened alert (no more hide-and-report; active defense at all secondary sites). **Morale:** escape only. Surrenders below half HP if escape is impossible. Gives nothing except "the schedule moved." **Difficulty: Easy (200 adj. XP).**

---

<div style="page-break-before: always;"></div>

## Room 4 — Magazine Alpha (Le Paludi Yards)

![[wiki/assets/sessions/session-05/maps/session-05-room-04-magazine-alpha-battlemap-realistic.png|Room 4 battlemap — Magazine Alpha with stacked blackpowder barrels, timber wedges, drainage pipe, cover, and 5-foot tactical grid.]]

**Dimensions:** 35 × 25 ft side magazine with a raised dry ledge and a flooded drain trench. Ceiling 6 ft. Exits: back to Room 2, drainage overflow pipe to Room 6.

> [!read-aloud]
> The tunnel opens into a side magazine cut around an old drain trench. The air changes — dry, chemical, sharp enough to taste at the back of the throat. The rope lashing the barrels glistens with something that is not water: an iridescent residue, deliberately applied, that makes the hands want to pull away before the mind catches up. Against the far ledge: six barrels are stacked two high and three across, wedged tight with fresh-cut timber. The pale wood is unstained. The barrels are sealed with tar.

**Features:**

- **Blackpowder barrels (×6)**: Tar-sealed, timber-wedged at a structural weak point in the ceiling. (DC 10 Investigation: blackpowder. DC 18 on a critical: positioned where the sewer ceiling is thinnest — someone chose this spot because the surface above carries foot traffic. Fire or thunder damage within 10 ft: **4d6 fire, 20-ft radius, DC 14 DEX half. Ceiling collapse: 2d6 bludgeoning, buried, DC 14 STR to free.**)
- **Raised magazine ledge**: Dry stone lip 2 ft above the trench. (Half cover from the trench; climbing up costs 5 ft extra movement.)
- **Timber wedges**: Hold the barrel stack in place. (Removing: 1 minute careful work, or DC 12 Sleight of Hand as an action. Barrels roll free — magazine neutralized, but the noise alerts sentries in adjacent rooms.)
- **Drainage overflow pipe**: 4-ft-diameter pipe in the floor, leads to Room 6. (Medium creatures must crawl: half speed, prone, disadvantage on attacks. Small creatures walk normally. Jean-Claude: climb speed applies, no penalty.)
- *Grung Poison Vials (×2)*: On the handler's belt. (25 gp each. Can coat a weapon: next hit deals +2d4 poison damage, one use.)

> [!dm]
> First magazine encounter. Teaches the party how the sentry teams work and what the blackpowder means. The overflow pipe to Room 6 rewards exploration — it bypasses the main corridors entirely.

> [!mechanic]
> **Sentry Team.** 2 [[grung-npc|Grung]] + 1 [[grung-elite-warrior|Grung Elite Warrior]]. **Difficulty: Hard (1100 adj. XP).**
>
> - **Green Grung** (CR 1/4) — full stat block: [[grung-npc|Grung]].
> - **Elite Handler** (CR 2) — Mesmerizing Chirr (stun) is the ability to watch; full stat block: [[grung-elite-warrior|Grung Elite Warrior]].
> - **Orders:** hide, let intruders pass, report after. Break cover only if the party touches barrels.
> - **On discovery:** handler signals laborers through drainage pipe, then covers retreat from three-quarters cover.
> - **Morale:** green-caste flee if handler dies; handler breaks at half HP. Killing all three silently prevents a report.
> - **Poison craft:** Barrel lashings are pre-coated with concentrated skin secretions (DC 12 CON on bare-skin contact or poisoned 10 min; gloves negate). The Elite Handler carries a sealed glass vial of torpor extract — if cornered with no escape, she cracks it: 5-ft cloud, DC 12 CON or speed halved for 1 minute as limbs go heavy and sluggish. Retreating greens smear secretions on any surface they pass.

---

## Room 5 — Magazine Beta (Working Yards)

![[wiki/assets/sessions/session-05/maps/session-05-room-05-magazine-beta-battlemap-realistic.png|Room 5 battlemap — Magazine Beta with unfinished scaffolding, loose barrels, mortared breach, tools, and 5-foot tactical grid.]]

**Dimensions:** 40 × 30 ft working bay with a shallow flooded corner and half-built scaffold. Ceiling 6 ft. Exit: mortared breach to Room 6.

> [!read-aloud]
> This chamber mirrors the last only in purpose, and the chemical bite in the air is worse — concentrated, with nowhere to vent. Scaffolding climbs one wall, half-built, with one support beam braced against the ceiling and another leaning unsecured. The standing water in the flooded corner carries an oily sheen, pooled runoff from the workers with nowhere to drain. Barrels sit on the stones and in the water, not yet stacked. A hand drill and coils of rope lie beside a wooden bowl of cold rice. The rope is slick with the same iridescent residue as the magazine next door.

**Features:**

- **Incomplete scaffolding**: One support beam is unsecured. (DC 12 Athletics as an action: collapse the scaffolding, dumping barrels into the flooded corner. Powder soaks — magazine neutralized without detonation risk. The collapse is loud — audible in Rooms 6 and adjacent corridors.)
- **Blackpowder barrels (×6)**: Same as Room 4, but on the floor, not stacked. Same detonation risk if fire/thunder applied.
- **Builder's notation**: Scratched into the unsecured beam in Grung shorthand. Reads: "anchor south of M — tie to main." (DC 15 Investigation to notice. DC 12 Intelligence to parse "M" as a Mercatura reference. Jean-Claude reads the Grung shorthand automatically — "anchor to the primary, south of the Mercatura collector." **Three Clue #1.**)
- *Builder's tools*: Chisels, rope, hand drill. (5 gp total. Usable as improvised weapons or for disarming other magazines faster — grants advantage on the DC 12 Sleight of Hand check to remove wedges.)
- *Grung Poison Vials (×2)*: On the handler's belt. (25 gp each. Can coat a weapon: next hit deals +2d4 poison damage, one use.)
- **Loose plank bridge**: Crosses the flooded corner beside the scaffold. (DC 10 Acrobatics to cross while moving faster than half speed; failure drops the creature prone in ankle-deep water.)

> [!dm]
> Investigation room. The incomplete scaffolding is the easiest magazine to neutralize — water-soak the powder instead of risking detonation. The builder's notation is the first clue pointing toward the primary site. The sentry team here is distracted (one laborer building, handler split between tasks) — party gains advantage on initial Stealth checks.

> [!mechanic]
> **Bazzoth's Bench.** [[bazzoth-the-steeped|Bazzoth, the Steeped]] (CR 6) has claimed Beta as his working magazine — the flooded corner is his mixing station, the incomplete scaffolding his excuse to stay hands-on. He fights alongside 2 [[grung-npc|Grung]] laborers (one actively building, one watching); handler's attention is split. **Party gains advantage on Stealth checks to approach.** Same poison craft as Room 4 (coated surfaces, torpor extract, retreating secretion smear) plus Bazzoth's own Sump-Reek Bomb and Clinging Ichor. **Escalated — roughly 4,800 adj. XP (Bazzoth 2300 + 2×Grung 50, ×2 for 3 monsters), well past Hard.** Verify against the party's current HP/resources before running; the Stealth advantage and his single-target Shed the Years concentration are the intended outs.

---

<div style="page-break-before: always;"></div>

## Room 6 — Handler Relay

![[wiki/assets/sessions/session-05/maps/session-05-room-06-handler-relay-battlemap-realistic.png|Room 6 battlemap — Handler Relay with dry alcove, desk, route papers, stacked barrels, hidden passage, and 5-foot tactical grid.]]

**Dimensions:** 30 × 25 ft dry relay alcove raised above the service corridor. Ceiling 6 ft. Exits: overflow pipe to Room 4, mortared breach to Room 5, service corridor to Room 7, hidden passage to Room 8.

> [!read-aloud]
> The passage rises onto dry, swept stone — the first clean air since the shaft, though even here a faint chemical sweetness lingers in the lamplight. An oil lamp burns low on a plank desk balanced across two barrels, with more barrels stacked into a wall behind it. Waxed papers are pinned to the limestone: routes, numbers, tide markings in a hand too small for human fingers. A small blue-skinned figure sits with her back to the entrance, cross-referencing one chart against another, and has not heard the party yet.

**Features:**

- **Ruma Delacroix**: Blue-caste handler, quartermaster for the secondary magazine network. If she ever fights, use [[grung-elite-warrior|Grung Elite Warrior]] stats. Carries a hand crossbow (shortbow stats) and a signal whistle. (If she blows the whistle: all sentry teams go to active defense — no more hide-and-report. Reaching for the whistle costs her action. If the party acts before she whistles, she can be talked to.)
- **Waxed route map**: Pinned to the wall. Shows 5 positions, not 4. Four marked with green-caste notation. The fifth marked with a red-caste authority symbol — a different command level. (**Three Clue #2.** DC 12 Investigation to examine the map. The fifth position is not labelled with a location — only the authority marker. Ruma refers to it as "the circle site" but does not know where it is.)
- **Raised dry floor**: 1 ft above the adjacent wet service corridor. (Counts as normal terrain; the corridor lip provides half cover to prone creatures.)
- *Globe of Invulnerability Scroll (×1)*: In a waxed tube under the desk. (Single-use. 6th-level abjuration. Requires DC 16 Arcana check to use — the caster's level is below the spell's level. Creates a 10-ft-radius barrier that blocks spells of 5th level or lower. Thematic: raid equipment intended to shield extraction teams from their own detonation blast.)
- *Grung Poison Vials (×2)*: On Ruma's belt. (25 gp each.)
- **Stacked empty barrels**: Along the south wall. (Three-quarters cover. Behind them: false wall leading to Room 8. DC 16 Investigation to find by search. Ruma does not know this passage exists — it was built by Solange's team.)
- *Handler's purse*: 15 gp mixed Calven and Tessarine coin. Tide charts. A personal tally of secondary site powder weights.

> [!dm]
> Ruma is the intelligence pivot: route map, Globe scroll, hidden passage, and network check-in clock. Make the room feel safe, then put the check-in clock on the table. Resolve spoof/alert before any long rest.

> [!mechanic]
> **Ruma Delacroix — Social Encounter.** Ruma values survival over operational security.
>
> - **Surrenders:** disarmed and outnumbered.
> - **Triggers:** naming [[felix-aho|Felix Aho]]; Jean-Claude speaking Grung in handler-register.
> - **Knows:** four secondary sites/status, accelerated timeline, fifth red-caste site, sentry composition, egress vents, poison protocols (which surfaces are coated, how torpor extract works, what the weapon venom does).
> - **Doesn't know:** usable primary route, circle purpose, [[solange-barret|Solange]]'s identity, [[simone-tabarnack|Simone]]'s identity.
> - **Key use:** her map proves a fifth authority marker exists; Jean-Claude/trail-marker synthesis makes it navigable.

**Ruma check-in clock:**

| Time | If not spoofed | If spoofed |
|---|---|---|
| T+0 | Ruma captured/killed/delayed; clock starts | Jean-Claude/Ruma sends routine status |
| T+1h | Pipe-click inquiry from another handler | No change |
| T+2h | Handler network marks Room 6 missing; primary garrison goes active defense | No change |
| T+3h | Remaining secondary teams begin evacuating nonessential labourers | No change |
| T+8h | Party finishes rest; no patrol enters Room 6, but no surprise in Room 8 unless hidden passage is used | Party finishes rest; hidden passage grants surprise as written |

**Spoofing the check-in:** DC 13 Deception, Intimidation, or Performance using handler-register Grung; Jean-Claude speaking Grung has advantage. Captured Ruma can do it if promised believable protection.

> [!dm]
> **Session 06: this clock is moot.** Ruma is a party ally and answers every check-in herself — no detection clock, no spoof roll, no patrol. The table above is retained for a run where she is *not* turned; in Session 06, skip it. (See [[session-06-run-guide|Session 06 Run Guide § Scene 2]].)

### Long Rest — Room 6

The party has likely fought two Hard encounters back-to-back (Rooms 4 and 5), plus whatever fired in Rooms 2 and 3. By the time they reach Room 6 and neutralize Ruma, expect depleted slots, inspiration, and HP. Room 6 is dry stone, swept clean, defensible from two chokepoints, and silent.

> [!dm]
> Make the rest feel obvious, safe, and smart: dry stone, oil-lamp warmth, quiet, two chokepoints, Ruma's desk as barricade. If the party hesitates, have a Warren runner report the flagged secondary sites are handled. Quote: "Nona says rest; she says you'll need it."

**Heroes' Feast expiration:**

- Feast was eaten the previous evening at [[nona-black-jaw|Nona]]'s safe house; the 24-hour duration expires during this 8-hour rest.
- Do not mention it, hint at it, or volunteer the math.
- If asked when they ate, answer honestly; the realization lands when Foul Miasma deals poison damage.

> [!mechanic]
> **Watchful Long Rest (8 Hours).** The party can maintain watch rotations. Resolve Ruma's check-in before the rest; the room remains physically safe either way.
>
> **First watch:** Distant grinding from deeper in the collector system — stone settling, water shifting in the channels. The festival is muffled through stone overhead. Nothing approaches. A Warren runner's voice echoes faintly through a maintenance pipe — [[nona-black-jaw|Nona]] confirming that Warren fighters are handling the secondary sites the party marked. The party has permission to focus forward.
>
> **Second watch:** If the check-in was not spoofed, pipe-clicks travel through the stone — a handler code no one in the room answers. If spoofed, a canal crocodile investigates the drainage pipe, sniffs, and withdraws.
>
> **Third watch:** Silence. Complete silence. The standing water in the adjacent tunnels stops flowing for several minutes. Then it resumes — a tidal shift somewhere in the system, nothing more. The air is still. The oil lamp burns steady.
>
> **On waking:** The party is rested. Full HP, full spell slots, full inspiration. Describe them feeling sharp, focused, ready. The air from the deeper tunnels carries something faint — mineral, organic, not quite identifiable. The trail markers converge ahead. The primary site is waiting.

---

## Room 7 — Main Collector

![[wiki/assets/sessions/session-05/maps/session-05-room-07-main-collector-battlemap-realistic.png|Room 7 battlemap — Main Collector with central water channel, raised walkways, service exits, overflow vent, and 5-foot tactical grid.]]

**Dimensions:** 90 × 25 ft vaulted tunnel. Ceiling 8 ft. Central water channel (10 ft wide, 2 ft deep). Raised stone walkways and service shelves on either side. Exits: archway to Room 3, service corridor to Room 6, descending passage to Room 8, overflow vent to T2.

> [!read-aloud]
> The ceiling rises and the tunnel widens around a central channel — eight feet overhead, room to breathe for the first time in hours. Running water splits the collector down the centre, fast enough to carry the chemical film in long iridescent streaks toward a grate you can hear but not see. The air is worse here, not better: organic, mineral, thick enough to taste at the back of the throat. Every trail marker you've followed converges on the south wall, and above them, faded commission letters: MERCATURA NEXUS 200 PAS.

**Features:**

- **Central water channel**: 10 ft wide, 2 ft deep, flowing. Difficult terrain. Swim DC 10 to cross without being pushed 5 ft downstream. (Small creatures are fully submerged if they enter — swim or drown.)
- **Stone pier supports**: Every 20 ft along the walkways and channel edge. (Half cover.)
- **Trail markers**: Knee-height on the right walkway wall. Green and blue directional marks point back toward the secondary sites. One set of red-caste priority marks points forward — toward the Mercatura. (Jean-Claude reads automatically: the red marks are command-level, same notation as the Y-junction set. They converge here, pointing deeper. This is the third confirmation of the primary site's direction.)
- **Canal commission sign**: Faded chalk on the wall. "MERCATURA NEXUS 200 PAS." in old Calven script. (DC 10 History or Intelligence: "200 paces to the Mercatura collector nexus." Confirms direction for non-Grung-readers.)

> [!dm]
> Decompression and escalation. The ceiling lifts but the air worsens — this is the toxic peak before the climax. The vaulted space lets the party stand upright and plan, but the chemical saturation communicates that they are deeper in the Grung's territory than ever. Trail markers and commission sign both point forward. After this room, the party is committed to the primary chamber approach.

---

<div style="page-break-before: always;"></div>

## Room 8 — Primary Detonation Chamber (Mercatura)

![[wiki/assets/sessions/session-05/maps/session-05-room-08-primary-detonation-chamber-battlemap-realistic.png|Room 8 battlemap — Primary Detonation Chamber with converging drainage channels, central summoning circle, scaffolding, powder storage, and 5-foot tactical grid.]]

**Dimensions:** Roughly 60 × 50 ft irregular vaulted collector nexus. Ceiling 15 ft. Four drainage channels (3 ft deep, 5 ft wide) converge from cardinal directions. Central dry stone platform (15 ft diameter) with summoning circle. Scaffolding along all walls to 10 ft height, with powder packed into the ceiling joints. Exits: ascending passage to Room 7 (north), hidden passage to Room 6 (south, behind scaffolding).

> [!read-aloud]
> The passage opens into a vaulted collector nexus broad enough to swallow footsteps. The chemical saturation peaks here — the air is thick, acrid, layered: blackpowder above, Grung secretion on every surface, and beneath both a sharp, electric ozone bite that pricks the throat and lifts the hair on your arms, rising off the stone floor. Fifteen feet overhead, pale stone and old masonry hold up the Mercatura, every crack packed with dark powder and crude timber scaffolding. In the centre, four drainage channels part around a bone-white circle cut deep into dry stone. The circle hums at the edge of hearing while a red-skinned Grung kneels beside it and four purple warriors hold the channels.

**Features:**

- **Blackpowder-packed ceiling**: Every crack, join, and crevice. Catastrophic scale. (Fire or thunder damage anywhere in the chamber: **8d6 fire across the chamber and 10 ft into each exit, DC 16 DEX half. Total ceiling collapse: 4d6 bludgeoning, buried, DC 16 STR to free.** This collapses the Mercatura plaza above. Using fire in this room is a last resort.)
- **Summoning circle**: 15-ft diameter, cut into stone, kept dry by water-routing trenches. Sheds bright light in a 10-ft radius and dim light for 10 ft beyond that. Jean-Claude's Umbral Sight does not function in the bright zone. (DC 14 Arcana: summoning circle for an extraplanar entity, not fiend or celestial, outer planes. DC 20 Arcana or critical: configured for a **Slaad**, unbound, uncontrolled. Keyed to activate on detonation — the explosion and the summoning are one event. **Disruption:** 1 minute of careful work, or DC 18 Arcana as an action to sever a key resonance line. Prevents summoning even if detonation fires.)
- **Scaffolding**: Timber frames along all walls, rising to 10 ft. (Elevated positions: +2 AC vs. melee from below, no cover vs. ranged. Two [[grung-elite-warrior|Elite Warriors]] fire from here. Climbing the scaffolding: DC 10 Athletics. Destroying a scaffold section: DC 12 Athletics or 10 HP damage — collapses that section, dealing 1d6 bludgeoning to anyone on it and creating difficult terrain.)
- **Drainage channels (×4)**: 3 ft deep, 5 ft wide, flowing water. (Difficult terrain. Half cover for a prone creature inside a channel. Small creatures are chest-deep — move at half speed, disadvantage on melee attacks.)
- **[[solange-barret|Solange Barret]]**: Red-caste warlock, channeling the summoning ritual. Uses her action each turn to sustain it — cannot attack or cast offensive spells. Mirror Image active (3 duplicates). Within the circle she has advantage on concentration saves; her reaction is Counterspell OR Detonate, not both in the same round. The circle deflects the blast (everyone outside takes full detonation). She completes the ritual on her next turn unless it's disrupted — [[otar-the-foul|Otar]] manifests through her body, consuming her. Full stat block: [[solange-barret|Solange Barret]].
- **4 [[grung-elite-warrior|Grung Elite Warriors]]**: Purple-caste. Concealed at the four drainage channel entrances. (DC 16 Perception to detect before surprise round. Shortbow from concealment, then melee + Mesmerizing Chirr.)
- *Solange's ritual components*: Chalk, powdered limestone, an iridescent pigment that does not wash off. (50 gp to an arcane collector. Also: evidence of formal arcane training — the techniques in this circle are not Grung-developed. Connects to the open question of who designed it.)

> [!dm]
> Run Room 8 as three phases: garrison, detonation, manifestation. The hidden passage reverses surprise and may let a PC reach Solange before Phase 2. If the circle is disrupted before manifestation, no Otar; Solange detonates as cover and escapes by *Dimension Door* or a prepared route.

> [!mechanic]
> **Phase 1 — Primary Site Garrison.** 4 [[grung-elite-warrior|Grung Elite Warriors]] (CR 2 each) + [[solange-barret|Solange Barret]] (channeling, Mirror Image active) — stat blocks on their pages. Standing order: shoot on sight. One Elite Warrior per drainage channel entrance — 50-ft spread forces individual engagement.
>
> - **Hidden passage approach:** passive Perception 12 from the south scaffolding; surprise if no alert is active.
> - **Main approach:** DC 16 Perception to detect elites before they shoot from concealment.
> - **Terrain shift, round 3:** bright light expands to 20-ft radius; water channels rise to 4 ft deep.
> - **Poison discipline:** Scaffolding handholds are pre-coated (contact secretion, DC 12 CON). Each Elite carries one torpor extract vial — crack on death or when cornered (5-ft cloud, DC 12 CON, speed halved 1 min). The drainage channels carry concentrated secretion runoff; bare skin in the water triggers the environmental contact poison.

> [!mechanic]
> **Solange Timing.**
>
> - **Action:** sustain ritual each turn; she cannot attack or cast offensive spells while channeling.
> - **Concentration:** advantage inside Circle Ward. Damage calls for normal concentration DC: 10 or half damage, whichever is higher.
> - **Reaction:** Counterspell OR Detonate. Counterspell spends one of two Pact slots and prevents Detonate until her next turn unless fire/thunder ignites powder.
> - **Disrupt circle:** DC 18 Arcana as an action, or 1 minute careful work. No Otar if done before manifestation.
> - **Incapacitated:** channel breaks. **Grappled:** channel continues but she cannot reposition. **Silence:** blocks spoken Detonate while she remains inside it; fire/thunder still ignites powder.

> [!mechanic]
> **Phase 2 — Detonation.** Trigger: 2nd Elite Warrior drops; circle is disrupted; Solange starts her turn with no Elite within 10 ft of the circle; or fire/thunder damage happens anywhere in the chamber.
>
> - Solange uses her reaction to Detonate if available. If she already used Counterspell, detonation waits until her next turn unless fire/thunder ignited the powder.
> - Detonate is a command word keyed to alchemical fuses; it is not a spell and cannot be counterspelled.
> - Damage: 8d6 fire across chamber and 10 ft into exits, DC 16 DEX half.
> - Collapse: 4d6 bludgeoning, DC 16 STR or buried/restrained; DC 16 STR to escape as an action.
> - Solange takes no damage inside the circle ward; the plaza above collapses into the chamber.

**After Detonation Battlefield:**

| Element | State |
|---|---|
| Room | Entire chamber becomes rubble; difficult terrain throughout |
| Exits | Room 7 remains passable but choked; hidden passage requires DC 14 Athletics to clear for Medium creatures |
| Buried PCs | Restrained; DC 16 STR action to escape, or adjacent ally DC 14 Athletics to clear |
| Surface breach | 30-ft Mercatura crater open to sky; civilians gather at edge until Otar attacks |
| Light/vision | Daylight from crater; dust lightly obscures chamber until initiative count 20 next round |
| Fire sources | Torch racks DC 12 Investigation; lamp oil DC 14; alchemist cart debris DC 14 for 2 alchemist's fire |
| Clock | Otar manifests on Solange's next turn unless circle was disrupted |

> [!mechanic]
> **Phase 3 — Otar manifests.** Run him straight from his stat block: **[[otar-the-foul|Otar the Foul]]** (CR 12, recalibrated for the five-PC Session-06 party). The page carries AC/HP, Foul Miasma, Entropic Regeneration, Chaos Pulse, Unstable Form, legendary and lair actions, plus the Catarina staggered-entry adaptation. Suppressing Entropic Regeneration with fire or acid is the tactical key.
>
> **Difficulty: Extremely Deadly.** Rewards stealth, planning, and environmental creativity over direct assault.

---

<div style="page-break-before: always;"></div>

## Room T1 — Magazine Gamma (Bridge District)

![[wiki/assets/sessions/session-05/maps/session-05-room-t1-magazine-gamma-battlemap-realistic.png|Room T1 battlemap — Magazine Gamma: low old-brick magazine with four blackpowder barrels under a fresh timber-braced seam, barred culvert to Room 3, rusted street drain, and 5-foot tactical grid.]]

**Dimensions:** 30 × 20 ft low service magazine. Ceiling 5 ft. Exits: barred culvert to Room 3, rusted street drain toward the Bridge district.

> [!read-aloud]
> The culvert opens into older brickwork, lower and tighter than the Le Paludi lines. Four barrels sit under a stone seam braced with fresh timber. The air tastes of powder, rust, and the same chemical sweetness as the main tunnels — concentrated in the tight space until breathing feels deliberate. Above, festival feet drum faintly through the Bridge stones.

**Features:**

- **Blackpowder barrels (×4)**: Smaller charge, enough to buckle ground rather than open a full breach. (Same neutralization and detonation rules as Room 4.)
- **Low ceiling**: 5 ft. (No jumping; Medium creatures cannot use reach over allies cleanly.)
- **Rusted street drain**: Leads to a Bridge district maintenance alcove. (Small creatures pass freely; Medium creatures need DC 13 Athletics or thieves' tools to force the grate.)
- **Guardian**: [[vashu-the-weeping-veil|Vashu, the Weeping Veil]] (CR 5) plus 1 [[purple-caste-enforcer|Purple-Caste Enforcer]]. Vashu's blindsight ignores the low light and cramped sightlines entirely — she does not need to see in a 5-ft-ceiling room. The enforcer's Binding Tongue sets up a grapple; Vashu's Pressure Point finishes it. **~2,850 adj. XP (Vashu 1800 + Enforcer 100, ×1.5 for 2 monsters).**

> [!dm]
> Gamma is the low-ceiling variant. Use it to punish flight/leaping without adding new rules. If neutralized, Bridge captives drop by one lane. Vashu's Weeping Veil (blinding/poisoning mist) is brutal in this footprint — telegraph it before she pops it if the party has no way to disengage.

---

## Room T2 — Magazine Delta (Harbour Approach)

![[wiki/assets/sessions/session-05/maps/session-05-room-t2-magazine-delta-battlemap-realistic.png|Room T2 battlemap — Magazine Delta: tidal harbour-approach magazine with six barrels at the wet seam, flood overflow vent to Room 7, barred quay egress vent with daylight, and 5-foot tactical grid.]]

**Dimensions:** 35 × 25 ft tidal magazine beside a 3-ft egress vent. Ceiling 6 ft. Exits: flood overflow vent to Room 7, outer-quay vent above the waterline.

> [!read-aloud]
> Salt air cuts through the chemical film here — the first breath that doesn't taste of Grung. Six barrels are wedged against a wet seam while black water slaps below an iron vent, the iridescent residue on the barrel lashings catching what light filters from outside. Beyond the bars, open air moves. Somewhere outside, rigging knocks against a mast.

**Features:**

- **Blackpowder barrels (×6)**: Full secondary charge. (Same neutralization and detonation rules as Room 4.)
- **Outer-quay egress vent**: 3 ft wide, above the waterline. (Sealing/blocking it disrupts harbour-side extraction even if detonation fires.)
- **Tidal slap**: Water rises 1 ft per hour near high tide. (After 2 hours, Stealth checks here have disadvantage from splashing unless creatures have swim speed.)
- **Guardian**: [[ozzeth-the-twiceborn|Ozzeth, the Twiceborn]] (CR 8) with a [[purple-caste-zealot|Purple-Caste Zealot]] escort. A 9th-level INT caster with swim 30 ft. — as comfortable in the tidal water as anyone here. His control magic (*dominate person*, *hypnotic pattern*, *hold person*) and mobility (*misty step*, *dimension door*, *greater invisibility*) make him a slippery backline threat; the Zealot is a walking powder-charge that closes to detonate. His casting has no verbal components, so *Silence* does nothing.

> [!dm]
> Delta is the extraction-lane room. The vent matters more than the barrels if the party is trying to reduce captives. Ozzeth won't die guarding barrels — he'll *dominate* whoever moves to disable the vent and turn them back on their own party, teleporting clear (*dimension door* to the outer-quay side) once the fight sours. Watch the Zealot near the barrel stack: a suicidal charge next to blackpowder is its own detonation risk. *(Session 06 roster: Ozzeth was promoted here from the former mobile reserve, which has been dropped — see [[session-06-run-guide|Session 06 Run Guide]].)*

---

<div style="page-break-before: always;"></div>

## Three Clue Audit

**Conclusion:** A 5th primary detonation site exists beneath the Mercatura. The summoning/Otar conclusion is confirmed in Room 8, not by the route clues alone.

| # | Clue | Room | Mechanic | Without combat? |
|---|---|---|---|---|
| 1 | Builder's notation on incomplete scaffolding: "anchor south of M — tie to main" | 5 (Magazine Beta) | DC 15 Investigation; DC 12 INT to parse | Yes (after disarming) |
| 2 | Waxed route map showing 5 positions — fifth marked with red-caste authority notation | 6 (Handler Relay) | DC 12 Investigation on map, or Ruma confirms the fifth marker | Yes (stealth or social) |
| 3 | Red-caste priority trail markers pointing toward the Mercatura, distinct from green/blue directional marks | 2 (Y-Junction) | Automatic for Jean-Claude; impossible without Grung expertise | Yes (entry room) |

---

## Clues & Threads

| Clue / Thread | Location | Connects To |
|---|---|---|
| Grung trail notation (caste-specific) | Rooms 2, 7 | [[grung-clans\|Grung caste hierarchy]]; Jean-Claude's expertise |
| Builder's notation referencing primary site | Room 5 | Primary chamber (Room 8) |
| Route map (5 positions) | Room 6 | Full operation scope; [[calveno-beffa-grung-raid\|raid plan]] |
| Summoning circle (Slaad) | Room 8 | [[otar-the-foul\|Otar the Foul]]; open question of who designed the circle |
| Solange's ritual components | Room 8 | Formal arcane training; Simone's network capabilities |
| Globe of Invulnerability scroll | Room 6 | Raid extraction mechanics; [[calveno-beffa-grung-raid\|detonation sequence]] |
| Accelerated timeline (from Ruma) | Room 6 | Party's intervention window is shorter than expected |
| Egress vent to outer quay | T2 | Extraction route; vethka positioning |

---

## Treasure Summary

| Item | Value | Location |
|---|---|---|
| *Grung Poison Vials* (×6) | 25 gp each (150 gp total) | Rooms 4, 5, 6 (2 per site on handler belts) |
| *Globe of Invulnerability Scroll* (×1) | Priceless (quest reward) | Room 6 (waxed tube under desk) |
| *Builder's tools* (chisels, drill, rope) | 5 gp | Room 5 |
| *Handler's purse* | 15 gp mixed coin | Room 6 |
| *Solange's ritual components* | 50 gp to arcane collector | Room 8 |
| Handler equipment (crossbows, bolts) | ~30 gp total | Rooms 4, 5, 6, 8 |
| Dravosi sewer maps + tide charts | Intel value | Room 6 |
| Blackpowder (salvageable if soaked) | 5 gp/barrel | Rooms 4, 5, 8, T1, T2 |
| **Total monetary** | **~250 gp** + scroll | |

---

<div style="page-break-before: always;"></div>

## Running This Dungeon

### Pacing

The dungeon has four natural acts:

1. **Discovery (Rooms 1–3):** The party enters the network and encounters the first signs of Grung presence. The toxic atmosphere begins as a hint — iridescent residue on ladder rungs, an oily film on the water, a chemical smell that shouldn't be here. Optional encounters (crocodiles, fleeing handler) set the tone. Stealth and investigation dominate.
2. **Disruption (Rooms 4–6):** The party finds and disarms secondary magazines. The Grung saturation becomes obvious: coated surfaces, chemical air sharp enough to taste, secretion residue on every rope and handle. Two Hard encounters (sentry teams) back-to-back drain resources. The handler relay is the intelligence pivot — what the party learns from Ruma (or the route map) determines whether they discover the primary site.
3. **The Rest (Room 6):** The party has burned spell slots, inspiration, and HP through Acts 1–2. Room 6 is dry, defensible, and quiet — a respite from the chemical oppression. See "Long Rest — Room 6" in the Room 6 key. The rest gives the party a full resource reset before the climax, but Heroes' Feast (consumed the previous evening) expires during the 8-hour rest. The party enters the primary chamber fresh but without poison immunity, Wisdom save advantage, or the max HP buffer.
4. **Confrontation (Rooms 7–8):** The toxic escalation peaks. Room 7's air burns. Room 8 layers blackpowder, Grung secretion, and summoning-circle ozone into air that stings the eyes and coats the throat. The hidden passage from Room 6 is the party's best tactical advantage.

### If Loud

The party fights through the sentry teams and makes noise. Each combat alert propagates:

- Room 2 combat alerts Rooms 3 and 4 (DC 14 Stealth to fight quietly)
- Room 4 combat alerts Room 6 (Ruma reaches for the whistle)
- Room 6 whistle alerts all secondary sites and the primary garrison

If the entire network is alerted, the primary chamber garrison has time to prepare: the Elite Warriors set ambush positions and the party loses any chance of surprise. Solange continues channeling regardless — the ritual does not accelerate, but the garrison is ready. The encounter in Room 8 becomes a fortified position rather than a working site caught mid-task.

**No mobile reserve (Session 06).** The lieutenant roster is now three placed guardians — [[bazzoth-the-steeped|Bazzoth]] (Beta), [[vashu-the-weeping-veil|Vashu]] (Gamma), [[ozzeth-the-twiceborn|Ozzeth]] + [[purple-caste-zealot|Purple-Caste Zealot]] (Delta) — with no roving response force. [[ozzeth-the-twiceborn|Ozzeth]], who used to hold that role, now guards Delta himself. If the network goes to full alert, the guardians brace in place and combat noise draws the nearest working crew (a green [[grung-npc|laborer]] or two); "who shows up next" is proximity, not a reserve boss. ([[ozvok-the-vermillion-distiller|Ozvok, the Vermillion Distiller]] is shelved for this run — his block is retained for future use.)

### If Stealthy

The party moves through the network without triggering alerts. Stealth DCs are listed per room. If no alert propagates, the sentry teams are in their default posture (hide-and-report at secondary sites, working at the primary). The party can:

- Bypass secondary sites entirely and go straight to Room 8
- Neutralize sites silently (kill sentries before they flee, soak powder without noise)
- Use Room 6's hidden passage to approach Room 8 from the unguarded direction
- Follow the iridescent secretion trails on walls and water to track Grung movement patterns without needing trail-marker literacy

Stealth through the entire network is possible but demanding — 4+ group Stealth checks at DC 12–16. Crissdalynn (no Stealth proficiency, metal weapons) is the weak link. Perrin's Minor Illusion can create distracting sounds to cover movement.

### If Negotiate

Ruma Delacroix (Room 6) is the negotiation path. She values her life over the operation. If the party captures her without raising an alarm, she gives them:

- Secondary site locations (confirms Felix's intel)
- The accelerated timeline
- Existence of "the circle site" (fifth position, red-caste authority)
- Sentry compositions and rotation times
- Egress vent locations
- Poison protocols: which surfaces are coated, how torpor extract works, what the weapon venom does, and how to handle coated surfaces safely (gloves or cloth wrapping)

She cannot give them the primary site's location (she does not know it). But the route map on her wall shows five positions, and the trail markers in the network converge. The party can navigate to Room 8 using the clues even without Ruma's cooperation.

<div style="page-break-before: always;"></div>

### The Primary Chamber — Tactical Options

The Room 8 encounter is Extremely Deadly by the numbers — and that is before Phase 2 detonates the ceiling and Phase 3 drops a Slaad ([[otar-the-foul|Otar]]) on a wounded party. The fight rewards preparation:

- **Hidden passage (Room 6 → 8):** Reverses surprise. The party enters behind the garrison — may let a PC reach Solange before elites react.
- **Circle disruption (DC 18 Arcana):** If the circle is disrupted before manifestation, Solange cannot complete the summoning. She detonates as cover and escapes by *Dimension Door* or a prepared route. No Otar — but [[simone-tabarnack|Simone]] learns about [[jean-claude-tabarnack|JC]].
- **Globe of Invulnerability scroll (Room 6):** DC 16 Arcana to activate before Phase 2. Shields a 10-ft radius from the detonation blast. The scroll was designed for this — reward the party for carrying it.
- **Environmental weapons:** Collapsing scaffolding (DC 12) drops sentries from elevated positions. Water channels provide half cover for prone characters.
- **Allies:** If the party briefed [[master-kyzil|Kyzil]] (CR 14 monk), he accelerates Phase 1 and survives Phase 2. If he reaches the circle, he tries to destroy it himself — likely preventing Otar while letting Solange escape and report JC. If [[nona-black-jaw|Nona]] knows, Warren runners can seal maintenance hatches behind the party.
- **Split approach:** Two PCs through the main passage (Room 7), two through the hidden passage. The garrison cannot watch both directions.

### If Solange Escapes

Solange escapes only if the circle is disrupted before manifestation. She detonates the ceiling as cover and escapes by *Dimension Door* or a prepared rubble route. She reports to [[simone-tabarnack|Simone]]: the primary is compromised, a Grung defector identified caste notation. **Simone now knows JC is alive and active.** If the ritual completes, Solange is consumed by the manifestation — she does not escape and Simone does not learn about JC from this source.

### Pressure Valve (Primary Chamber)

Targets party weaknesses — amplified by the expired Heroes' Feast:

- **Foul Miasma bites.** Without poison immunity, 1d6 poison per turn for standing near Otar. Elite Warrior poison arrows (2d4 + DC 12 poisoned condition) now connect. The torpor extract any surviving handler cracks adds speed-halved on top of the poisoned condition — a party member hit by both is poisoned, slowed, and taking passive poison damage every round. Melee range is genuinely costly.
- **No Wisdom advantage.** Mesmerizing Chirr (DC 12 WIS, stun) from 4 Elite Warriors threatens Perrin's concentration without the feast's save advantage. Stagger Chirr: first warrior fires round 1, hold the rest for rounds when Perrin is drumming.
- **No HP buffer.** The +2d10 max HP from the feast is gone. The party is at their natural HP pools against Phase 2's detonation (8d6 fire + 4d6 bludgeoning). Characters who took damage in Phase 1 may go down.
- **The dead-man switch.** The party's success at clearing the garrison can trigger the detonation. Dropping the 2nd Elite, leaving Solange unguarded, disrupting the circle, or using fire/thunder all collapse the ceiling. Winning Phase 1 too cleanly is the encounter's core tension.
- **Bright light zone.** The summoning circle's bright light (expanding at round 3) neutralizes Jean-Claude's Umbral Sight. He must choose: snipe from the dim edges or approach the circle where he's visible.
- **No fire or acid (Phase 3).** After the detonation, Otar's Entropic Regeneration demands fire or acid to suppress. Fire sources are in the rubble above (DC 12–14 Investigation), and Otar's uncontrolled Bile Spray can also suppress his regeneration.

**No-rest branch:** If the party skips the Room 6 long rest, Heroes' Feast remains active: poison immunity, frightened immunity, Wisdom-save advantage, and +2d10 max HP. They enter Room 8 depleted on HP, slots, inspiration, and focus. The fight becomes less poison-brutal but more resource-starved; fire the Rattle later unless two PCs drop.

### Secondary Extraction Clock

Use this during the Otar fight for any secondary site the party did not neutralize or seal.

| Otar round | Visible tick | Captive pressure |
|---|---|---|
| 1–2 | Crowd confusion; Beffa laughter becomes panic | Extraction teams breach lanes |
| 3 | DC 12 Perception hears screams from the Bridge | First captives pulled below |
| 5 | Smoke visible from Le Paludi | 10–20 captives per active lane |
| 7 | Harbour runners reach T2 egress if open | Loading begins toward waiting *vethka* |
| Fight ends | Count active lanes | Use Raid Scale in Session 05 run guide |

<div style="page-break-before: always;"></div>

### Safety Valve — The Rattle

The fight is brutal by design. If it tilts toward a TPK, the [[warren|Warren]] responds — represented as **lair and legendary actions the party temporarily gains**, mirroring Otar's own.

**Trigger:** Two PCs unconscious simultaneously, OR party aggregate HP drops below 25% of maximum, OR the DM reads the table and sees a TPK forming. Fires on initiative 20 the round after the threshold is met; lasts until Otar falls.

**The detonation collapsed the Mercatura plaza.** The sound carries into [[le-paludi|Le Paludi]]. The Warren feels the ground shake. Someone strikes a pan.

> [!mechanic]
> **Full mechanic:** the party's Rattle **lair action** (Human Chain / Fire Brigade / Din of Pans) and shared **3-legendary-action pool** (Colla's Toss / Shoulder In / Ruk Wades In) live on **[[otar-the-foul|Otar the Foul § The Rattle — The Warren Fights Beside You]]**. Net effect: healing, fire (regen suppression), and breathing room. It does not kill Otar; two quick taps end it when he falls.

### Advantage Window (Primary Chamber)

Rewards party strengths if they prepare. The party is rested (full HP, slots, inspiration) — their advantage is resource depth, not feast buffs:

- **Hidden passage (Room 6 → 8):** Reverses surprise — the party's strongest observed pattern pays off here.
- **Full resources.** The long rest means full spell slots, full Bardic Inspiration, full Ki/Focus. Perrin has every slot and every inspiration die. This is the tradeoff for losing the feast — they enter the fight at peak capacity.
- **Vertical terrain.** 15-ft ceilings and 10-ft scaffolding reward Crissdalynn's flight and Delmar's boots. A flier above scaffolding has advantage on melee vs. prone warriors and partial cover from ground-level ranged.
- **Bardic inspiration.** Perrin's d8 makes Mesmerizing Chirr saves manageable and turns near-misses into hits. Without the feast's Wisdom advantage, his inspiration is now the PRIMARY defense against Chirr stuns. Protecting him is the tactical key — Kyzil identified this.
- **Circle disruption.** If disrupted before Phase 2 triggers, the summoning fails. Solange detonates and escapes — no Otar, but Simone learns about JC.
- **Allies.** If the party briefed [[master-kyzil|Kyzil]] (CR 14), he can accompany or create a surface diversion. If he personally disrupts the circle, Otar is likely prevented but Solange escapes with proof JC is active. If [[nona-black-jaw|Nona]] knows, Warren runners can seal maintenance hatches behind the party.
- **The Rattle.** If the fight goes badly, the Warren responds. See "Safety Valve — The Rattle" above.

### Drama Suite (Primary Chamber)

| DC | Effect |
|---|---|
| 10 | Identify blackpowder, climb scaffolding, cross a drainage channel |
| 12 | Resist Mesmerizing Chirr (WIS), resist Poisonous Skin (CON) |
| 13 | Resist Solange's spell save (Counterspell check) |
| 15 | Detect Elite Warriors before surprise (Perception), identify circle as extraplanar (Arcana) |
| 16 | Detect hidden passage from Room 6 (Investigation), resist Tongue Lash grapple (STR, Otar) |
| 18 | Sever a circle resonance line (Arcana, action) |
| 20 | Identify circle as Slaad-configured (Arcana), identify ritual techniques as non-Grung-developed |

**Shenanigan offers:**

- Use the *Globe of Invulnerability* scroll (Room 6) before Phase 2 triggers. DC 16 Arcana. Shields a 10-ft radius from the detonation — the scroll was designed for this exact use.
- Incapacitate Solange before Phase 2 (break her concentration, grapple, Silence). Prevents both detonation and summoning. Extremely hard given Circle Ward and Mirror Image.
- Turn Otar's Bile Spray (acid) against his own regeneration — the uncontrolled splash can suppress his regen. Reward creative positioning.

**Box of Doom flags:**

- Slaad egg infection from Otar's bite (DC 15 CON — 3-month time bomb, curable by Lesser Restoration)
- The detonation itself — 8d6 fire + 4d6 bludgeoning is a potential PC death if they're already wounded from Phase 1
- Civilian deaths/captives at secondary sites — use the Secondary Extraction Clock above

---

## If Ignored

The detonation fires on the shortened timeline (~1.5 days from current state). The Mercatura plaza collapses. [[otar-the-foul|Otar the Foul]] erupts through the rubble into festival crowds. Four secondary breaches open simultaneously across Le Paludi, the Bridge, and the harbour approach. Grung extraction teams seize 200–300 captives if the raid is intact. The party's intel gap means the primary site hits unopposed.

See [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] for full consequences. See [[otar-the-foul|Otar the Foul]] for the city-level encounter.

---

## Connections

- [[calveno-beffa-grung-raid|Calveno — Beffa Grung Raid]] — the operation this dungeon serves
- [[warren-grung-sewers|Warren — Grung in the Sewers]] — the investigation that led the party here
- [[otar-the-foul|Otar the Foul]] — what the summoning circle calls if not disrupted
- [[solange-barret|Solange Barret]] — red-caste warlock operating the circle
- [[simone-tabarnack|Simone Tabarnack]] — operation commander
- [[felix-aho|Felix Aho]] — captured green laborer whose intel points to the secondary sites
- [[nona-black-jaw|Nona Black-Jaw]] — assigned the original sewer investigation
- [[jean-claude-tabarnack|Jean-Claude Tabarnack]] — the party's Grung expertise; Simone's brother
- [[perrin-black-jaw|Perrin Black-Jaw]] — Warren native; the conduit to Nona
- [[calveno|Calveno]] — the city above
- [[warren|The Warren]] — the Rattkin settlement sharing this tunnel system
- [[master-kyzil|Master Kyzil]] — potential CR 14 ally if briefed
- [[grung-npc|Grung (Green-Caste NPC)]], [[grung-elite-warrior|Grung Elite Warrior]], [[grung-wildling|Grung Wildling]] — creature stat blocks
- [[bazzoth-the-steeped|Bazzoth, the Steeped]] (Room 5/Beta), [[vashu-the-weeping-veil|Vashu, the Weeping Veil]] + [[purple-caste-enforcer|Purple-Caste Enforcer]] (Room T1/Gamma), [[ozzeth-the-twiceborn|Ozzeth, the Twiceborn]] + [[purple-caste-zealot|Purple-Caste Zealot]] (Room T2/Delta) — the three magazine lieutenants. [[ozvok-the-vermillion-distiller|Ozvok, the Vermillion Distiller]] — shelved for this run

---
type: rules
subtype: rule
campaign: shattered-sea
status: active
audience: players
publish: true
summary: "Play-table cheat sheet for ship tiers, crew roles, operations, bastion, and guns — consolidated quick reference."
created: 2026-05-30
updated: 2026-05-31
tags: []
sources:
  - "Inbox/ships-cheat-sheet.md"
confidence_level: medium
---

# Ships & Bastion — Quick Reference

Full rules: [[ship-mechanics|Ship Mechanics Hub]]

---

## Ship Tiers

| Tier | Examples | Cargo | Guns | Cost (used) | Min / Full Crew | Upkeep/wk |
|---|---|---|---|---|---|---|
| **1** | Sloop, cutter, lugger | 20 tons | 2–6 | 800–2,000 gp | 2–4 / 8–12 | 20–40 gp |
| **2** | Brigantine, schooner | 60 tons | 8–16 | 4,000–10,000 gp | 8–10 / 20–30 | 80–145 gp |
| **3** | Frigate, galleon | 150 tons | 20–40 | 15,000–35,000 gp | 20–25 / 55–80 | 270–430 gp |
| **4** | First-rate ship of the line | 100 tons | 80–112 | Crown property only | 55 / 280 | ~1,400 gp |

**Below minimum crew** — all ship checks at disadvantage; speed –20%.
**Upkeep** — due weekly whether sailing or docked. Missing it is handled narratively.
**Tier 4** — Crown property only. Not acquirable.

---

## Ship Stats

| Tier | Closest DMG Type | AC | Hull Points | Combat Speed |
|---|---|---|---|---|
| **1** | Keelboat | 15 | 100 | 10 ft. |
| **2** | Sailing Ship | 15 | 300 | 20 ft. |
| **3** | Warship / Galley | 15 | 500 | 25–40 ft. |
| **4** | Custom (first-rate) | 15 | 700 | 20 ft. |

All wooden vessels: **Damage Immunities** poison, psychic. **Condition Immunities** blinded, charmed, deafened, exhaustion, frightened, incapacitated, paralyzed, petrified, poisoned, prone, stunned, unconscious.

- **Condition** — Pristine / Worn / Damaged / Wrecked. Tracked narratively; mechanical penalties apply when relevant.
- **Repairs at sea** — Carpenter role required. Short rest: DC 15 Dexterity (Carpenter's Tools); success restores 2d8 + proficiency bonus HP. In port: 1 gp per HP, 1 workday per 25 HP.

---

## Crew Roles

| Role | Required When | Key Ability | Hireling/wk |
|---|---|---|---|
| **Captain** | Always | Charisma | — (PC or major NPC) |
| **Navigator** | Open-water voyages | Int (Navigator's Tools) | 10 gp |
| **Bosun** | Always | Str or Dex | 8 gp |
| **Gunner** | Guns in use | Dexterity | 8 gp |
| **Carpenter** | Repairs at sea | Int (Carpenter's Tools) | 6 gp |
| **Cook** | Voyages over 3 days | Wisdom | 4 gp |
| **Surgeon** | Surgeon's Berth facility | Wis (Medicine) | 8 gp |
| **Marine** | Boarding party actions | Str or Dex | 14 gp |
| **Ordinary Sailor** | Always (see tier minimums) | — | 2 gp |

**PC in role** — adds their modifier to relevant checks.
**Hireling in role** — baseline competence.
**Role unfilled** — function can't be performed, or rolls at disadvantage.

---

## At Sea

**Navigation checks** — roll when: reef channels, Maw approach, storm, unfamiliar waters. Navigator uses **Intelligence (Navigator's Tools)**.

| DC | Failure |
|---|---|
| 10 | Off course. +1 day. |
| 14 | Significantly off course. +2 days, minor complication. |
| 18 | Lost. +1d4 days, serious complication. |

- Tidewardens' charts: **advantage** in charted waters. Midchain charts: contradictory, no advantage.
- **Within 5 miles of the Maw:** compass and magical nav fail. Star navigation still works. Compass Rose solves this.

**Long rests** — standard 2024 rules. Cook role filled: +1d6 HP recovered. Storm during rest: DC 12 Con save or rest grants no benefits.

---

## Ship Upgrades

| Rarity | Access | Examples |
|---|---|---|
| Common | Port Tidefall | Weatherglass (200 gp), Signal Lantern pair (300 gp), Compass Rose (400 gp) |
| Uncommon | Faction contacts / specialists | Wind Caller's Boom (1,200 gp), Ghost-Keel Coating (900 gp), Fog Cannon (1,500 gp) |
| Rare | Catarina Da'Virelli or senior faction reward | Cartographer's Table (8,000 gp), Wardstone Figurehead (12,000 gp), Arcane Artillery (3,000 gp/mount) |
| Legendary | Late campaign only | The Drowned Keel (25,000 gp) |

Full details: [[ship-upgrades|Ship Upgrades]]

---

## Bastion

One shared bastion for the whole party. Slots pool across all PCs. Bastion Turns resolve weekly at sea or in port.

### Levels, Slots & Facility Gates

Both character level and ship tier must be met to install a facility.

| Character Level | Slots/PC | Party Pool (4 PCs) | Unlocks | Min Ship Tier |
|---|---|---|---|---|
| Any | — | — | Basic facilities | Any |
| 5 | 2 | 8 | Level 5 facilities | 1 |
| 9 | 3 | 12 | Level 9 facilities | 2 |
| 13 | 4 | 16 | Level 13 facilities | 3 |
| 17 | 5 | 20 | Level 17 facilities | 3 |

### Bastion Turn Orders

| Order | Effect |
|---|---|
| **Craft** | Produce items allowed by the facility. |
| **Empower** | Trigger the facility's power effect. |
| **Harvest** | Collect facility outputs. |
| **Maintain** | No order — roll a Bastion Event. |
| **Recruit** | Hire hirelings, defenders, or specialists. |
| **Research** | Gather intel or identify items. |
| **Trade** | Generate income via commerce. |

Absent PCs need *Sending* to issue orders. No order = Maintain. Neglect kicks in after consecutive missed turns equal to the PC's level.

---

## Facilities

### Level 5 — Tier 1+

| Facility | What it does |
|---|---|
| Navigator's Chart Room | *Identify* at low levels; Arcana item crafting at L9+ |
| Weapons Locker | Upgrades defender dice d6 → d8 |
| Crew Berths | Recruits and houses up to 12 Defenders |
| Provisions Store | Produces Basic Poison or Healing Potions each turn |
| Chart Archive | Research orders for navigation, history, factions |
| Waveservant Shrine | Counts as having paid the departure offering every voyage |
| Carpenter's Shop | Crafts mundane gear; Armaments magic items at L9+ |
| Expanded Cargo Hold | Trade income, scales with level |
| Rigger's Workshop | Implement magic items; Heroic Inspiration via Short Rest |
| Surgeon's Berth (HB) | Once/turn: stabilize all downed crew, or remove condition, or *Lesser Restoration*. Requires Surgeon role. |

### Level 9 — Tier 2+

| Facility | What it does |
|---|---|
| Officer's Mess | ~70 gp/week gambling income |
| Hydroponics Bay | Greater Healing Potions and stronger poisons |
| Tinker's Workshop | Any-rarity potion/poison crafting with Alchemist's Supplies |
| Reliquary Shrine | Relic magic items; spell slot refresh |
| Ship's Logbook Room | **Only facility that crafts spell scrolls.** Also produces false documents. |
| Sparring Deck | One week training → combat buffs for one week |
| Captain's Trophy Cabinet | 50% chance to research a Common magic item |

### Level 13 — Tier 3 only

| Facility | What it does |
|---|---|
| Captain's Archive | Legend Lore research without a spellcaster |
| Navigator's Sanctum | **Best defensive facility.** Reduces Attack chance from 1-in-20 to 1-in-400. |
| Beast Hold | House captured creatures CR 2 or lower for poison harvesting |
| Crow's Nest Observatory | Free level-5 spell effect (DC 15 Int save) |
| Ship's Galley | 24-hour buff drinks (Bigby's Burden, Sterner Stuff standouts) |
| Sacred Hold | *Greater Restoration* free (no diamond dust) |

### Level 17 — Tier 3 only

| Facility | What it does |
|---|---|
| Merchant Consortium | Six guild variants; Bakers'/Brewers' = 500 gp/week; Shipbuilders' = build a vessel in 40 days |
| Admiral's Sanctum | Free *Heal*, renewable THP, Sanctum Recall (instant party teleport to ship) |
| Command Deck | Up to 10 Lieutenants, each commanding 100 soldiers |

---

## Bastion Events at Sea

Triggered when any facility takes the Maintain order while underway.

| Event Type | Shipboard Version |
|---|---|
| Local threat/attack | Hostile vessel tracking or intercepting |
| Beneficial contact | Passing ship offers trade, intel, or opportunity |
| Structural damage | Storm/incident damages a facility |
| Windfall | Favorable current — voyage shortened 1d4 days |
| Hireling issue | Hireling problem requiring party response |

---

## Defense

**Attack event** — roll 6d6. Each 1 kills one Defender. No Defenders left: one Special Facility shuts down for one Bastion Turn.

**Armored Hull** — reduces Attack dice from 6d6 to 4d6. Cost: 250 gp per 5-ft exterior section.

| Ship State | Defense Modifier |
|---|---|
| Party aboard | Resolve through play |
| In port, party absent | RAW bastion defense |
| Underway, full experienced crew | +3 |
| Underway, skeleton crew | +0 |
| Underway, below minimum crew | −2 |

---

## Ship's Guns

**Operating a gun:** 3 crew per gun (1 fires, 2 load). 1 action to fire; 1 action to reload (light guns) or 2 actions (heavy guns). PC Gunner directs up to proficiency bonus in gun crews using their own attack roll.

**Broadside volley (ship action):** Gunner role filled + minimum crew. One attack roll; all guns on one deck/side fire. Hit = full damage; miss = half damage.

| Gun | Damage | Range | Reload |
|---|---|---|---|
| Swivel Gun | 2d6 piercing | 100/400 ft | 1 action |
| 12-lb Long Cannon | 4d10 bludgeoning | 600/2,400 ft | 1 action |
| 24-lb Long Cannon | 6d10 bludgeoning | 500/2,000 ft | 2 actions |
| 32-lb Long Cannon | 8d10 bludgeoning | 400/1,600 ft | 2 actions |
| Heavy Carronade | 10d10 bludgeoning | 150/600 ft | 1 action |
| 12-lb Chaser | 4d10 bludgeoning | 600/2,400 ft | 1 action |

**Shot types:** Round (hull damage) · Chain (half damage, −10 mi/day speed) · Grapeshot (crew DC 14 Dex or 3d6 piercing, 150 ft) · Bar (mast damage, attack at disadvantage) · Heated (hull damage + DC 12 fire risk)

Full rules: [[ship-combat|Ship Combat]] · [[ship-stats|Ship Stats]] · [[ship-bastion|Ship Bastion]] · [[ship-operations|Ship Operations]] · [[ship-upgrades|Ship Upgrades]]

# Party Combat Profile — Template & Field Rules

> Read this when compiling or updating the party-wide combat profile.

---

## Purpose

The party combat profile is the single document `prep-encounter` reads for
difficulty calibration. It compiles all PC combat profiles into actionable
encounter design parameters. Its most important output is the **Effective CR Band**
— a table-specific replacement for generic 5e difficulty thresholds.

---

## File Path

`wiki/dm/party-combat-profile.md`

---

## Frontmatter Template

```yaml
---
type: dm-intelligence
subtype: party-combat-profile
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "Party combat profile — {N} PCs, level {L}. Combined sustained DPR {X}, nova {Y}, total effective HP {Z}. Effective CR band: easy {A}, medium {B}, hard {C}, deadly {D}."
party_level: {number}
party_size: {number}
combined_sustained_dpr: {number}
combined_nova_dpr: {number}
total_effective_hp: {number}
healing_per_short_rest: {number}
effective_cr_easy: "{CR range or single value}"
effective_cr_medium: "{CR range}"
effective_cr_hard: "{CR range}"
effective_cr_deadly: "{CR range}"
confidence_level: "{high|medium|low|theoretical}"
last_compiled: "{date}"
mandatory_for: [encounter-design]
token_profile: always-read
update_trigger: "any PC profile updated"
created: "{date}"
updated: "{date}"
tags:
  - combat
  - party-profile
---
```

---

## Body Sections

### 1. Fast Read

```markdown
## Fast Read

- **Party:** {N} PCs, level {L}, tier {T}
- **Combined sustained DPR:** {number} [compiled from PC profiles]
- **Combined nova (round 1 all-in):** {number} [compiled]
- **Total effective HP:** {number} | **Healing/short rest:** {number}
- **Critical weakness:** {one sentence — the thing that will TPK them}
- **Effective CR band:** Easy {X}, Medium {Y}, Hard {Z}, Deadly {W}
```

---

### 2. Combined Offensive

```markdown
## Combined Offensive

### Party Sustained DPR (all PCs, per round, vs AC 15)

| PC | Sustained DPR | Conditions |
|---|---|---|
| {pc1} | {number} | {what must be true for this output} |
| {pc2} | {number} | {conditions} |
| ... | ... | ... |
| **Total** | **{sum}** | |

### Party Nova (round 1 maximum, all resources)

| PC | Nova damage | Resources spent |
|---|---|---|
| {pc1} | {number} | {what's burned} |
| ... | ... | ... |
| **Total** | **{sum}** | |

### Focus-Fire Potential

- **Single-target burst (1 round, 1 target):** {number} — all PCs focusing one enemy
- **Implied:** solo monsters with HP below {threshold} die in round 1-2

### AoE Capability

- **Available AoE:** {list all party AoE options with avg damage and area}
- **AoE gap assessment:** {what the party can't clear efficiently}
```

**Quality rules:**
- Sustained DPR conditions matter. "Delmar needs adjacent ally or isolated target"
  means his DPR is conditional — note when it drops.
- Focus-fire potential tells you the minimum HP a boss needs to survive round 1.
- AoE gap is a party weakness — designs that exploit it should be noted.

---

### 3. Combined Defensive

```markdown
## Combined Defensive

### AC & HP Distribution

| PC | AC | HP | Effective HP | Role |
|---|---|---|---|---|
| {pc1} | {number} | {number} | {number} | {frontline/midline/backline} |
| ... | ... | ... | ... | ... |
| **Totals** | range: {low}-{high} | {sum} | {sum} | |

### Save Distribution (party-wide weaknesses)

| Save | Lowest | Highest | Party avg | Design note |
|---|---|---|---|---|
| STR | {PC} +{N} | {PC} +{N} | +{avg} | {implication} |
| DEX | ... | ... | ... | ... |
| CON | ... | ... | ... | ... |
| INT | ... | ... | ... | ... |
| WIS | ... | ... | ... | ... |
| CHA | ... | ... | ... | ... |

### Healing Economy

| Source | Amount | Recovery | Action cost |
|---|---|---|---|
| {ability/item} | {avg healing} | {rest type} | {action/bonus/reaction} |
| **Total per short rest** | **{sum}** | | |
| **Total per long rest** | **{sum}** | | |

### Concentration Count

- PCs maintaining concentration in combat: {list with spells}
- Implied: {N} concentration checks per round of AoE damage
```

**Quality rules:**
- Save distribution is encounter gold. If the party average WIS save is +1,
  WIS-save monsters are disproportionately threatening.
- Healing economy determines how many encounters the party can survive without rest.
- Note which healing competes with other actions (opportunity cost).

---

### 4. Synergy Matrix

```markdown
## Synergy Matrix

### Confirmed Synergies (observed at table)

| Combo | PCs involved | Effect | Evidence |
|---|---|---|---|
| {name} | {pc1} + {pc2} | {mechanical result} | [session-NN] |

### Theoretical Synergies (not yet observed)

| Combo | PCs involved | Expected effect | Confidence |
|---|---|---|---|
| {name} | {pc1} + {pc2} | {predicted result} | {low/medium} |

### Force Multipliers

- **Primary multiplier:** {PC and ability} — observed to turn {X}% of failures into successes
- **Secondary multipliers:** {list}

### Coordination Bonus

The party's observed coordination consistently produces output above the sum of
individual DPR calculations. Estimated coordination multiplier: **{1.X}×** [derived
from comparing theoretical sum vs. observed party output]
```

**Quality rules:**
- Only mark a synergy as "confirmed" when there's session evidence.
- The coordination multiplier is the single most important party-specific insight.
  It tells encounter designers: "this party punches above its weight by X%."
- Force multipliers (usually bardic inspiration, flanking setups) get called out
  because removing or neutralizing them is a valid encounter pressure.

---

### 5. Weakness Map

```markdown
## Weakness Map

### Structural Weaknesses (always present)

| Weakness | Why | Severity | Counter available? |
|---|---|---|---|
| {weakness} | {mechanical reason} | {high/medium/low} | {what the party can do about it} |

### Conditional Weaknesses (situation-dependent)

| Weakness | Trigger | Effect |
|---|---|---|
| {weakness} | {when it manifests} | {what happens to party output} |

### What Will TPK This Party

- {Specific scenario with highest kill probability — be concrete}
- {Second most dangerous scenario}

### What This Party Trivializes

- {Encounter types that are reliably easy for this group}
- {Why — which PC capabilities make it trivial}
```

**Quality rules:**
- Severity ratings must be justified. "High" means the party has NO answer
  without environmental help or DM intervention.
- "What Will TPK" is the most actionable design constraint — it tells the
  designer where the line is between "hard" and "unfair."
- "What This Party Trivializes" is equally important — don't waste encounter
  budget on things they'll steamroll.

---

### 6. Effective CR Band

The core output. This is what `prep-encounter` uses for difficulty calibration.

```markdown
## Effective CR Band

### Standard 5e Thresholds (baseline reference)

| Difficulty | XP threshold | CR equivalent (single monster) |
|---|---|---|
| Easy | {xp} | CR {N} |
| Medium | {xp} | CR {N} |
| Hard | {xp} | CR {N} |
| Deadly | {xp} | CR {N} |

### Adjusted Thresholds (this party)

| Difficulty | Effective CR | Adjustment | Confidence | Evidence |
|---|---|---|---|---|
| Easy | CR {N} | {+/-X from standard} | {level} | {sessions or reasoning} |
| Medium | CR {N} | {+/-X} | {level} | ... |
| Hard | CR {N} | {+/-X} | {level} | ... |
| Deadly | CR {N} | {+/-X} | {level} | ... |

### Adjustment Rationale

- {Why this party deviates from standard thresholds}
- {Which specific capabilities drive the adjustment}
- {What encounter types DON'T follow this band (exceptions)}

### Multi-Enemy Scaling

| Enemy count | CR per enemy (for Hard) | Notes |
|---|---|---|
| 1 (solo) | CR {N} | {party focus-fires; needs legendary actions} |
| 2-3 | CR {N} each | {standard} |
| 4-6 | CR {N} each | {party lacks AoE; harder than CR suggests} |
| 7+ (horde) | CR {N} each | {attrition; party burns resources fast} |

### Environmental Modifiers

| Factor | CR adjustment | Reason |
|---|---|---|
| Darkness (full) | {+/- N} | {JC advantage but 2 PCs blinded} |
| Dim light | {+/- N} | {optimal for full party} |
| Water/vertical | {+/- N} | {party has superior mobility} |
| Enclosed/flat | {+/- N} | {denies flight and positioning} |
```

**Quality rules:**
- Base the adjustments on OBSERVED data first, theoretical analysis second.
- Multi-enemy scaling is critical because this party's strengths/weaknesses
  change dramatically based on enemy count.
- Environmental modifiers are party-specific. This party is exceptionally
  strong in dim-light multi-axis terrain and weak in flat bright enclosed spaces.
- Confidence levels are mandatory. A designer needs to know if "CR 8 = Medium"
  is based on 5 encounters or on one lucky fight.
- Mark bands derived from fewer than 3 encounters as `[low confidence]`.

---

### 7. Encounter Design Parameters

Compiled from all PC counter profiles into ready-to-use design levers.

```markdown
## Encounter Design Parameters

### Give Them (enables party strengths)

- {Terrain/condition that lets the party shine}
- {Another enabler}

### Pressure Them (targets weaknesses without being unfair)

- {Legitimate pressure that makes the party work for it}
- {Another pressure}

### Avoid (encounter design traps for this party)

- {Design choice that's either trivializing or unfair}
- {Another anti-pattern}

### Difficulty Tuning Knobs (mid-encounter adjustments)

| Knob | Turn up (harder) | Turn down (easier) |
|---|---|---|
| Enemy count | Add reinforcements wave 2 | Enemies flee at morale threshold |
| Environment | Terrain shift that removes cover/height | Terrain shift that adds it |
| Targeting | Focus the force multiplier | Split attacks |
| Resources | Force concentration saves | Offer short rest opportunity |
```

**Quality rules:**
- This section directly replaces the "Prep Levers" in the old party-combat-primer.
- Every lever must be grounded in PC profile data, not vibes.
- "Avoid" is binding for encounter design — violations require explicit DM override.

---

### 8. Update History

```markdown
## Update History

| Date | Trigger | Changes | Source sessions |
|---|---|---|---|
| {date} | {what prompted update} | {what changed} | {session numbers} |
```

---

## Compilation Protocol

When building/updating the party combat profile:

1. Read all current PC combat profiles
2. Sum/calculate combined metrics
3. Cross-reference synergies between profiles
4. Check for new weakness patterns that emerge at party level
5. Recalculate effective CR band with latest data
6. Update design parameters if any PC profile changed significantly
7. Stamp the update history

**Staleness rule:** If any PC profile has been updated more recently than the party
profile's `last_compiled` date, the party profile is stale and should be recompiled.

---

## Anti-Patterns

- **Averaging individual data without weighting.** A PC who was in 5 combats
  contributes more reliable data than one in 1 combat. Weight accordingly.
- **Ignoring conditional DPR.** Delmar's DPR is high IF conditions are met.
  The party's combined DPR should note conditions, not assume best-case.
- **Static CR bands.** The effective CR band should shift every 2-3 sessions
  as new data arrives. A band unchanged for 5+ sessions needs re-examination.
- **Forgetting the party's worst matchup.** The weakness map must include
  "this party will lose to X" — that's the designer's hard ceiling.
- **Over-precision.** CR bands are ranges, not exact numbers. "CR 7-9 = Hard"
  is more honest than "CR 8.3 = Hard."

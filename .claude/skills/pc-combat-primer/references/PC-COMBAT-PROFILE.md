# PC Combat Profile — Template & Field Rules

> Read this when creating or updating any individual PC combat profile.

---

## Purpose

A PC combat profile is the quantitative companion to the qualitative PC primer.
The primer says "spotlight with vertical space"; the profile says "sustained DPR
is 14.5, nova round is 31, effective HP is 38." Together they give an encounter
designer both the *feel* and the *math*.

---

## File Path

`wiki/dm/{pc-slug}-combat-profile.md`

---

## Frontmatter Template

```yaml
---
type: dm-intelligence
subtype: pc-combat-profile
campaign: shattered-sea
status: active
audience: agent
publish: false
summary: "{PC name} combat profile — level {N}, sustained DPR {X}, nova {Y}, effective HP {Z}. Last updated from session {NN}."
pc: "{pc-slug}"
pc_level: {number}
last_session_data: {session number or "none"}
theoretical_dpr_sustained: {number}
theoretical_dpr_nova: {number}
effective_hp: {number}
primary_save_weakness: "{lowest save type}"
confidence_level: "{high|medium|low|theoretical}"
created: "{date}"
updated: "{date}"
tags:
  - combat
  - pc-profile
update_trigger: "level-up, new session combat data, significant gear change"
---
```

---

## Body Sections

### 1. Fast Read

Four lines, scannable in 5 seconds:

```markdown
## Fast Read

- **Role:** {combat role in 3-5 words}
- **Sustained DPR:** {number} [source] | **Nova DPR:** {number} [source]
- **Effective HP:** {number} (HP {X} + avoidance modifier {Y}) [source]
- **Achilles heel:** {one sentence — what drops this PC fastest}
```

**Source tags:** `[sheet]` for character sheet math, `[session-NN]` for observed,
`[calculated]` for derived from multiple sources.

---

### 2. Offensive Profile

Calculate at current level with current gear. Show the math.

```markdown
## Offensive Profile

### Sustained DPR (per-round average across a full combat)

{Attack routine breakdown}
- Attack 1: +{to-hit} vs AC {assumed target AC}, {damage dice} + {modifier} = {avg}
- Attack 2: ...
- Conditional damage (e.g., Sneak Attack): {avg} × {probability of trigger}
- **Sustained total:** {sum} DPR [calculated]

### Nova Round (maximum single-round output, all resources spent)

- {Best possible round breakdown}
- **Nova total:** {sum} damage [calculated]

### To-Hit Analysis

| Target AC | Hit chance (per attack) | Expected DPR |
|---|---|---|
| 13 (low) | {%} | {dpr} |
| 15 (medium) | {%} | {dpr} |
| 17 (high) | {%} | {dpr} |
| 19 (boss) | {%} | {dpr} |

### Observed DPR (from session log)

- **Average actual DPR:** {number} across {N} rounds [session-NN through session-NN]
- **Peak observed round:** {number} damage [session-NN, context]
- **Lowest observed round:** {number} damage [session-NN, context]
- **Hit rate observed:** {%} across {N} attacks [sessions NN-NN]
```

**Quality rules:**
- Always calculate against AC 13/15/17/19 — these are the relevant range for this tier.
- Include advantage/disadvantage scenarios separately if the PC commonly operates in one.
- For observed data, note sample size. Mark `[insufficient data]` if fewer than 10 attack rolls.
- Bardic inspiration or other external buffs go in Synergy Hooks, not here.

---

### 3. Defensive Profile

```markdown
## Defensive Profile

| Metric | Value | Source |
|---|---|---|
| AC | {number} ({breakdown}) | [sheet] |
| HP | {current max} | [sheet] |
| Effective HP | {number} | [calculated] |
| Concentration saves | +{mod} (DC 10 floor) | [sheet] |

### Save Bonuses

| Save | Mod | Proficient? | Observed pass rate |
|---|---|---|---|
| STR | +{N} | {yes/no} | {%} or [insufficient data] |
| DEX | +{N} | {yes/no} | {%} or [insufficient data] |
| CON | +{N} | {yes/no} | {%} or [insufficient data] |
| INT | +{N} | {yes/no} | {%} or [insufficient data] |
| WIS | +{N} | {yes/no} | {%} or [insufficient data] |
| CHA | +{N} | {yes/no} | {%} or [insufficient data] |

### Effective HP Calculation

Effective HP = raw HP adjusted for avoidance, damage reduction, and escape:
- Base HP: {number}
- {Avoidance feature}: approximately {multiplier}× against {attack type}
- {Damage reduction}: reduces incoming by ~{amount} per hit
- **Effective HP:** {final number} [calculated]

### Escape & Recovery

- {List abilities that avoid or mitigate damage: Uncanny Dodge, Patient Defense,
  Misty Step, flight escape, etc.}
```

**Quality rules:**
- Effective HP is NOT just raw HP. A rogue with Uncanny Dodge at 30 HP has
  ~45 effective HP against single-target damage. A monk with Patient Defense
  active has higher effective HP than listed. Show the reasoning.
- Save bonuses are the most important defensive data for encounter design.
  Knowing a PC has +0 WIS save means WIS-save enemies are more threatening.
- Concentration saves matter for casters — note them specifically.

---

### 4. Resource Economy

```markdown
## Resource Economy

### Per Short Rest

| Resource | Pool | Avg uses/combat | Recovery |
|---|---|---|---|
| {resource name} | {max} | {observed or estimated} | Short rest |

### Per Long Rest

| Resource | Pool | Avg uses/combat | Recovery |
|---|---|---|---|
| {resource name} | {max} | {observed or estimated} | Long rest |

### Attrition Pressure

- Combats before resource-starved: ~{number} (assuming no short rests)
- Most-constrained resource: {name} — runs out first in observed play
- Least-constrained: {name} — rarely fully expended
```

**Quality rules:**
- "Avg uses/combat" should be observed where possible. Mark theoretical estimates.
- Attrition pressure is critical for adventure-day pacing.

---

### 5. Counter Profile

```markdown
## Counter Profile

### Hard Counters (reliable shutdown)

| Counter | Why it works | Observed? |
|---|---|---|
| {condition/tactic} | {mechanical reason} | {session-NN or theoretical} |

### Soft Counters (reduces effectiveness)

| Counter | Effect | Observed? |
|---|---|---|
| {condition/tactic} | {what it reduces} | {session-NN or theoretical} |

### What This PC Can't Handle

- {Specific scenario this PC has no answer for}
- {Another gap}
```

**Quality rules:**
- Hard counter = reduces this PC's output by 75%+ or removes them from combat.
- Soft counter = reduces output by 25-75% or forces suboptimal play.
- Always note whether a counter is theoretical or observed at table.
- The "Can't Handle" list feeds the party weakness map.

---

### 6. Synergy Hooks

```markdown
## Synergy Hooks

### This PC Amplifies

| Target | Mechanic | Multiplier estimate |
|---|---|---|
| {other PC} | {how this PC enables them} | {rough % boost or description} |

### This PC Depends On

| Source | Mechanic | Impact when absent |
|---|---|---|
| {other PC} | {what they provide} | {what happens without it} |

### Observed Combos (from sessions)

- **{Combo name}:** {description} — resulted in {outcome} [session-NN]
```

**Quality rules:**
- Synergy data is crucial for the party combat profile's synergy matrix.
- "Multiplier estimate" can be rough: "+2 to hit from advantage = ~25% DPR boost."
- Observed combos go here when they happen; these feed calibration.

---

### 7. Session Combat Log

**Append-only.** Never edit or delete previous entries.

```markdown
## Session Combat Log

| Session | Encounter | Rounds active | Damage dealt | Damage taken | Hits/Attacks | Key moments |
|---|---|---|---|---|---|---|
| 03 | Whip shark | 3 | 22 | 8 | 4/6 | Lifted shark from water (grapple) |
| 04 | Kyzil spar | 3 | 18 | 31 | 3/7 | Grappled R1 (Kyzil nat 1); stunning failed |
| 04 | Grung sewer | 1 | 12 | 0 | 2/2 | Clotheslined Grung; kingfisher dive capture |
```

**Columns:**
- **Rounds active:** How many rounds this PC was in combat (not total encounter length)
- **Damage dealt:** Total damage this PC inflicted
- **Damage taken:** Total damage this PC received
- **Hits/Attacks:** Successful attacks / total attacks attempted
- **Key moments:** One-line notable actions (clutch saves, tactical plays, failures)

**Quality rules:**
- Record 0s honestly. A PC who dealt 0 damage in a round is data.
- If exact numbers aren't available from transcript, estimate with `~` prefix.
- Key moments are for calibration — "what did this PC actually do?" not flavor.

---

### 8. Calibration Notes

```markdown
## Calibration Notes

### Theoretical vs. Observed Delta

- **DPR delta:** theoretical {X} vs. observed average {Y} ({reason for gap})
- **Hit rate delta:** theoretical {X}% vs. observed {Y}% ({reason})
- **Survivability:** theoretical {X} effective HP, observed {assessment}

### Design Implications

- {What encounter designers should know from this data}
- {How this PC performs relative to expectations}
- {Specific adjustments for future encounters}

### Confidence Assessment

- **Offensive data:** {confidence level} — based on {N} combat rounds
- **Defensive data:** {confidence level} — based on {N} instances of taking damage
- **Resource data:** {confidence level} — based on {N} full encounters observed
```

**Quality rules:**
- The delta between theoretical and observed is the most valuable insight.
  A PC whose theoretical DPR is 15 but observed is 8 means something — bad luck,
  suboptimal play, encounter design that doesn't enable them, or the math is wrong.
- Design implications should be actionable. Not "Delmar is good" but "Delmar needs
  isolated targets within 30ft to perform at theoretical DPR."
- Update confidence assessment every time new data arrives.

---

## Anti-Patterns

- **Mixing theoretical and observed in one number.** Keep them in separate fields.
- **Averaging without sample size.** "Average DPR: 12" means nothing without N.
- **Ignoring 0-damage rounds.** These are the most important data for counter profiles.
- **Calculating in a vacuum.** DPR against what AC? Always state the assumption.
- **Optimistic theoreticals.** Calculate sustained DPR assuming average rolls and
  no advantage unless the PC has a reliable source of it.
- **Forgetting positioning.** A melee PC's effective DPR drops if enemies are 60ft away.
  Note range assumptions.

---

## Example: Partial Profile (Crissdalynn, Level 4)

```markdown
## Fast Read

- **Role:** Mobile aerial striker
- **Sustained DPR:** 14.5 vs AC 15 [calculated] | **Nova DPR:** 31 [calculated]
- **Effective HP:** 38 (HP 31 + Deflect Attacks ~7 effective) [calculated]
- **Achilles heel:** Blinded in darkness; no darkvision means magical darkness = 0 DPR

## Offensive Profile

### Sustained DPR (vs AC 15, no advantage)

- Unarmed Strike 1: +6 to hit (60% hit), 1d6+4 = 7.5 × 0.6 = 4.5
- Unarmed Strike 2 (Flurry): +6 to hit (60%), 1d6+4 = 7.5 × 0.6 = 4.5
- Bonus Unarmed (Flurry): +6 to hit (60%), 1d6+4 = 7.5 × 0.6 = 4.5
- Eldritch Claw (1/dawn, first hit): +1d6 force = 3.5 (amortized ~1.0/round)
- **Sustained total:** 14.5 DPR [calculated] (Flurry active, 1 ki/round)

### Nova Round

- 3 attacks as above: 22.5 expected
- Eldritch Claw bonus: +3.5
- Crit chance (5% × 3): ~1.1 extra
- Grapple → prone → advantage chain (if setup): attacks at advantage = ~19.5 DPR
- **Nova (with advantage setup):** ~31 damage [calculated]
```

# Data Extraction Protocol

> Read this when processing session combat data into PC combat profile updates.

---

## Purpose

Session transcripts and scene files contain raw combat information. This protocol
defines how to extract quantitative data and append it to PC combat profiles without
losing fidelity or introducing assumptions.

---

## Source Priority

When extracting combat data, prefer sources in this order:

1. **Session-ingest combat summary** (`audio/sessions/session{NN}/combat-summary.md`)
   — already structured with per-PC tables and encounter headers. If this exists,
   it is the primary source — skip re-processing transcripts.
2. **Session-ingest extracts** (`audio/sessions/session{NN}/extracts.md`, `[COMBAT]` blocks)
   — same data, interleaved with other tags. Use if combat-summary.md doesn't exist yet.
3. **Session scene files** (`wiki/sessions/session-{NN}-scene-*`) — structured but
   may lack per-PC granularity.
4. **Session recaps** (`wiki/sessions/session-{NN}-recap.md`) — least granular,
   last resort.

The `session-ingest` skill produces combat data in the structured format this
protocol expects (encounter header + per-PC table + party state). When that
output exists, extraction is a mapping exercise, not a re-read of transcripts.

---

## What to Extract

### Per-PC, Per-Encounter

| Field | Source hint | If unavailable |
|---|---|---|
| Rounds active | Count described rounds | Estimate from encounter length |
| Total damage dealt | Sum all mentioned damage numbers | Mark `~` with best estimate |
| Total damage taken | Sum all mentioned incoming damage | Mark `~` |
| Attacks attempted | Count attack descriptions | Mark `[unknown]` |
| Attacks hit | Count successful attacks | Mark `[unknown]` |
| Saves forced on PC | Count mentioned saves | Mark `[unknown]` |
| Saves passed/failed | Count results | Mark `[unknown]` |
| Resources spent | List abilities/slots used | Note what's mentioned |
| Key moments | 1-2 notable tactical actions | Always extractable |

### Per-Encounter (party-wide)

| Field | Source hint |
|---|---|
| Total encounter rounds | Count or estimate from narrative |
| Enemy count and types | Named in scene setup |
| Estimated CR/difficulty | From encounter prep or post-hoc assessment |
| Outcome | Win/loss/retreat/social resolution |
| Party HP at end | If mentioned |
| Rest before next encounter | If mentioned |

---

## Extraction Rules

### Rule 1: Record Actuals, Not Intentions

```
GOOD: "Delmar dealt 17 damage with Sneak Attack" → record 17
BAD:  "Delmar could deal up to 2d6+4+2d6" → this is theoretical, not extraction
```

### Rule 2: Mark Uncertainty

- `~14` = approximate (narrator said "about 14" or context implies it)
- `[unknown]` = not available from source
- `[inferred]` = derived from context (e.g., "badly wounded" on a monster = ~50% HP)
- Never invent numbers. Better to mark `[unknown]` than guess.

### Rule 3: Context Matters

Record the circumstances alongside the numbers:
- Was the PC advantaged/disadvantaged?
- Were they operating in ideal conditions for their build?
- Were they shut down by something specific?

This context feeds the calibration notes, not just the raw numbers.

### Rule 4: Negative Data is Data

A PC who dealt 0 damage, missed every attack, or was incapacitated is important
information. Record it — it feeds the counter profile and observed-vs-theoretical delta.

### Rule 5: Don't Double-Count Synergy

If Perrin's Bardic Inspiration turned Delmar's miss into a hit:
- Record the damage under Delmar (he dealt it)
- Note the inspiration use under Perrin's "Resources spent"
- Note the combo in both PCs' synergy observations

---

## Extraction Procedure

### Step 1: Identify Combat Data

Check sources in priority order (see Source Priority above):
- If `audio/sessions/session{NN}/combat-summary.md` exists → use it directly,
  skip to Step 3
- If `extracts.md` exists with `[COMBAT]` blocks → compile them, skip to Step 3
- Otherwise scan scene files for `tags: [combat]`, `## What Happened (Played)`,
  initiative descriptions, attack rolls, damage numbers

### Step 2: Build Round-by-Round if Possible

For each round mentioned:
- Who acted (PC turn order if discernible)
- What they did (attack, spell, ability, movement, help)
- Result (hit/miss, damage, effect)
- Enemy actions against PCs

If round-by-round isn't available, extract totals per encounter.

### Step 3: Fill the Session Combat Log Entry

For each PC, create one row per encounter:

```markdown
| {session} | {encounter name} | {rounds} | {damage dealt} | {damage taken} | {hits/attacks} | {key moment} |
```

### Step 4: Update Observed Averages

After appending new log entries, recalculate:
- Average DPR (total damage dealt ÷ total rounds, across all logged encounters)
- Hit rate (total hits ÷ total attacks)
- Average damage taken per round
- Peak and trough rounds

### Step 5: Flag Calibration Shifts

If new data significantly changes any of these, note in calibration:
- Observed DPR diverging from theoretical by >25%
- A counter that worked at table (add to counter profile)
- A synergy that fired successfully (confirm in synergy hooks)
- A new weakness discovered

---

## Handling Incomplete Data

Session transcripts vary in detail. Here's how to handle common gaps:

| Gap | Approach |
|---|---|
| No specific damage numbers | Use monster stat block + described outcome to estimate |
| No round count | Estimate from narrative pacing (most combats = 3-5 rounds) |
| Mixed combat/social scene | Only extract the initiative-tracked portion |
| PC was absent from combat | Record `rounds: 0, damage: 0, taken: 0` with note |
| Multiple combats, unclear separation | Treat as separate encounters if there's any pause between |

---

## Example Extraction

**Source:** Session 04, Kyzil spar scene

```
Relevant transcript data:
- 4v1 spar, non-lethal, 3 rounds
- Crissdalynn grappled R1 (Kyzil rolled nat 1 on contest)
- Perrin's bardic inspiration saved two key moments
- Delmar landed sneak attack through Empty Wing Parry via inspiration — 17 damage
- Kyzil brought Delmar to 2 HP
- Crissdalynn's stunning strike failed (Kyzil's CON save too high)
```

**Extracted for Delmar:**

| Session | Encounter | Rounds | Damage dealt | Damage taken | Hits/Attacks | Key moments |
|---|---|---|---|---|---|---|
| 04 | Kyzil spar | 3 | 17 | ~29 | 1/[unknown] | SA through Empty Wing via inspiration; dropped to 2 HP |

**Extracted for Crissdalynn:**

| Session | Encounter | Rounds | Damage dealt | Damage taken | Hits/Attacks | Key moments |
|---|---|---|---|---|---|---|
| 04 | Kyzil spar | 3 | ~12 | [unknown] | [unknown] | Grappled R1 (nat 1 contest); stunning strike failed (high CON) |

**Calibration flags:**
- Delmar's HP of ~31 means 29 damage = nearly dropped. Against CR 14, his survivability
  is razor-thin without Uncanny Dodge (which he doesn't have yet at L4).
- Crissdalynn's stunning strike failed against high CON — confirms counter profile:
  high CON saves resist her control.
- Bardic inspiration directly enabled Sneak Attack — confirms synergy: Perrin → Delmar
  multiplier is real and observed.

---

## Update Cadence

| Trigger | Action |
|---|---|
| Session ingested with combat data | Append to all participating PC session logs |
| 2+ new session entries since last avg recalc | Recalculate observed averages |
| PC levels up | Recalculate theoreticals; do NOT change historical observed data |
| Party profile is stale | Recompile party profile from updated PC profiles |

---

## Integration with Session Ingest

When `session-ingest` processes a session with combat:

1. Session-ingest extracts `[COMBAT]` blocks with per-PC tables during Pass 2
2. After the final part, session-ingest compiles all `[COMBAT]` blocks into
   `audio/sessions/session{NN}/combat-summary.md`
3. The handoff notes: "Combat data available — run pc-combat-primer to update
   affected profiles."
4. This skill reads `combat-summary.md` and maps each per-PC table row directly
   to a session combat log entry (the columns are 1:1)
5. PC profiles are updated with new session log entries
6. If 2+ new encounters are logged, recalculate observed averages
7. Flag party profile as stale

### Field Mapping: combat-summary.md → Session Combat Log

| combat-summary column | Profile log column | Notes |
|---|---|---|
| PC | (row identity) | Match to `{pc-slug}` |
| Rounds | Rounds | Direct |
| Damage Dealt | Damage dealt | Direct |
| Damage Taken | Damage taken | Direct |
| Hits/Attacks | Hits/attacks | Direct |
| Saves (Pass/Fail) | — | Record in calibration notes if notable |
| Resources Spent | — | Record in resource economy observations |
| Key Moment | Key moments | Direct |

Encounter-level fields (enemy types, CR, outcome) go in the log entry's
encounter name and the calibration notes section.

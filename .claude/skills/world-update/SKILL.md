---
name: world-update
description: >
  Advance the living world for the Shattered Sea campaign — the canon owner of faction-clock
  writes. Two modes. POST-SESSION (default): after every session, run the full tick — triage
  every thread into hot/warm/cold, roll d20 for each, weave PC arcs, write all changes. Trigger
  on: "world update", "post-session update", "update after session N", "run the world forward",
  "tick the world", "advance the world after session". ON-DEMAND / MID-SESSION clock advance:
  advance specific faction clocks in response to party action or inaction without the full
  ritual. Trigger on: "advance the factions", "advance the clocks", "what do the factions do",
  "what happened offscreen", "what is [faction] doing right now", "between sessions", "faction
  clock", "world tick", "simulate the world". Never advances a clock without citing the situation
  that justifies it. Never fires a triggered (filled) clock without flagging it to the DM first.
---

# World Update — Living-World Advancement

The world didn't pause while the party played. Now it moves.

Factions pursue goals. Villains continue plans. Consequences compound. And slowly, session by
session, the four PCs' stories weave together — not through plot, but through the pressure the
world applies to the people they've become.

**Core question (every mode, every thread):** *If the party had done nothing, what would have
changed anyway?* Factions pursue their own goals. The party is one variable — not the engine.

---

## Modes

| Mode | When | What it does |
|---|---|---|
| **Post-session tick** (default) | After a session, once a recap exists | Full ritual: triage all threads hot/warm/cold → roll each → interpret → write → weave PC arcs → close out. Read `references/update-workflow.md`. |
| **On-demand clock advance** | Mid-session, or a focused "what are the factions doing" check between sessions | Advance specific faction clocks only (see *Clock Advance* below). No full triage, no PC-arc weaving. |

Both modes own canon clock writes. The clock-advance discipline below applies to both.

---

## Clock Advance (both modes)

For each faction with an active clock in `wiki/hot.md`:

1. Read their situation file — what is the trigger condition for each segment?
2. Did that trigger condition occur this session / interval? (party action or world-state change)
3. **Yes** → advance the clock. Record citation: `[from: {situation-slug}]`. Never advance without one.
4. **Clock fills** → **flag to DM, do not fire.** No triggered event executes without DM confirmation.
5. **No trigger** → document what the faction did anyway (minimum passive activity). Factions don't
   pause — they do something, even if the clock doesn't advance.

---

## Post-Session: When to Use

Run after every session, once a session recap exists. Input priority:

1. Session recap file (`wiki/sessions/session-NN-recap.md`) — preferred
2. Session summary or DM notes — if recap lacks detail
3. Raw transcript — fallback for ambiguous events

If no recap exists yet, ask the DM for a quick rundown before proceeding.

### Thread Priority Chain

Threads are triaged into three tiers and processed in this order:

| Tier | What it covers | Roll determines |
|---|---|---|
| **HOT** | Directly engaged this session | How effectively the faction/force reacts to party action |
| **WARM** | Party engaged before, not this session | How much the faction advances its agenda while party is elsewhere |
| **COLD** | Brewing — party unaware or disengaged | How far the villain/force advances its plan unopposed |

**HOT** threads get full treatment — detailed interpretation, multiple wiki writes, narrative
device consideration. **WARM** threads get one action and one visible ripple the party could
notice. **COLD** threads get one sentence of offscreen movement and a hook that strengthens. As
cold threads accumulate advances across sessions, their hooks escalate from whisper to collision.

### Workflow

Read `references/update-workflow.md` for the complete step-by-step ritual. Summary:

1. **Load context** — session recap, hot.md, situation frontmatter (summaries only)
2. **Triage** — classify threads as HOT / WARM / COLD; present for DM confirmation
3. **Process each thread** — deep read situation + linked entities → Context Brief → propose action
   → roll d20 via roll.sh → interpret → write (one thread at a time)
4. **PC arc weaving** — convergence scan, spotlight check, narrative device seeding
5. **Close out** — update hot.md, situation lifecycle, commit

---

## Relationship to Other Skills

| Skill | Relationship |
|---|---|
| `sandbox-narrative` | Load for narrative device application during PC arc weaving. |
| `ttrpg-writing` | Load for prose standards when writing wiki updates. |
| `roll-dice` | Every thread/clock advancement uses `roll.sh d20`. The result is canon. |
| `prep-session` | For *prep-time pending pressure* (not canon), prep-session simulates likely clocks as pending. world-update owns the canon write and feeds next session's prep via hot.md predictions. |

---

## Reference Files

| File | Read when |
|---|---|
| `references/update-workflow.md` | Post-session tick — the complete ritual workflow |

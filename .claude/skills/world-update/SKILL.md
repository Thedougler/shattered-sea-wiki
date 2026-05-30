---
name: world-update
description: >
  Use after every session to advance the living world. Trigger on: "world update",
  "post-session update", "update after session N", "run the world forward", "living
  world update", "tick the world after session", "advance the world after session".
  Processes session recap through three priority tiers of threads (hot/warm/cold),
  rolls d20 for each, weaves PC arcs, writes all changes to wiki.
---

# World Update — Post-Session Living-World Advancement

The world didn't pause while the party played. Now it moves.

This is the post-session ritual that advances every active thread based on what
happened at the table and what happened offscreen. Factions pursue goals. Villains
continue plans. Consequences compound. And slowly, session by session, the four PCs'
stories weave together — not through plot, but through the pressure the world applies
to the people they've become.

**Core question:** What changed while they were busy? What changed because of what
they did? Roll the dice. Find out.

---

## When to Use

Run this after every session, once a session recap exists. Input priority:

1. Session recap file (`wiki/sessions/session-NN-recap.md`) — preferred
2. Session summary or DM notes — if recap lacks detail
3. Raw transcript — fallback for ambiguous events

If no recap exists yet, ask the DM for a quick rundown before proceeding.

---

## Relationship to Other Skills

| Skill | Relationship |
|---|---|
| `faction-clock` | world-update supersedes the world-tick ritual — broader scope, automated rolls, PC weaving. faction-clock remains useful for focused mid-session clock checks. |
| `sandbox-narrative` | Load for narrative device application during PC arc weaving. |
| `ttrpg-writing` | Load for prose standards when writing wiki updates. |
| `roll-dice` | Every thread advancement uses `roll.sh d20`. The result is canon. |
| `prep-session` | world-update feeds directly into next session's prep via hot.md predictions. |

---

## Thread Priority Chain

Threads are triaged into three tiers and processed in this order:

| Tier | What it covers | Roll determines |
|---|---|---|
| **HOT** | Directly engaged this session | How effectively the faction/force reacts to party action |
| **WARM** | Party engaged before, not this session | How much the faction advances its agenda while party is elsewhere |
| **COLD** | Brewing — party unaware or disengaged | How far the villain/force advances its plan unopposed |

**HOT** threads get full treatment — detailed interpretation, multiple wiki writes,
narrative device consideration.

**WARM** threads get one action and one visible ripple the party could notice.

**COLD** threads get one sentence of offscreen movement and a hook that strengthens.
As cold threads accumulate advances across sessions, their hooks escalate from whisper
to collision — the party engages or the thread comes to them.

---

## Workflow

Read `references/update-workflow.md` for the complete step-by-step ritual.

Summary:

1. **Load context** — session recap, hot.md, active situations
2. **Triage** — classify threads as HOT / WARM / COLD; present for DM confirmation
3. **Process each thread** — propose action, roll d20 via roll.sh, interpret, write
4. **PC arc weaving** — convergence scan, spotlight check, narrative device seeding
5. **Close out** — update hot.md, log.md, situation lifecycle, commit

---

## Reference Files

| File | Read when |
|---|---|
| `references/update-workflow.md` | Always — the complete ritual workflow |

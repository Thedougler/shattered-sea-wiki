---
name: faction-clock
description: >
  Simulate what factions do between sessions for the Shattered Sea campaign. Invoke for:
  "advance the factions", "what do the factions do", "update the clocks", "advance the
  world", "what happened offscreen", "between sessions", "faction clock", "world tick",
  "simulate the world", "what is [faction] doing right now". Reads hot.md faction clocks
  and active situation files. Determines what each faction does given party actions or
  inaction. Advances clocks, identifies triggered events, updates hot.md. Never advances
  a clock without citing the situation that justifies it. Never fires a triggered event
  without flagging it to the DM first.
---

## Prerequisites

1. Read `wiki/hot.md` — current faction clocks, fill state, trigger conditions
2. Read `wiki/situations/active/` — all active situation files for relevant factions
3. Read most recent session summary (`wiki/sessions/sNNN-summary.md`) — what did the
   party actually do?

---

## Core Question

**If the party had done nothing this session, what would have changed anyway?**

Answer this for every active faction before determining party-influenced advances.
Factions pursue their own goals. The party is one variable — not the engine.

---

## Clock Advance Workflow

For each faction with an active clock:

1. Read their situation file — what is the trigger condition for each segment?
2. Did that trigger condition occur this session? (party action or world state change)
3. **Yes** → advance the clock. Record citation: `[from: {situation-slug}]`
4. **Clock fills** → **flag to DM, do not fire.** No triggered event executes without DM
   confirmation.
5. **No trigger** → document what the faction did anyway (minimum passive activity).
   Factions don't pause — they do something, even if the clock doesn't advance.

---

## Output

After processing all factions, produce:

1. **Advance summary** — which clocks advanced, by how much, why, citation
2. **Triggered events** — any clocks that filled (flagged for DM, not fired)
3. **Off-screen activity** — what each faction did that the party won't immediately
   know about
4. **hot.md update** — rewrite the faction clocks block with new fill states and notes

Read `references/world-tick.md` for the full post-session world advancement ritual that
wraps faction clock advances into the complete between-session update.

---

## Reference Files

| File | Read when |
|---|---|
| `references/world-tick.md` | Full post-session world advancement ritual and workflow |

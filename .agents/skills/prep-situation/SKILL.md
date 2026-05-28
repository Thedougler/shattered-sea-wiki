---
name: prep-situation
description: >
  Create or expand a situation file for the Shattered Sea campaign. Invoke for:
  "create a situation for [conflict]", "track [event] with a clock", "this needs a
  lifecycle", "file this as a situation", any world pressure with a timeline or trigger
  condition. Generates frontmatter with lifecycle and island fields, clock definition,
  trigger conditions, involved entities, possible outcomes, Three Clue placement (when
  applicable), and DM notes. Places correctly in wiki/situations/active/ or
  wiki/situations/dormant/ per lifecycle state.
---

## Prerequisites

1. Check `wiki/index.md` — stub exists? Expand it; don't recreate.
2. Read `wiki/hot.md` — what factions and active situations already exist? Avoid redundancy.
3. Determine whether this situation has a hidden conclusion (mystery, secret faction, hidden
   cause) — if yes, Three Clue Rule applies.

---

## Interview

If the user message doesn't already answer these, ask all at once — not one at a time:
- What is the core tension or unresolved pressure? (One sentence)
- Which PC thread does this pull on, and how?
- Is the clock currently running (active) or waiting for a trigger (dormant)?
- What happens when the clock fills — what is the consequence?

PC connection is required. If you cannot name it, ask before generating.

---

## Situation Shape

### Lifecycle Decision

| State | Meaning | File path |
|---|---|---|
| `active` | Clock is running right now | `wiki/situations/active/slug.md` |
| `dormant` | Clock starts on a named trigger | `wiki/situations/dormant/slug.md` |
| `resolved` | Situation concluded | `wiki/situations/resolved/slug.md` |

### Clock Definition

Every situation gets a clock unless it resolves on first contact.

```yaml
clocks:
  - name: "[Short descriptive name]"
    segments: 4   # 4 for fast-moving; 6 for slow burns
    filled: 0
    trigger: "[What advances this — player inaction, faction action, or elapsed time]"
    consequence: "[What happens at fill — specific, observable, irreversible]"
```

Consequence rules: specific > vague. Observable > atmospheric. Irreversible > undoable.

---

## Three Clue Rule

**Apply when:** the situation has a hidden conclusion — a truth players must reach to engage
meaningfully (concealed cause, secret faction, hidden threat).

**Skip when:** the situation is fully visible — players can already see the faction advancing,
the NPC defecting, the trade route collapsing. No clues needed for what's already apparent.

When the rule applies, three distinct clues are required before the page is complete.
Redundancy rule: clues must span different nodes. Two clues at the same location fails.

```
## Three Clue Audit
Conclusion: [One sentence — what players must understand]
Clue 1: [Location or NPC] — [How it is found — specific discovery mechanic]
Clue 2: [Different location or NPC] — [Different mechanic]
Clue 3: [Third node] — [Third mechanic]
Note: at least two clues reachable without combat.
```

If you cannot name three distinct clues, the situation is incomplete. Add access points
before writing the page.

---

## Faction Timeline

What happens if the players do nothing? Map this explicitly — it is a playable consequence
chain, not flavor.

| Interval | Actor Action | Observable Signal |
|---|---|---|
| Day 1 | [what they do right now] | [what players could notice] |
| Day 3 | [next step] | [what changes visibly] |
| Day 7 | [escalation or clock fill] | [consequence at the table] |

If the situation doesn't involve a faction, apply the same format with the relevant actor
(NPC, environmental hazard, political body).

---

## Possible Outcomes

2–3 outcomes. None requiring a specific player choice or player presence.

```
**[Outcome Name]:** [What happens — one sentence. Observable, specific, irreversible.]
[Which entities are affected and how.]
```

Railroading check: if every outcome requires the players to do X first, rewrite. Situations
resolve with or without party involvement. Player action changes *which* outcome, not
*whether* one occurs.

---

## Output Sections

1. `> [!dm]` — one-line situation brief: who wants what, what's in the way
2. `## Summary` — 2–3 sentences (this fills the `summary` frontmatter field)
3. `## Clock` — name, segments, current fill, trigger, consequence
4. `## Involved Entities` — wikilinks only
5. `## Three Clue Audit` — include only if hidden-conclusion situation
6. `## Faction Timeline` — Day 1 / Day 3 / Day 7 table
7. `## Possible Outcomes` — 2–3 outcomes, none requiring specific player action
8. `## DM Notes` — contingencies, secret connections, things only the DM knows

---

## Frontmatter

```yaml
---
type: situation
subtype: conflict  # conflict | mystery | political | environmental | personal
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: "[One sentence: what is at stake and who is driving it]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [situation]
sources: [Homebrew]
lifecycle: active  # active | dormant | resolved
island: null  # or "[[island-slug|Island Name]]"
clocks:
  - name: ""
    segments: 4
    filled: 0
    trigger: ""
    consequence: ""
---
```

---

## Filing

After writing the page:
1. Place at `wiki/situations/active/slug.md` or `wiki/situations/dormant/slug.md`
2. Add entry to `wiki/index.md` under `## situations`
3. Add reciprocal links to all referenced entities and factions
4. If the situation has a faction clock: add or update entry in `wiki/hot.md`
5. Commit: `feat: situation — {slug} — {one-line summary}`

---

Load `ttrpg-writing` for all prose and formatting standards — DM-facing reference mode,
anti-slop constraints, and callout types apply to every situation page.

---

**Coordinates with:** `wiki-categorize`, `faction-clock`, `sandbox-narrative`

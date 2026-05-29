# Session Run Guide Reference

The complete spec for building a Shattered Sea session run guide: the inline-first contract, the assembly workflow, every section with a worked example, the module formatting craft, the file template, and the quality gate.

A run guide is a **scannable operating document the DM runs cold at the table.** Not a script, not prose. Judge every line by one test: *does this help the DM run the next beat without opening another file?* If not, cut it or link it.

## Contents

- The Inline-First Contract
- Assembly Workflow
- Section Specs (with examples)
  - Session Snapshot
  - Strong Start
  - Scene Menu
  - NPC Bench
  - Threads & Clocks
  - Spotlight
  - Secrets & Clues
  - If They Surprise You
  - Possible Cliffhanger
  - Capture For Next Time
- Module Formatting Craft
- File Template
- Quality Gate

---

## The Inline-First Contract

Everything the DM needs to run a beat lives at the point they run it. Wikilinks are for depth chased between sessions, never for retrieval mid-session. Concretely, a beat is "complete" when the DM could run it with the rest of the wiki closed:

| The DM needs… | Put it inline as… | Link the… |
|---|---|---|
| To open the scene | A `> [!read-aloud]` box, ready to speak | — |
| To play the NPC | One-line handle (voice + behaviour) + their want right now + the one thing they'll reveal or do | Full NPC page for backstory |
| To resolve a roll | A `> [!skill-check]` callout: ability, DC, what success *and* failure each reveal | Rules page if the mechanic is exotic |
| To run a fight | Compact stat line — AC, HP, to-hit or save DC, key damage, one tactic | Full statblock page |
| To drop a clue | The fact stated plainly + which actions surface it | Source page for the lore behind it |
| To judge consequence | "If engaged / If ignored" lines | — |

The failure mode to design against: a guide that is really a table of contents pointing elsewhere. Links are cheap and feel comprehensive, but at the table they cost the DM the one thing they don't have — time and attention. Bring the answer to them.

---

## Assembly Workflow

1. **Ground in current state** — `wiki/hot.md`, the latest `wiki/sessions/session-NN-recap.md`, active situation files near the party, relevant entity pages (summaries first). Stop when you have enough; never read the whole vault.
2. **Answer the Session Snapshot questions** (below) from the wiki. If you can't answer one, that's the first thing to resolve.
3. **Choose structure.** Default to a **scene menu** — 3–5 live situations the party can approach in any order. Use a **scene order** only when canon has already put the party inside a fixed sequence (an unresolved fight, a cliffhanger, a ship crisis, an arrival established last session). Even then, keep everything after the fixed opening modular.
4. **Write the Strong Start** (see `references/STRONG-START.md`).
5. **Pick threads and pace** (see `references/PACING.md`): 2–3 threads to advance, register varied.
6. **Draft each section** inline-first, in template order.
7. **Run the Quality Gate.**
8. **If writing to the wiki:** save under `wiki/sessions/session-NN-run-guide.md`, fill the frontmatter (the hook completes the rest), and update `wiki/hot.md` if prep revealed a state change. Commit. Do not touch unrelated dirty files.

**Decompose before drafting.** A run guide has many sections; write them one at a time to completion, not all at once in a single pass — that is how scenes end up thin and inconsistent.

---

## Section Specs

### Session Snapshot

A four-row table the DM reads in ten seconds to know where they stand. No prose.

```markdown
## Session Snapshot

| | |
|---|---|
| **Party is** | [[la-vasca\|La Vasca]] dry dock, Calveno — ship hidden, ~5 days shore leave |
| **Last break** | Session 03 ended as the *Surety* settled into the cradle |
| **Hottest pressure** | Beffe registration opens at dawn; Nona already knows Perrin is here |
| **Table time** | ~3.5 hrs; plan 3 scenes, 1 optional |
```

Do not infer where the party will go. State only what canon or the DM has established.

### Strong Start

One in-medias-res opening: present tense, second person, one concrete image, one immediate pressure, **no recap**. The party is already mid-something. End at the decision point and stop. Full construction guidance and the five types: `references/STRONG-START.md`.

```markdown
## Strong Start

> [!read-aloud]
> The cradle under the *Surety* groans upward, wet timber taking the ship's weight an inch at a time. Beyond La Vasca's arch, Calveno is already moving — festival cloth piled higher than the skiffs carrying it, a bell up toward the Mercatura marking the turn of the working day. Sem is naming repairs. Cobb is naming who'll hear you're here.

Then stop and ask what matters first. Do not narrate their answer.
```

Pair the box with a one-line DM cue when the opening needs framing ("Then stop and ask…") — but the box itself never tells players what they feel or decide.

### Scene Menu

3–5 simultaneous situations, offered through the world when player intent points at them — never announced as a quest board. Each scene is self-contained per the Inline-First Contract.

**Per scene, in this shape:**

```markdown
### The Warren Route
*Pull: Perrin (family), Delmar · Register: social*

> [!read-aloud]
> [Optional sensory opener if the scene has a clear entry moment.]

**What's true here:** [[savia-brentino\|Savia Brentino]] at the [[carpenters-slip\|Carpenters' Slip]] does hull work off the Commission's books — but not for a cold approach. Three ships tried this month and are on her list now.

**NPC — Savia:** dry, unhurried, says the hard thing once and lets it sit. *Wants:* a Warren introduction before she'll deal. *Reveals (flatly, at the end):* "She'll still read as a cutter to anyone who knows cutters. That's not a paint problem."

> [!skill-check] Insight (DC 13)
> Success: Savia isn't hostile — she's been burned and is screening. Failure: she reads as a dead end.

**If engaged:** 220 gp + 5 city days + one unassigned Tangle favour; the cutter-silhouette problem is now the party's to solve.
**If ignored:** repairs proceed cosmetically; the silhouette and Crown clock remain live.
**Hook out:** the Warren introduction routes through [[warren-nonas-table\|Nona's Table]].
```

**Sandbox rules for the menu:**
- Every scene has an **if ignored** consequence, or it is a resolved/required logistics beat. Ignored ≠ deleted — the pressure *moves*, it doesn't vanish. Say where it goes.
- **No scene may depend on the party having chosen another scene first.** A scene may depend on established canon, never on a future player choice. If scene B only works after scene A, rewrite the prep.
- Mark the genuinely cuttable scene `*(optional)*` — and make it the most fun one, so if it's skipped the loss is felt, not the session.

### NPC Bench

A quick-reference table of everyone likely to matter, with a **table handle** — the one line that lets the DM play them instantly. Cap at ~8 unless the session is festival-scale. This complements (doesn't replace) the inline NPC notes in each scene; it's the at-a-glance roster.

```markdown
## NPC Bench

| Face | Grab them when | Table handle | Wants now |
|---|---|---|---|
| [[nona-black-jaw\|Nona Black-Jaw]] | Perrin's family pressure lands | Feeds you first, then names what you owe — as accounting, not threat | The Tangle's favour balance settled |
| [[cobb\|Cobb]] | Basin logistics need a voice | Helpful young Black-Jaw; won't hide Perrin from Nona | To be useful and stay clear of trouble |
```

When an NPC's performance really matters at the table, give them a **Roleplay Prompt + Anchor** per `ttrpg-writing` rather than just the handle.

### Threads & Clocks

What moves whether or not the party acts. A clock here is *pending pressure*, not a canon write — actual world advancement is the `faction-clock` skill's job. Make each tick **observable**: the party sees the effect, never the mechanic.

```markdown
## Threads & Clocks

| Thread | Current pressure | If ignored | Visible tick |
|---|---|---|---|
| [[knighton-pursuit\|Knighton Pursuit]] | Rook is gone; Knighton is moving | Ships dispatched toward the party's route | A Crown commercial eye is absent on a schedule someone knew in advance |
| [[il-gioco-delle-beffe\|The Beffa]] | Registration opens at dawn | Festival runs without them, becomes cover for other actors | Cloth in the streets; nervous marks; daily results at sundown |
```

Good tick: "three more soldiers arrived on the morning ferry." Bad tick: "tensions are rising." If the DM can't show it at the table, it isn't a tick.

### Spotlight

Name the PC who has waited longest (from `hot.md` Spotlight Tracking) and attach them to a scene that already exists. Never manufacture a scene whose only purpose is the spotlight.

```markdown
## Spotlight

- **Delmar:** Red Lady Salvage Money already pulls on his Maw obsession — let him be the expert the broker network notices, so the offer comes *to* him.
```

### Secrets & Clues

5–10 discoverable facts, kept **unassigned** — give each to the first action that earns it, never bound to one mandatory scene or one roll. Separate DM-only truth from player-safe clue. A critical clue must have multiple discovery vectors (the Three Clue Rule: any one truth reachable three ways).

```markdown
## Secrets & Clues

- A Calveno repaint won't erase a Crown cutter's silhouette — surfaces via Savia, a dock regular, or a failed papers check.
- Nona doesn't yet know the *[[vestra\|Vestra]]* is gone — surfaces the moment Perrin or the party mentions a ship.

> [!secret]
> The sewer collector under the Mercatura has three access hatches; two were re-seated this week. Give this only if players look in the right direction — it's a raid thread, not free intel.
```

### If They Surprise You

The sandbox safety net, and the single biggest source of DM confidence. A short procedure for running a beat you didn't prep, so "they went off-menu" becomes a tool instead of a panic.

```markdown
## If They Surprise You

1. **Place the request** in the world — who locally would have this? (district, NPC type)
2. **Give one competent local** who wants one small thing now (a sale, a witness, a referral, a favour).
3. **Attach one live pressure** from the Threads table so the new direction still feeds the session.
4. **Let the choice stand.** Note what changed, tick the relevant clock, and move on. Never have a second NPC repeat the same hook until they comply.
```

### Possible Cliffhanger

Don't plan an ending — name the highest-tension state worth recognizing *if* it happens, so the DM knows a good stopping point when they see one.

```markdown
## Possible Cliffhanger

If the session ends here: [the unresolved pressure that is visible and active right now].
```

### Capture For Next Time

A tiny closing checklist — what to note after the session so prep compounds instead of resetting. Keeps the guide a living loop, not a one-shot.

```markdown
## Capture For Next Time

- Which scenes fired, which were ignored (and where their pressure moved)
- Any clock that should advance in `hot.md`
- Whose spotlight landed; who's owed next
```

---

## Module Formatting Craft

The conventions that make the guide read like a published module and run like one. Obsidian-flavoured markdown throughout; `ttrpg-writing` is the authority for prose and which callout types exist — these are the ones a run guide leans on.

**Read-aloud** — `> [!read-aloud]`. Present tense, second person, sensory, ends at a decision point. Never states player emotion, thought, or action. 2–4 sentences; every sentence past the fourth is the DM talking to themselves.

**DM-only truth inline** — `> [!secret]`. For information the DM holds back: hidden motives, what a search really finds, the truth behind a clue. Keeps GM knowledge visually separate from player-facing text on the same page.

**Skill checks** — `> [!skill-check] Ability (DC N)`, then what **success** and **failure** each reveal. Always give failure a *result*, not just "nothing happens" — a failed roll should still move play.

**Stat lines, inline** — when a scene can turn violent, give the runnable minimum so the DM doesn't flip out to a statblock:

```markdown
**Handler (×3):** AC 14 · HP 22 · +5 to hit, 1d6+3 · poison dart DC 12 Con (save or poisoned 1 min) · *Tactic:* skirmish, break line of sight, never fight to the death — they have a report to file.
→ full block: [[grung-handler\|Grung Handler]]
```

Link the full Fantasy Statblocks block (see `prep-creature`) for completeness; keep the line for speed.

**Relationship maps** — when spatial or faction connections matter, a small `mermaid` `flowchart LR` beats a paragraph. Use sparingly; only when the picture genuinely runs faster than prose.

**Wikilinks** — always aliased: `[[slug|Display Name]]`. First mention in a section links; later mentions in the same section don't. Verify the path exists before linking; if it doesn't, create the stub per doctrine rather than emitting a dead link.

---

## File Template

When writing to the wiki, save as `wiki/sessions/session-NN-run-guide.md` (match the existing `session-0N` numbering). The frontmatter hook completes missing fields and stamps `updated:` — fill what you can and write the content.

```markdown
---
title: "Session NN — Run Guide"
type: session
subtype: run-guide
campaign: shattered-sea
status: active
audience: dm
publish: false
session_number: NN
session_date: "YYYY-MM-DD"
summary: "At-table run guide for Session NN: <primary pressure>, <2–3 key scenes>, ~<duration>."
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
tags: [session-prep, run-guide]
sources: [Homebrew]
---

# Session NN — Run Guide

> Scene menu, not a script. The party picks; you react. Nothing here breaks if they wander — ignored pressure moves, it doesn't vanish. See *If They Surprise You* before you panic.

## Session Snapshot

| | |
|---|---|
| **Party is** | ... |
| **Last break** | ... |
| **Hottest pressure** | ... |
| **Table time** | ... |

## Strong Start

> [!read-aloud]
> ...

## Scene Menu

> Live situations, any order. Offer through the world, not as a quest board.

### [Scene Name]
*Pull: [PC(s)] · Register: [social/exploratory/combat/revelation]*

**What's true here:** ...
**NPC — [Name]:** [handle]. *Wants:* ... *Reveals:* ...
**If engaged:** ...
**If ignored:** ...
**Hook out:** ...

## NPC Bench

| Face | Grab them when | Table handle | Wants now |
|---|---|---|---|
| [[...]] | ... | ... | ... |

## Threads & Clocks

| Thread | Current pressure | If ignored | Visible tick |
|---|---|---|---|
| [[...]] | ... | ... | ... |

## Spotlight

- **[PC]:** [existing scene] can spotlight them because [specific connection to their hook].

## Secrets & Clues

- [Truth] — surfaces via [vector], [vector], or [vector].

## If They Surprise You

1. Place the request. 2. Give one competent local. 3. Attach one live pressure. 4. Let the choice stand and tick the clock.

## Possible Cliffhanger

If the session ends here: ...

## Capture For Next Time

- ...

## Context Read

- [[Source Page]] — what it grounded
```

If the session opens in a fixed canon sequence, rename `Scene Menu` to `Scene Order` for the fixed opening and add an `Open Menu` for everything after the crisis resolves.

---

## Quality Gate

Before finalizing:

- **Run-cold test:** could the DM run each scene with the rest of the wiki closed? Anything that fails this gets inlined or cut.
- Strong Start: one image, one pressure, no recap; read-aloud dictates no player feeling or action.
- Every scene has an *if ignored* consequence (or is a required logistics beat), and ignored pressure *moves* rather than vanishing.
- No scene depends on a prior player choice — only on established canon.
- Every clock tick is observable at the table.
- NPC count is table-manageable; each has a usable handle and a present-tense want.
- Spotlight attaches to an existing pressure.
- Critical clues have multiple discovery vectors; DM-only truth stays in `[!secret]`.
- Every campaign claim was read from the wiki this session, or is marked a proposal. Contradictions get `[!contradiction]`, not a silent pick.
- Every wikilink path was verified.
- Voice: concise, direct, devoid of mystery; encouragement delivered as "you have what you need," not pep talk.
- If written to the wiki: frontmatter filled, `hot.md` updated if state changed, committed without touching unrelated files.

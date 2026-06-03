# Session Run Guide — Spec & Template

The complete spec for building a Shattered Sea session run guide: the inline-first contract, the assembly workflow, the three-zone section specs with worked examples, the module formatting craft, the file template, and the quality gate.

A run guide is a **scannable operating document the DM runs cold at the table.** Not a script, not prose. Judge every line by one test: *does this help the DM run the next beat without opening another file?* If not, cut it or link it.

## Contents

- The Inline-First Contract
- Assembly Workflow
- Zone 1: Dashboard
  - Session Snapshot
  - Strong Start
  - Thread Strip (Threads & Clocks)
  - NPC Quick-Ref (NPC Bench)
  - Day Tracker (multi-day sessions only)
- Zone 2: Scenes
  - Scene Card Template
  - Worked Example
  - Scene Card Rules
- Zone 3: Reference
  - Secrets & Clues
  - Stall Hooks
  - Spotlight
  - If They Surprise You
  - Possible Cliffhanger
  - Capture For Next Time
  - Context Read
- Formatting Craft
- File Template
- Quality Gate

---

## The Inline-First Contract

Everything the DM needs to run a beat lives at the point they run it. Wikilinks are for depth chased between sessions, never for retrieval mid-session. Concretely, a beat is "complete" when the DM could run it with the rest of the wiki closed:

| The DM needs… | Put it inline as… | Link the… |
|---|---|---|
| To open the scene | A `> [!read-aloud]` box, ready to speak | — |
| To play the NPC | One-line handle (voice + behaviour) + their want right now + the one thing they'll reveal or do | Full NPC page for backstory |
| To resolve a roll | A `> [!skill-check]` or `> [!check]` callout: ability, DC, what success *and* failure each reveal | Rules page if the mechanic is exotic |
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

## Zone 1: Dashboard

The first screen the DM sees. Everything here is a table or a callout — no prose paragraphs.

### Session Snapshot

A four-row table the DM reads in ten seconds to know where they stand. No prose.

```markdown
## Session Snapshot

| | |
|---|---|
| **Party is** | [[la-vasca|La Vasca]] dry dock, Calveno — ship hidden, ~5 days shore leave |
| **Last break** | Session 03 ended as the *Surety* settled into the cradle |
| **Hottest pressure** | Beffe registration opens at dawn; Nona already knows Perrin is here |
| **Table time** | ~3.5 hrs; plan 5 scenes, 1 optional |
```

Do not infer where the party will go. State only what canon or the DM has established.

### Strong Start

One in-medias-res opening: present tense, second person, one concrete image, one immediate pressure, **no recap**. The party is already mid-something. End at the decision point and stop. See `prep-session/references/STRONG-START.md` for the five types and failure modes.

```markdown
## Strong Start

> [!read-aloud]
> The cradle under the *Surety* groans upward, wet timber taking the ship's weight an inch at a time. Beyond La Vasca's arch, Calveno is already moving — festival cloth piled higher than the skiffs carrying it, a bell up toward the Mercatura marking the turn of the working day. Sem is naming repairs. Cobb is naming who'll hear you're here.

Then stop and ask what matters first. Do not narrate their answer.
```

Pair the box with a one-line DM cue when the opening needs framing ("Then stop and ask…") — but the box itself never tells players what they feel or decide.

### Thread Strip (Threads & Clocks)

What's live this session — what moves whether or not the party acts. Compact: one line per thread, max 5. This is the DM's "what's in play tonight" at a glance. A clock here is *pending pressure*, not a canon write — actual world advancement is the `world-update` skill's job. Make each tick **observable**: the party sees the effect, never the mechanic.

```markdown
## Threads

| Thread | Right now | If ignored | Tick they'll see |
|---|---|---|---|
| [[nonas-favor\|Nona's Favor]] | Stone sent; wants JC in the tunnels | Nona presses via runner | The stone speaks |
| [[umberlees-message\|Pearl Summons]] | Branca waiting in the shrine | Font omen goes public | Branca hasn't moved in days |
| [[red-lady-salvage-money\|Red Lady Salvage]] | Commission 8–10 days out | Reaches the Maw first | Diving gear at the anchorage |
```

A fuller variant when you want to name the current pressure and the visible tick explicitly:

```markdown
## Threads & Clocks

| Thread | Current pressure | If ignored | Visible tick |
|---|---|---|---|
| [[knighton-pursuit\|Knighton Pursuit]] | Rook is gone; Knighton is moving | Ships dispatched toward the party's route | A Crown commercial eye is absent on a schedule someone knew in advance |
| [[il-gioco-delle-beffe\|The Beffa]] | Registration opens at dawn | Festival runs without them, becomes cover for other actors | Cloth in the streets; nervous marks; daily results at sundown |
```

Good tick: "three more soldiers arrived on the morning ferry." Bad tick: "tensions are rising." If the DM can't show it at the table, it isn't a tick.

### NPC Quick-Ref (NPC Bench)

The roster for tonight — a quick-reference table of everyone likely to matter, with a **table handle**: the one line that lets the DM play them instantly. One-line handles, cap at ~8 NPCs unless the session is festival-scale. This is the "who might appear" lookup — enough to play an NPC for 30 seconds without finding their scene card. It complements (doesn't replace) the inline NPC notes in each scene; full detail (first line, wants, reveals) lives in the scene card.

Compact 3-column form (name, grab-when, handle):

```markdown
## NPCs

| Name | Grab when | Handle |
|---|---|---|
| [[nona-black-jaw\|Nona]] | Perrin's family pressure | Feeds you first, names what you owe second |
| [[branca\|Branca]] | Delmar goes to the shrine | Bubbly cult EA; "So!" / "Does that work for you?" |
| [[savia-brentino\|Savia]] | Ship disguise comes up | Dry, unhurried; says the hard thing once |
| [[master-kyzil\|Kyzil]] | Crissdalynn, anytime | Owl Obi-Wan — relief held under discipline |
| [[cobb\|Cobb]] | Basin logistics, harbour gossip | Helpful young Black-Jaw; won't hide Perrin from Nona |
```

Four-column form when an explicit present-tense want per NPC earns its keep:

```markdown
## NPC Bench

| Face | Grab them when | Table handle | Wants now |
|---|---|---|---|
| [[nona-black-jaw\|Nona Black-Jaw]] | Perrin's family pressure lands | Feeds you first, then names what you owe — as accounting, not threat | The Tangle's favour balance settled |
| [[cobb\|Cobb]] | Basin logistics need a voice | Helpful young Black-Jaw; won't hide Perrin from Nona | To be useful and stay clear of trouble |
```

When an NPC's performance really matters at the table, give them a **Roleplay Prompt + Anchor** per `ttrpg-writing` rather than just the handle.

### Day Tracker (multi-day sessions only)

When a session might span 2–3 in-game days, show what changes overnight. One row per thread, one column per day. Replace separate day files.

```markdown
## Day Tracker

| Thread | Day 1 eve | Day 2 dawn | Day 3 dawn |
|---|---|---|---|
| Ship | Paint stripped, port quarter | Day 2 of ~5 | Plate decision due by Day 4 |
| Raid | Pre-festival | Route testing underway | La Finestra day 1; handlers timing bridges |
| Branca | In the shrine | Still there; third dawn | Font omen noticed by locals |
| Beffa | Pre-festival | La Scelta — registration | La Finestra — execution window opens |
```

> [!dm]
> This table answers "what's different if they reach Day 3?" without you opening another file. Update it as the session progresses if you like — it's a cheat sheet, not canon.

---

## Zone 2: Scenes

Self-contained scene cards (the **scene menu**): 3–5 simultaneous situations the party can pull on, offered through the world when player intent points at them — never announced as a quest board. Organized by thread, not by day or time. Each scene is self-contained per the Inline-First Contract.

### Scene Card Template

```markdown
### [Scene Name] *(Thread Name)*
*Pull: [PC(s)] · Register: [social/combat/revelation/exploratory]*
*Available: [any time / Day 2+ / when the party does X]*

![[wiki/assets/sessions/session-NN/scene-slug.webp|Full generation prompt as alt text]]

> [!read-aloud]
> [Sensory opener if the scene has a clear entry moment. Present tense, second person, 2–4 sentences.]

**What's true:** [The situation in one paragraph. What is physically here, who is present, what just happened or is about to.]

**NPC — [Name]:** [handle — voice + behaviour]. *Wants:* [present-tense want]. *Reveals:* [what they'll give up and under what pressure].

> [!skill-check] Ability (DC N)
> Success: [what it reveals or achieves]. Failure: [what it reveals or costs — never "nothing happens"].

**If engaged:** [concrete consequence — cost, gain, what changes].
**If ignored:** [where the pressure moves — ignored ≠ deleted].
**Hook out:** [what thread or scene this connects to next].
```

### Worked Examples

A revelation beat with image, secret, and a check tied to aftermath:

```markdown
### The Shrine — Pearl Summons *(Umberlee)*
*Pull: Delmar · Register: revelation*
*Available: any time Delmar approaches the shrine*

![[wiki/assets/sessions/session-05/shrine-pearl-summons.webp|Archer-style adult animated illustration, clean vector-like linework, strong ink contours, cel-shaded lighting. Scene art, 16:9 widescreen cinematic. The Waveservant Shrine — a low tide-stained stone vault off a Mercatura canal, seawater font breathing on its own, Branca sitting upright with tide-table booklet, salt-white hair pulled back hard, bright unsettling warmth in her expression. No text, no watermarks, no logos, no gore, no photorealism, no anime/chibi, no pixel art, no stock-photo aesthetic.]]

> [!read-aloud]
> The Waveservant Shrine is a low, tide-stained vault off a Mercatura canal. The font holds a hand's depth of seawater that will not lie flat — it rises and falls like something breathing under it. Branca is exactly where she sat down: upright, awake, booklet on her knee. "So," she says, bright and clipped. "You came. Good. We have an appointment."

**What's true:** Branca has waited days. The font is moving on its own. Umberlee will speak through Branca — demand the Pearl, offer Delmar's death as "mercy," then snap Branca's neck when he refuses. Branca revives. This is a fixed dramatic beat, not a negotiation.

**NPC — Branca:** bubbly cult EA — too much eye contact, checks the tide-table booklet mid-sentence as if it settles everything. *Wants:* Delmar at his appointment; no escalation. *Reveals:* Umberlee's demand — retrieve the Pearl of Souls, return it to the shrine, accept death.

> [!read-aloud]
> Branca's eyes roll white. The voice is not hers — the sea given a throat, cold and enormous and patient. "FISK. You carry what is Mine. Go down to the wreck. Bring Me the Pearl. Return it to My shrine — and I will grant you the one mercy you have earned: a swift death, and the souls you stole brought home to Me."

> [!secret]
> The party hears that Delmar carries souls Umberlee claims and that there's a Pearl to retrieve. They don't learn the five captains or Vel Orn — keep Her words to "what is Mine" and "the souls you stole."

> [!check] Insight (DC 12) — After the Revival
> Success: Branca means it completely — she experienced her own murder as a privilege. *That* is the horror.
> Failure: reads as shock; the depth doesn't register.

**If engaged:** the Pearl demand now hangs over every Maw decision. Branca leaves the shrine, appointment complete.
**If ignored:** Branca remains. Third dawn, fourth dawn. Locals notice the woman who won't leave. The font omen goes public.
**Hook out:** the Pearl is inside the Red Lady — exactly where the salvage commission is racing. Demand and money pull at the same wreck.
```

A social/gatekeeper beat with engaged/ignored economy and a hook-out routing:

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

### Scene Card Rules

- **One card per beat. Default 3–5 live scenes; max 7 total.** More than 7 = multiple sessions. Cut ruthlessly.
- **No card depends on the party having chosen another card first.** A scene may depend on established canon, never on a future player choice. If scene B only works after scene A, rewrite the prep. Note: a card's `Available` line can describe a **situation trigger** ("when JC is in the tunnels," "when anyone enters the shrine") without violating this rule — the card is available whenever the situation arises, regardless of which other cards the party engaged. A dependency means the card *cannot work* unless a prior card fired; a trigger means the card *activates* when the fiction reaches a certain state.
- **Every card has an *if ignored* consequence,** or it is a resolved/required logistics beat. Ignored ≠ deleted — the pressure *moves*, it doesn't vanish. Say where it goes.
- **Mark the genuinely cuttable scene `*(optional)*`** — and make it the most fun one, so if it's skipped the loss is felt, not the session.
- **Multi-beat scenes:** If a scene has distinct phases (arrival → confrontation → aftermath), use H4 subheaders within the card rather than separate cards. Keep them in one scene card so they're spatially together.
- **Stat lines inline when violence is possible:**

```markdown
**Handler (×3):** AC 14 · HP 22 · +5 to hit, 1d6+3 · poison dart DC 12 Con · *Tactic:* skirmish, break sightlines, never fight to the death.
→ full block: [[grung-handler|Grung Handler]]
```

---

## Zone 3: Reference

Material the DM looks up by need, not by scroll position. Lives at the bottom of the file.

### Secrets & Clues

5–10 discoverable facts, kept **unassigned** — give each to the first action that earns it, never bound to one mandatory scene or one roll. Separate DM-only truth from player-safe clue. A critical clue must have multiple discovery vectors (the Three Clue Rule: any one truth reachable three ways).

```markdown
## Secrets & Clues

- A Calveno repaint won't erase a Crown cutter's silhouette — via **Savia**, **a dock regular**, or **a failed papers check**.
- Nona doesn't yet know the *[[vestra\|Vestra]]* is gone — surfaces the moment Perrin or the party mentions a ship.
- The Mercatura sewer collector has three access hatches; two were re-seated this week, no Commission record.
- Unusual broker money is building a Maw salvage job — via **a chandler**, **Savia** (names "Zusto" once), or **canal gossip**.
```

Separate tiers if some secrets are sensitive — give only if the party looks in the right direction:

```markdown
**Raid-adjacent — use only if the party looks in the right direction:**

> [!secret]
> The Dravosi patrol schedule has a three-day gap starting Beffa Day 4. Any harbour factor can quote the dates. The question is who else already has them.
```

### Stall Hooks

Quick table for when the table can't decide. Each hook is self-contained and pulls toward a different thread. Pick one — don't throw all at once.

```markdown
## Stall Hooks

| Hook | Comes to | Pulls toward |
|---|---|---|
| The sending stone speaks: "Come back. Bring the blue one." | Perrin | Warren / the favor |
| Branca hasn't moved. Third dawn, same position. A local mentions the woman who won't leave. | Delmar (via rumor) | Pearl Summons |
| A chandler lowers his voice: "You're not the first to ask about Maw salvage this month." | Delmar / Crissdalynn | Red Lady salvage |
| A Beffa team picks a PC as their mark. Fish oil from a balcony. | Any | City engagement |
```

### Spotlight

Name the PC who has waited longest (from `hot.md` Spotlight Tracking) and attach them to a scene that already exists. Never manufacture a scene whose only purpose is the spotlight.

```markdown
## Spotlight

- **Delmar:** Red Lady Salvage Money already pulls on his Maw obsession — let him be the expert the broker network notices, so the offer comes *to* him.
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

Don't plan an ending — name the highest-tension state(s) worth recognizing *if* they happen, so the DM knows a good stopping point when they see one.

```markdown
## Possible Cliffhanger

- **Found the blackpowder:** end on the moment JC understands the scale.
- **Engaged Umberlee:** end on the breath — Branca gasping back, "I hope you understand my lady's power."
- **Broke a handler cell:** end on what the handler reveals — the raid is days out.
```

Single-state form when only one tension dominates: `If the session ends here: [the unresolved pressure that is visible and active right now].`

### Capture For Next Time

A tiny closing checklist — what to note after the session so prep compounds instead of resetting. Keeps the guide a living loop, not a one-shot.

```markdown
## Capture For Next Time

- Which scenes fired, which were ignored (and where their pressure moved)
- Any clock that should advance in `hot.md`
- Whose spotlight landed; who's owed next
- [Session-specific items: e.g., whether JC took the tunnel job, whether Delmar witnessed the Branca beat]
```

### Context Read

Pages read during prep, listed so the DM (or a future agent) can trace sourcing.

```markdown
## Context Read

- [[hot|hot.md]] — current world state, threads, clocks
- [[session-03-recap|Session 03 Recap]] — last break
- [[calveno-sandbox-run-guide|Calveno Sandbox Run Guide]] — parent island
```

---

## Formatting Craft

The conventions that make the guide read like a published module and run like one. Obsidian-flavoured markdown throughout; `ttrpg-writing` is the authority for prose and which callout types exist — these are the ones a run guide leans on.

**Read-aloud** — `> [!read-aloud]`. Present tense, second person, sensory, ends at a decision point. Never states player emotion, thought, or action. 2–4 sentences; every sentence past the fourth is the DM talking to themselves.

**DM-only truth inline** — `> [!secret]`. For information the DM holds back: hidden motives, what a search really finds, the truth behind a clue. Keeps GM knowledge visually separate from player-facing text on the same page.

**DM notes** — `> [!dm]`. Guidance on how to run the beat — timing, tone, what to hold back. Not for content the players might see.

**Skill checks** — `> [!skill-check] Ability (DC N)` or `> [!check]`: ability, DC, then what **success** and **failure** each reveal. Always give failure a *result*, not just "nothing happens" — a failed roll should still move play.

**Stat lines, inline** — when a scene can turn violent, give the runnable minimum so the DM doesn't flip out to a statblock:

```markdown
**Handler (×3):** AC 14 · HP 22 · +5 to hit, 1d6+3 · poison dart DC 12 Con (save or poisoned 1 min) · *Tactic:* skirmish, break line of sight, never fight to the death — they have a report to file.
→ full block: [[grung-handler\|Grung Handler]]
```

Link the full Fantasy Statblocks block (see `prep-creature`) for completeness; keep the line for speed.

**Relationship maps** — when spatial or faction connections matter, a small `mermaid` `flowchart LR` beats a paragraph. Use sparingly; only when the picture genuinely runs faster than prose.

**Wikilinks** — always aliased: `[[slug|Display Name]]`. First mention in a section links; later mentions in the same section don't. Verify the path exists before linking; if it doesn't, create the stub per doctrine rather than emitting a dead link.

**Images** — one image per scene card, max. Place it at the top of the card, before the read-aloud, with a blank line above and below. Scene art (the shrine at dawn, a handler in the crowd) and tactical maps (raid overview, sewer layout) both belong inline at the scene where the DM uses them. The dashboard zone has no images — it's pure text and tables for fast scanning. Load `ttrpg-visual-aids` for prompt construction, placement rules, storage paths, and embedding syntax. Load `openrouter-image-gen` to generate. If generation fails, leave a `> [!visual-aid]` callout with the full prompt.

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
summary: "At-table run guide for Session NN: <primary pressure>, <key scenes>, ~<duration>."
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

[DM cue]

## Threads

| Thread | Right now | If ignored | Tick they'll see |
|---|---|---|---|
| ... | ... | ... | ... |

## NPCs

| Name | Grab when | Handle |
|---|---|---|
| ... | ... | ... |

## Day Tracker

*(Include only if the session may span 2+ in-game days.)*

| Thread | Day 1 | Day 2 | Day 3 |
|---|---|---|---|
| ... | ... | ... | ... |

---

## Scenes

> Live situations, any order. Offer through the world, not as a quest board.

### [Scene Name] *(Thread)*
*Pull: [PC(s)] · Register: [social/exploratory/combat/revelation]*

![[wiki/assets/sessions/session-NN/scene-slug.webp|Full prompt as alt text]]

> [!read-aloud]
> ...

**What's true:** ...
**NPC — [Name]:** [handle]. *Wants:* ... *Reveals:* ...
**If engaged:** ...
**If ignored:** ...
**Hook out:** ...

---

## Secrets & Clues

- [Truth] — surfaces via [vector], [vector], or [vector].

## Stall Hooks

| Hook | Comes to | Pulls toward |
|---|---|---|
| ... | ... | ... |

## Spotlight

- **[PC]:** [existing scene] can spotlight them because [specific connection to their hook].

## If They Surprise You

1. Place the request. 2. Give one competent local. 3. Attach one live pressure. 4. Let the choice stand and tick the clock.

## Possible Cliffhanger

- ...

## Capture For Next Time

- ...

## Context Read

- [[Source Page]] — what it grounded
```

If the session opens in a fixed canon sequence, rename `Scenes` / `Scene Menu` to `Scene Order` for the fixed opening and add an `Open Menu` for everything after the crisis resolves.

---

## Quality Gate

Before finalizing:

- [ ] **One-file test:** is everything in one file? No day files, no scene files, no beat files linked for content the DM needs during play.
- [ ] **Run-cold test:** could the DM run each scene card with the rest of the wiki closed? Anything that fails gets inlined or cut.
- [ ] **Scope test:** max 7 scene cards, max 3 in-game days. If over, you're prepping multiple sessions — split into a second run guide.
- [ ] **Dashboard scannable:** snapshot, thread strip, and NPC bench all fit on one screen with no prose paragraphs.
- [ ] **Strong Start:** one image, one pressure, no recap; read-aloud dictates no player feeling or action.
- [ ] **Thread-organized:** scenes grouped by thread, not by in-game day. Thread tags in parentheses.
- [ ] **Every scene has *if ignored*** (or is a required logistics beat): ignored pressure moves, it doesn't vanish.
- [ ] **No scene depends on a prior player choice** — only on established canon.
- [ ] **Every clock tick is observable.** If the DM can't show it, it isn't a tick.
- [ ] **NPC bench is table-manageable** (3 columns: name, grab-when, handle — or 4 with wants-now); each has a usable handle and a present-tense want. Full detail lives in scene cards.
- [ ] **Images placed correctly.** Max 1 per scene card, at the top before read-aloud. No images in the dashboard zone. Generated via `ttrpg-visual-aids` + `openrouter-image-gen`, or `[!visual-aid]` fallback.
- [ ] **Spotlight attached to an existing pressure,** never manufactured.
- [ ] **Critical clues have multiple discovery vectors.**
- [ ] **DM-only truth in `[!secret]`.**
- [ ] **Every campaign claim read from the wiki this session,** or marked as proposal. Contradictions get `[!contradiction]`, not a silent pick.
- [ ] **Every wikilink path verified.**
- [ ] **Voice:** concise, direct, devoid of mystery. Encouragement = "you have what you need," not pep talk.
- [ ] **Frontmatter filled,** `hot.md` updated if state changed, **committed** without touching unrelated files.

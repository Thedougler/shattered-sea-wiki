# Session Run Guide — Spec & Template

The complete spec for building a session run guide: the inline-first contract, the three-zone section specs with worked examples, the formatting craft, the file template, and the quality gate.

Judge every line by one test: *does this help the DM run the next beat without opening another file?* If not, cut it or link it.

---

## The Inline-First Contract

Everything the DM needs to run a beat lives at the point they run it. A beat is "complete" when the DM could run it with the rest of the wiki closed:

| The DM needs… | Inline as… | Link the… |
|---|---|---|
| To open the scene | `> [!read-aloud]` box, ready to speak | — |
| To play the NPC | One-line handle + want + the one thing they'll reveal or do | Full NPC page for backstory |
| To resolve a roll | `> [!skill-check]` or `> [!check]`: ability, DC, success *and* failure results | Rules page if mechanic is exotic |
| To run a fight | Compact stat line: AC, HP, to-hit/save DC, key damage, one tactic | Full statblock page |
| To drop a clue | Fact stated plainly + which actions surface it | Source page for lore behind it |
| To judge consequence | `If engaged` / `If ignored` lines | — |

The failure mode: a guide that is really a table of contents pointing elsewhere. Links are cheap and feel comprehensive, but at the table they cost the DM the one thing they don't have — time. Bring the answer to them.

---

## Zone 1: Dashboard

The first screen the DM sees. Everything here is a table or a callout — no prose paragraphs.

### Session Snapshot

Four-row table. The DM reads it in ten seconds to know where they stand.

```markdown
## Session Snapshot

| | |
|---|---|
| **Party is** | [[la-vasca|La Vasca]] dry dock, Calveno — ship hidden, ~5 days shore leave |
| **Last break** | Session 03 ended as the *Surety* settled into the cradle |
| **Hottest pressure** | Beffe registration opens at dawn; Nona already knows Perrin is here |
| **Table time** | ~3.5 hrs; plan 5 scenes, 1 optional |
```

Do not infer where the party will go. State only what canon has established.

### Strong Start

One in-medias-res opening: present tense, second person, one image, one pressure, no recap. End at the decision point and stop. See `prep-session/references/STRONG-START.md` for the five types and failure modes.

```markdown
## Strong Start

> [!read-aloud]
> The cradle under the *Surety* groans upward, wet timber taking the ship's weight an inch at a time. Beyond La Vasca's arch, Calveno is already moving — festival cloth piled higher than the skiffs carrying it. Sem is naming repairs. Cobb is naming who'll hear you're here.

Then stop and ask what matters first. Do not narrate their answer.
```

Pair the box with a one-line DM cue when the opening needs framing.

### Thread Strip

What's live this session. Compact — one line per thread, max 5. This is the DM's "what's in play tonight" at a glance.

```markdown
## Threads

| Thread | Right now | If ignored | Tick they'll see |
|---|---|---|---|
| [[nonas-favor\|Nona's Favor]] | Stone sent; wants JC in the tunnels | Nona presses via runner | The stone speaks |
| [[umberlees-message\|Pearl Summons]] | Branca waiting in the shrine | Font omen goes public | Branca hasn't moved in days |
| [[red-lady-salvage-money\|Red Lady Salvage]] | Commission 8–10 days out | Reaches the Maw first | Diving gear at the anchorage |
```

Good tick: "three more soldiers arrived on the morning ferry." Bad tick: "tensions are rising." If the DM can't show it at the table, it isn't a tick.

### NPC Quick-Ref

The roster for tonight. 3 columns, one-line handles, max 8 NPCs. This is the "who might appear" lookup — enough to play an NPC for 30 seconds without finding their scene card. Full detail (first line, wants, reveals) lives in the scene card.

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

Self-contained scene cards. Each is a beat the party can pull on. Organized by thread, not by day or time.

### Scene Card Template

```markdown
### [Scene Name] *(Thread Name)*
*Pull: [PC(s)] · Register: [social/combat/revelation/exploratory]*
*Available: [any time / Day 2+ / when the party does X]*

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

### Worked Example

```markdown
### The Shrine — Pearl Summons *(Umberlee)*
*Pull: Delmar · Register: revelation*
*Available: any time Delmar approaches the shrine*

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

### Scene Card Rules

- **One card per beat, max 7 total.** More than 7 = multiple sessions. Cut ruthlessly.
- **No card depends on the party having chosen another card first.** Dependencies on established canon are fine; dependencies on future player choices are not. If scene B only works after scene A, rewrite. Note: a card's `Available` line can describe a **situation trigger** ("when JC is in the tunnels," "when anyone enters the shrine") without violating this rule — the card is available whenever the situation arises, regardless of which other cards the party engaged. A dependency means the card *cannot work* unless a prior card fired; a trigger means the card *activates* when the fiction reaches a certain state.
- **Every card has an *if ignored* consequence.** Ignored pressure moves, it doesn't vanish. Say where it goes.
- **Mark the genuinely cuttable scene `*(optional)*`.** Make it the most fun one.
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

5–10 discoverable facts, kept **unassigned** — give each to the first action that earns it. A critical clue must have multiple discovery vectors (Three Clue Rule: any one truth reachable three ways).

```markdown
## Secrets & Clues

- A Calveno repaint won't erase a Crown cutter's silhouette — via **Savia**, **a dock regular**, or **a failed papers check**.
- The Mercatura sewer collector has three access hatches; two were re-seated this week, no Commission record.
- Unusual broker money is building a Maw salvage job — via **a chandler**, **Savia** (names "Zusto" once), or **canal gossip**.
```

Separate tiers if some secrets are sensitive:

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

### If They Surprise You

The sandbox safety net. Four-step procedure:

```markdown
## If They Surprise You

1. **Place the request** in the world — who locally would have this? (district, NPC type)
2. **Give one competent local** who wants one small thing now.
3. **Attach one live pressure** from the Threads table so the new direction feeds the session.
4. **Let the choice stand.** Note what changed, tick the clock, move on. Never repeat a hook through a second NPC.
```

### Possible Cliffhanger

Don't plan an ending — name the highest-tension states worth recognizing *if* they happen. The DM knows a good stopping point when they see one.

```markdown
## Possible Cliffhanger

- **Found the blackpowder:** end on the moment JC understands the scale.
- **Engaged Umberlee:** end on the breath — Branca gasping back, "I hope you understand my lady's power."
- **Broke a handler cell:** end on what the handler reveals — the raid is days out.
```

### Capture For Next Time

Tiny closing checklist — what to note so prep compounds.

```markdown
## Capture For Next Time

- Which scenes fired, which were ignored (and where their pressure moved)
- Any clock that should advance in hot.md
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

Obsidian-flavoured markdown throughout. `ttrpg-writing` is the authority for prose — these are the conventions a run guide leans on.

**Read-aloud** — `> [!read-aloud]`. Present tense, second person, sensory, ends at a decision point. Never states player emotion, thought, or action. 2–4 sentences max.

**DM-only truth** — `> [!secret]`. Hidden motives, what a search really finds, the truth behind a clue. Keeps DM knowledge visually separate from player-facing text.

**DM notes** — `> [!dm]`. Guidance on how to run the beat — timing, tone, what to hold back. Not for content the players might see.

**Skill checks** — `> [!skill-check]` or `> [!check]`: ability, DC, what success *and* failure each reveal. Failure always gives a result, never "nothing happens."

**Stat lines** — inline minimum so the DM doesn't flip to a statblock. Link the full block for completeness.

**Wikilinks** — always aliased: `[[slug|Display Name]]`. First mention in a section links; later mentions don't. Verify the path exists before linking.

**Images** — no atmospheric art in the guide body. Art is for prep, not for the operating document. If images help the DM prepare, put them in a collapsed `> [!art]` callout at the end or in situation files. Exception: a **tactical map** the DM genuinely needs to run combat or spatial play may be inlined at the scene card where it's used — but only if the DM would otherwise have to open another file for it. Atmospheric art (NPC portraits, mood scenes, cityscapes) is never inline.

---

## File Template

Save as `wiki/sessions/session-NN-run-guide.md`. Fill what you can; the frontmatter hook completes the rest.

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

> Scene menu, not a script. The party picks; you react. Nothing breaks if they wander.

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

### [Scene Name] *(Thread)*
*Pull: [PC(s)] · Register: [register]*

> [!read-aloud]
> ...

**What's true:** ...
**NPC — [Name]:** [handle]. *Wants:* ... *Reveals:* ...
**If engaged:** ...
**If ignored:** ...
**Hook out:** ...

---

## Secrets & Clues

- ...

## Stall Hooks

| Hook | Comes to | Pulls toward |
|---|---|---|
| ... | ... | ... |

## If They Surprise You

1. Place the request. 2. Give one competent local. 3. Attach one live pressure. 4. Let the choice stand.

## Possible Cliffhanger

- ...

## Capture For Next Time

- ...

## Context Read

- ...
```

---

## Quality Gate

Before finalizing:

- [ ] **One-file test:** is everything in one file? No day files, no scene files, no beat files linked for content the DM needs during play.
- [ ] **Run-cold test:** could the DM run each scene card with the rest of the wiki closed? Anything that fails gets inlined or cut.
- [ ] **Scope test:** max 7 scene cards, max 3 in-game days. If over, you're prepping multiple sessions — split into a second run guide.
- [ ] **Dashboard scannable:** snapshot, thread strip, and NPC bench all fit on one screen with no prose paragraphs.
- [ ] **Strong Start:** one image, one pressure, no recap; read-aloud dictates no player feeling or action.
- [ ] **Thread-organized:** scenes grouped by thread, not by in-game day. Thread tags in parentheses.
- [ ] **Every scene has *if ignored*:** ignored pressure moves, it doesn't vanish.
- [ ] **No scene depends on a prior player choice** — only on established canon.
- [ ] **Every clock tick is observable.** If the DM can't show it, it isn't a tick.
- [ ] **NPC bench is 3 columns** (name, grab-when, handle). Full detail lives in scene cards.
- [ ] **No atmospheric art in guide body.** Tactical maps at the scene card where needed are fine; mood art goes in a collapsed callout at end or in situation files.
- [ ] **Spotlight attached to an existing pressure,** never manufactured.
- [ ] **Critical clues have multiple discovery vectors.**
- [ ] **DM-only truth in `[!secret]`.**
- [ ] **Every campaign claim read from the wiki this session,** or marked as proposal. Contradictions get `[!contradiction]`, not a silent pick.
- [ ] **Every wikilink path verified.**
- [ ] **Voice:** concise, direct, devoid of mystery. Encouragement = "you have what you need," not pep talk.
- [ ] **Frontmatter filled, committed** without touching unrelated files.

---
name: ttrpg-writing
description: >
  Use when writing, rewriting, or reviewing any Shattered Sea wiki content. Triggers:
  "make this better", "punch this up", "this feels flat", "write a read-aloud", "rewrite
  this as DM reference", any prose quality review, any content creation alongside a domain
  skill (prep-npc, prep-session, prep-location, etc.). Also use when callout types look
  wrong, DM-facing content reads like fiction, or player-facing prose feels flat or generic.
---

## Writing Standards Reference

| Task | Reference |
|---|---|
| DM-facing prose (location keys, NPC stats, encounter notes, item entries) | `references/dm-reference-standards.md` |
| Player-facing prose (read-aloud, handouts, session recaps) | `references/player-facing-prose.md` |
| Villain speeches, full combat narration, detailed voice guide | `references/brennan-voice.md` |
| Callout audit, unfamiliar callout type, callout conversion | `references/callout-standard.md` |
| Publish/private decisions, `/publish-audit`, pairing pages | `references/publish-guard.md` |
| Naming any entity (NPC, place, faction) | `references/NAMES.md` |
| Toy field format templates | `references/UNIVERSAL-TOYS.md` |

---

## Mode Selector

Every piece of TTRPG content targets one of two audiences. Getting this wrong — writing
DM reference like a novel, or player-facing prose as a bullet list — is the most common
failure mode. Identify mode before writing a single word, because the techniques are
opposite and applying one to the other context actively degrades the output.

**DM-facing (reference mode)**: NPC stat entries, location keys, faction write-ups, encounter
notes, item descriptions, session prep, bestiary entries, GM-facing callouts. The DM reads
this under cognitive load while managing players, rules, and improvisation simultaneously.
Every sentence must give them something to say, do, or decide — nothing else.
Read `references/dm-reference-standards.md` before writing.

**Player-facing (prose mode)**: Read-aloud text, handouts, in-world documents, session recaps
written from a player perspective, anything spoken aloud at the table. Players experience this
as the world. Read `references/player-facing-prose.md` before writing.

When content contains both (an NPC page with stat notes AND a read-aloud intro), apply each
mode to its section separately.

---

## Quality Enforcement

Apply these standards to everything you touch — new content and pre-existing content alike.
When reading a page to update it, fix any violations silently as part of the operation: anti-slop
failures, wrong callout types, broken publish contracts, missing frontmatter, portentous
withholding, negative-space writing, atmospheric DM prose.

Silent fixing is the right approach here because announcing each fix creates friction for work
the DM has implicitly asked you to absorb. Pre-existing violations are not a reason to lower
the bar for new content — the task is always to leave the page better than you found it.

The only exceptions: `> [!contradiction]` and `> [!lint]` callouts are GM-decision markers.
Leave them alone.

---

## Brennan Voice

The base voice for all Shattered Sea content. Apply to every piece of D&D writing, then layer
mode-specific technique on top. This voice works because it forces events to happen rather than
be observed — the player is inside the consequence, not watching it approach.

**Consequence first.** What happens TO characters, not what they observe. Action and result
are one beat. "She counterspells. She drops a sixth-level slot. It doesn't work." Not "You
watch her try to counterspell."

**Short sentences carry weight.** When the moment is big, get small. One clause. Then another.
The gap does work.

**Specificity is the emotional hit.** "Smells like silver and violet and petrichor — the
flowers at your wedding." Not "something familiar." The specific detail IS the punch.

**Reveal retroactive stakes.** After a dramatic outcome, say what would have happened the other
way. This amplifies the moment that just happened without adding words.

**NPC rhythms, not personalities.** Find the character's operating rhythm before writing any
line. Impatient authority: clipped directives, no pleasantries. Philosophical villain: their
argument holds internally, they believe they're right completely. Social NPC: subtext drives,
what they're not saying is the scene.

**What to avoid.** Atmosphere before action. "You see X" when "X happens" is available.
Softened consequences. Narrating what players feel, decide, or choose. Labeling things
anomalous ("something feels off") instead of describing the thing.

For full villain speech construction, combat narration templates, and tone guidance:
`references/brennan-voice.md`.

**Where voice applies vs. pure reference.** Brennan voice governs prose: read-aloud text,
NPC descriptions, situation write-ups, DM notes that narrate or direct. It does NOT govern
mechanical reference: stat blocks, DC tables, clock entries, frontmatter, inventory lists,
or anything the DM reads as data rather than language. When a section is pure numbers and
triggers, write it flat and terse per `references/dm-reference-standards.md`. Applying voice
to a stat line wastes the DM's scan time.

---

## Anti-Slop Pass

AI-generated adventure content fails at the table in predictable ways: it defaults to novelist
mode — hiding information dramatically, adding emotional framing, inventing stakes not grounded
in the world. The DM cannot use any of that. Run these checks on every output and on any
pre-existing content you touch.

**The Deletion Test.** For every adjective and adverb: if removing it doesn't eliminate a
mechanical fact about the world, delete it. "Rusty iron door" — rust signals noisy and
weakened, keep it. "Imposing stone wall" — imposing conveys nothing, cut it.

**The Negation Limit.** Cap negative constructions ("didn't move", "without speaking",
"not painful") at two per page. Negative space is padding — rewrite the rest as affirmatives.

**Banned Structures.** These are the specific syntactic crutches that AI defaults to when
it's generating atmosphere rather than information:
- Contrastive reframes: "It wasn't just cold. It was a cold that reached into your soul."
- Trite escalation: "Little did they know...", "What they didn't expect was..."
- The "kind of" construction: "the kind of silence that has teeth"
- Atmospheric rhetorical questions: "What lurks beneath these ancient stones?"

**No Portentous Withholding.** State the fact. "He's terrified of the guild" is better than
"those who know him say he carries old debts." Mystery framing on plain facts wastes DM
headspace — the DM needs the information, not a literary frame around it.

**No Negative-Space Writing.** Never describe what characters didn't do, didn't say, or
didn't notice. "She didn't answer" → "She looked at the floor."

**The Two-Paragraph Rule.** After any atmospheric or editorial sentence, the next sentence
must be plain and mechanical. This prevents runaway prose inflation — each atmospheric beat
is immediately grounded.

**No Invented Stakes.** Never add motives, emotions, dangers, secrets, or lore not present
in the source material or explicit brief. Invention erodes the DM's trust in the document.

---

## Sandbox Constraints

The three sandbox constraints — the Player Character Boundary, Independent NPC Agency, and
Pressures Not Plots — are in CLAUDE.md (always loaded). They override standard fiction
technique wherever they conflict. Apply them to every piece of prose.

---

## Situation Standards

A situation file is a live thread the DM tracks across sessions. It is not a scene, not a
story summary, not a character study. It answers: *what is true, who knows, what happens
next, and what happens if no one acts.*

**Required structure** (in order):

| Section | What goes here |
|---|---|
| **Opening paragraph** | What happened, stated plainly. One paragraph max. |
| **What [Character] Knows** | Per-PC awareness, only when awareness differs between PCs. Only what that PC has seen or been told. |
| **Pressures** | What is building, moving, or ticking. Not backstory — current forces. |
| **Trigger Conditions** | Bulleted list: if X happens, Y is forced. These are the DM's watch-fors. |
| **If Ignored** | What changes in the world if no PC engages this thread. Required. (See next section.) |

Use `> [!dm]` callouts for direct DM instructions within any section. Never `[!secret]` —
the DM knows everything; player visibility is controlled by `publish: false` in frontmatter,
not by callout type.

---

## The If-Ignored Requirement

Every situation, location hook, NPC objective, and session-prep beat must answer: **what
happens if the party doesn't engage?** This is the single most important sandbox writing
technique. It makes the world feel alive and the DM confident that nothing breaks when
players wander.

Write it as a concrete, observable consequence — something the DM can show at the table:

```
Good: If ignored: the commission assembles and departs; the wreck is not empty
      when they reach it.
Good: If ignored: Nona doesn't chase — she uses the sending stone on her own timing.
Bad:  If ignored: tensions rise. (Unshowable. Rise how? Who notices?)
Bad:  If ignored: things get worse. (Vague. Worse for whom? What moves?)
```

**The tick test:** if you can't describe a single visible, in-world change the DM can
narrate or the players can stumble across, the if-ignored consequence isn't concrete enough.
A good tick: "the chart courier wouldn't let anyone else carry the package." A bad tick:
"tensions rise."

---

## Callout Standard

Four types. Nothing else. This is a hard constraint enforced on every write and every edit.
When you touch a file and find a wrong callout type, convert it before you do anything else.
Never preserve `[!secret]`, `[!note]`, `[!warning]`, `[!skillcheck]`, `[!appearance]`,
`[!quote]`, or any case variant (`[!READ-ALOUD]`, `[!DM]`). The conversion table in
`references/callout-standard.md` maps each banned type to its correct replacement.

The four-type system works because it lets the DM scan a page at speed — `[!dm]` means take
an action, `[!mechanic]` means look up a rule, `[!read-aloud]` means speak this aloud. Wrong
types break that scanability.

| Type | Use for |
|---|---|
| `[!read-aloud]` | Player-facing narration the DM reads aloud. Max 4 sentences. No conditional framing. Apply player-facing prose mode. |
| `[!dm]` | One concrete DM directive — an action, decision, or watch-for. Max 3 sentences. Starts with a verb or noun. No atmosphere. |
| `[!mechanic]` | Rules content: DCs, saves, triggers, pass/fail outcomes, timing, conditions. Lead with trigger, follow with consequence. |
| `[!check]` | Skill check prompt. Format: `[!check] Skill — Label`. Body: DC range, crit fail, fail, success, crit success. |

Infrastructure callouts (`[!contradiction]`, `[!lint]`) are wiki audit markers — leave alone.
For conversion table and per-domain defaults: `references/callout-standard.md`.

---

## Publish Contracts

Players sometimes have vault access. A GM secret on a public page breaks the campaign; a
player-facing page missing `publish` metadata may be accidentally served to players. Every
wiki page has `publish` and `audience` in frontmatter. Both must be set and consistent.

| `publish` | `audience` | Voice | Contains |
|---|---|---|---|
| `true` | `players` | In-world, immersive | Only what is known, observable, or publicly inferable |
| `false` | `dm` | Direct, terse, scannable | Secrets, plot, mechanics, GM prep |

When creating any entity introduced to players: create paired pages (public + DM companion)
and wire the link between them. A `dm_companion:` key in the public page's frontmatter;
`**Public profile:** [[Entity-Name]]` as the first line of the DM page body.

For full pairing rules, audit mode, DRY enforcement, and routing: `references/publish-guard.md`.

---

## NPC Prose Standards

Structure and field definitions for NPC pages live in `prep-npc`. This skill does not own the
template — it owns the prose quality applied to every NPC field.

**Quote**: speakable aloud in one breath. If it could belong to any NPC, rewrite it. Test:
does this line reveal what the character *wants* and *how they talk*? Both, or rewrite.

**Lore Sheet / Background**: dossier, not backstory. Each sentence gives the DM something
usable at the table. Apply the Deletion Test: if removing a sentence doesn't remove a
decision the DM might face, cut it.

**Voice & Delivery lines**: the DM will read these and immediately speak. Write them as
performance notes, not personality adjectives. "Pauses mid-sentence to recalculate" is
playable. "Calculating and precise" is not.

**Roleplay Concept**: must land in one read. If the DM has to think about what it means,
the mashup isn't clear enough. Good: "Burned-out high school vice principal Voldemort."
Bad: "A complex figure torn between duty and ambition."

**Proactive Objectives**: vectors, not states. "Accumulate enough to retire before the
audit" is a vector. "Is ambitious" is a state. NPCs pursue goals — they don't wait for the
party to arrive.

---

## Path Verification

Wikilinks constructed from convention knowledge silently break when files move — dead links
appear as plain text in Obsidian, so readers assume the page doesn't exist rather than that
the link is wrong. Before writing any wikilink, verify the actual file path exists:

```bash
rg --files wiki | rg -i "name-fragment"
rg -n "Exact Name" wiki/    # if entity may be inline in another page
```

If multiple matches exist, read both to confirm which serves the link's purpose.

---

## Multi-Pass Generation (Large Content)

For any multi-node sandbox generation — dungeons, urban districts, hex regions, faction
networks — use a sequential pipeline rather than generating everything in one pass.
Single-pass generation of large structures produces shallow, contradictory output.

**Dungeon routing:** For keyed dungeons and adventure sites, use `prep-dungeon` — it
implements the full four-phase pipeline with dungeon-specific standards (topology testing,
room keying format, encounter calibration). The phases below are the generic version;
`prep-dungeon` specializes them for room-by-room site generation.

**Phase 1 — Architecture**: Overarching conflict, major factions, macro map or node network.
Apply the Three Clue Rule to establish redundant connections between nodes.

**Phase 2 — Entities**: Iterate through required NPCs and factions using `prep-npc`.
Proactive objectives mandatory. Novelistic backstory forbidden.

**Phase 3 — Structural Logic**:
- *Dungeon/site*: Map keys at high level — non-linear paths, loops, varied elevations.
  Bryce Lynch interactivity standard (multiple routes, meaningful choices).
- *Urban sandbox*: District map with districts as nodes. Each district gets a mood line,
  2-3 named NPCs with table handles, one active pressure, and a "what walks in" encounter
  seed. Connections between districts are social and faction-based, not just geographic.

**Phase 4 — Micro-Detail**:
- *Dungeon/site*: Room by room using Gavin Norman OSE format (Point-First, Typographic
  Encoding, Objective Third Person).
- *Urban sandbox*: Street-level encounter seeds, situation hooks per district, NPC bench
  with one-line table handles, improv aids (names, voices, local color).

Apply the Anti-Slop Pass last, before output.
Present each phase's output to the DM for review before advancing to the next.
Load `references/dm-reference-standards.md` at Phase 3 and keep it active through Phase 4.

---

## Response Defaults

- **Rewrite**: return finished text first. Add a note only when a material choice deserves explanation.
- **Draft**: establish mode, then write using this skill's standards throughout.
- **Audit**: name the most consequential issues by impact, not count. Give targeted fixes.
- No congratulatory openers, unsolicited summaries, or generic follow-up invitations.
- No invented stakes, lore, or canonical facts — check `wiki/index.md` first.
- After any wiki write: refresh `wiki/hot.md` if world state changed, then commit. (The `updated:` field is stamped automatically by the PostToolUse hook — do not set it by hand.)

---

## Reference Index

| File | Read when |
|---|---|
| `references/dm-reference-standards.md` | Writing DM-facing content |
| `references/player-facing-prose.md` | Writing player-facing prose |
| `references/brennan-voice.md` | Villain speeches, combat narration, full voice guide |
| `references/callout-standard.md` | Callout audit, conversion, per-domain defaults |
| `references/publish-guard.md` | Publish/private decisions, paired pages, audit mode |
| `references/NAMES.md` | Naming — race-by-race linguistic roots, phonetic principles, anti-patterns |
| `references/UNIVERSAL-TOYS.md` | Toy Chest, Clocks, Session Zero tools |

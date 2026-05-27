---
name: ttrpg-writing
description: >
  The single entry point for all TTRPG work in the Shattered Sea campaign. Invoke this
  skill for any D&D, TTRPG, GM, or worldbuilding task — even when informally phrased.
  When in doubt, invoke it; the task router inside handles routing to the right reference.

  WRITING & STYLE: DM reference material, player-facing read-aloud, NPC write-ups, session
  recaps, handouts, item descriptions, bestiary entries, faction pages. Rewrites, edits,
  "make this better", "punch this up", "this feels flat", "how do I play this NPC". Applies
  Brennan Lee Mulligan voice as the base layer with anti-slop enforcement throughout.

  ENTITY PREP: NPCs, monsters, encounters, locations, factions, ships, bastions, PC sheets,
  condition/class/rule pages, statblocks. "Prep an NPC", "make me a monster", "design this
  location", "build an encounter", "create a faction", "make a statblock".

  CAMPAIGN OPS: Session prep, run guides, strong starts, scene menus, thread review, faction
  clock advancement, spotlight targets, world tick, campaign scaffolding. "/run-guide",
  "/strong-start", "/thread-review", "/spotlight", "/faction-clock", "help me run tonight",
  "advance the world", "what happened offscreen", "between sessions".

  CITY BUILDING: Full city/settlement design. "Build me a city", "design a settlement",
  "I need a hub location", "what's in this town".

  SANDBOX GENERATION: Multi-pass pipeline for dungeons, regions, hex maps, or any multi-node
  structure built from scratch. "Build me a dungeon", "generate a region", "design this
  dungeon from scratch".

  WIKI OPS: Callout creation and auto-correction (4 types only). Publish/private split
  enforcement. "/publish-audit", wrong callout types auto-corrected without asking.

  Invoke for any D&D, TTRPG, DM, GM, worldbuilding, or sandbox generation task — including
  casual or indirect requests. If there's any doubt, invoke it.
---

## Task Router

Read the matching reference file before drafting. Multiple files may apply to a single task.

| Task | Reference |
|---|---|
| Any DM-facing prose (location keys, NPC stats, encounter notes, item entries) | `references/dm-reference-standards.md` |
| Any player-facing prose (read-aloud, handouts, session recaps) | `references/player-facing-prose.md` |
| Villain speeches, full combat narration, detailed voice guide | `references/brennan-voice.md` |
| Session structure, campaign arcs, faction timelines, "make this feel alive" | `references/narrative-devices.md` |
| Callout audit, unfamiliar callout type, callout conversion | `references/callout-standard.md` |
| Publish/private decisions, `/publish-audit`, pairing pages | `references/publish-guard.md` |
| Session prep, run guide, strong start, thread review, spotlight, faction clock | `references/co-dm.md` |
| Post-session world advancement, world tick | `references/world-tick.md` |
| City or settlement building | `references/prep-city.md` |
| Large sandbox generation (dungeon, region, hex map, district from scratch) | `references/SANDBOX-PIPELINE.md` |
| D&D entity prep — philosophy, method, universal rules | `references/PREP.md` |
| Naming any entity (NPC, place, faction) | `references/NAMES.md` |
| NPC page | `references/PREP.md` → `references/NPC.md` |
| Monster / homebrew creature | `references/PREP.md` → `references/MONSTER.md` |
| Encounter design | `references/PREP.md` → `references/ENCOUNTER.md` |
| Location page | `references/PREP.md` → `references/LOCATION.md` |
| Faction page | `references/PREP.md` → `references/FACTION.md` |
| Travel / sea events | `references/PREP.md` → `references/TRAVEL.md` |
| Condition, class, or rule reference page | `references/REFERENCE.md` |
| Campaign scaffolding (new or iteration) | `references/CAMPAIGN.md` |
| Statblock (Fantasy Statblocks plugin) | `references/STATBLOCK.md` |
| Ship content generation | `references/SHIP-GENERATE.md` + `references/SHIP-RULES.md` |

---

## Bootstrap

Before any wiki write operation, run these in parallel to orient before touching anything:

```bash
cat content/index.md
cat content/hot.md
git status
```

`content/index.md` tells you what entities already exist — check it before naming or creating anything new. `content/hot.md` carries the current session context so you're not writing into a vacuum. `git status` shows uncommitted changes that could conflict with your writes.

Read `templates/CLAUDE.md` for the template index before building any new page.

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

The Shattered Sea is a player-driven sandbox. These constraints override standard fiction
technique wherever they conflict. Fiction technique builds toward authored outcomes; sandbox
technique builds toward interesting decisions. The DM's job is to adjudicate an interactive
simulation, not read from a script.

**The Player Character Boundary.** Never write what a PC decides, chooses, intends, feels,
thinks, or wants. Write what the environment does and what NPCs do. If a sentence ends with
a player character taking action or having a feeling, rewrite it to end with the world doing
something instead.

**Independent NPC Agency.** Write NPC goals as if the party doesn't exist yet. Faction
objectives predate the party. NPC behavior follows their own wants — NPCs pursue, they
don't wait for players to arrive.

**Pressures, Not Plots.** Frame content as pressures (things that are true and building) and
possibilities (what the environment affords), never as scripted outcomes. Avoid "if the
players do X, then Y happens" chains scripted more than one step deep.

---

## Callout Standard

The four-type system works because it lets the DM scan a page at speed — `[!dm]` means take
an action, `[!mechanic]` means look up a rule, `[!read-aloud]` means speak this aloud. Wrong
types break that scanability. Auto-correct any deviation you find without asking.

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

## NPC Construction

The Alexandrian template works because it gives the DM things to do and say at the table, not
personality adjectives to interpret in real time. A quote and three physical quirks are
immediately playable. A paragraph of backstory is not. Use this for any NPC that needs to be
performed at the table.

| Field | What goes here |
|---|---|
| **Name & Identity** | Clear, distinct. One line. |
| **Quote** | One line that captures voice, cadence, and worldview. Replaces paragraphs of personality. |
| **Background** | Strictly what impacts current sandbox state. Nothing else. |
| **Roleplaying** | Three specific, physical, actionable behavioral quirks. Not adjectives — actions. |
| **Proactive Objectives** | Bulleted list of what the NPC is actively trying to accomplish. NPCs pursue; they don't wait. |

**When playability is the goal** — add a Roleplay Prompt and Anchor:

**Roleplay Prompt**: One sentence containing the specific, ironic, or dramatically loaded
thing that is true about this character right now:
- [Character] who [ironic condition]: "A harbormaster who's been waiting years to enforce this one rule"
- [Pop culture figure] + [impossible role]: "Jennifer Coolidge, air traffic controller"
- [Situation] escalating in a specific direction: "The more tools the surgeon asks for, the clearer it is he's winging it"

**Anchor**: A pop culture mashup that locks in voice and delivery. Formula: [unexpected
thing] + [pop culture character]. "Burned-out high school vice principal Voldemort."

Include when: user asks "how do I play this", "give them a voice", "make this fun", or
whenever NPC performance quality matters.

---

## Path Verification

Wikilinks constructed from convention knowledge silently break when files move — dead links
appear as plain text in Obsidian, so readers assume the page doesn't exist rather than that
the link is wrong. Before writing any wikilink, verify the actual file path exists:

```bash
rg --files content | rg -i "name-fragment"
rg -n "Exact Name" content/shattered-sea    # if entity may be inline in another page
```

If multiple matches exist, read both to confirm which serves the link's purpose.

---

## Response Defaults

- **Rewrite**: return finished text first. Add a note only when a material choice deserves explanation.
- **Draft**: establish mode, then write using this skill's standards throughout.
- **Audit**: name the most consequential issues by impact, not count. Give targeted fixes.
- No congratulatory openers, unsolicited summaries, or generic follow-up invitations.
- No invented stakes, lore, or canonical facts — check `content/index.md` first.
- After any wiki write: update `updated:` frontmatter, refresh `content/hot.md`, commit.

---

## Reference Index

| File | Read when |
|---|---|
| `references/dm-reference-standards.md` | Writing DM-facing content |
| `references/player-facing-prose.md` | Writing player-facing prose |
| `references/narrative-devices.md` | Session structure, arcs, faction timelines |
| `references/brennan-voice.md` | Villain speeches, combat narration, full voice guide |
| `references/callout-standard.md` | Callout audit, conversion, per-domain defaults |
| `references/publish-guard.md` | Publish/private decisions, paired pages, audit mode |
| `references/co-dm.md` | Session prep, run guides, strong starts, faction clocks, spotlight |
| `references/session-run-guide.md` | Run guide template and workflow (via co-dm.md) |
| `references/faction-simulation.md` | Faction clock advancement (via co-dm.md) |
| `references/world-tick.md` | Post-session world advancement ritual |
| `references/prep-city.md` | City and settlement building |
| `references/SANDBOX-PIPELINE.md` | Multi-pass large sandbox generation |
| `references/PREP.md` | Entity prep philosophy, universal rules, routing |
| `references/NAMES.md` | Naming — race-by-race linguistic roots, phonetic principles, anti-patterns |
| `references/NPC.md` | NPC page creation |
| `references/MONSTER.md` | Monster / homebrew creature |
| `references/MONSTER-EXAMPLES.md` | Worked examples — quality and format benchmark for monster/villain output |
| `references/ENCOUNTER.md` | Encounter design |
| `references/LOCATION.md` | Location page |
| `references/FACTION.md` | Faction page |
| `references/TRAVEL.md` | Travel and sea events |
| `references/CAMPAIGN.md` | Campaign scaffolding |
| `references/STATBLOCK.md` | Statblock (Fantasy Statblocks plugin) |
| `references/SHIP-GENERATE.md` | Ship content generation |
| `references/SHIP-RULES.md` | Ship mechanics and rulings |
| `references/REFERENCE.md` | Condition, class, rule reference pages |
| `references/CR-TABLES.md` | Monster CR / stat design |
| `references/STRONG-START.md` | Strong start types |
| `references/PACING.md` | Session pacing heuristics |
| `references/NAMED-ENEMIES.md` | Named antagonist stat citations |
| `references/STAT-BLOCKS.md` | Encounter enemy stat block references |
| `references/ADVENTURE-STRUCTURE.md` | Adventure structure patterns |
| `references/CAMPAIGN-TYPES.md` | Campaign type reference |
| `references/UNIVERSAL-TOYS.md` | Toy Chest, Clocks, Session Zero tools |
| `references/ISLAND-TEMPLATE.md` | Island session prep template |
| `references/5E-FIELDS.md` | 5e frontmatter field reference |
| `references/co-dm-config-template.md` | Co-DM config creation or repair |
| `references/BESTIARY.md` | Bestiary structure |
| `references/STATBLOCK-CONFIG.md` | Statblock plugin configuration |

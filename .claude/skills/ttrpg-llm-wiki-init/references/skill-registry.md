# Skill Registry — TTRPG LLM-Wiki

Read when the Missing Skill Protocol is triggered and `skill-creator` needs a build brief.
Each entry defines the skill's name, purpose, trigger conditions, critical behaviors,
and which other skills it coordinates with. This is the starting context for building
any skill in the stack.

When handing off to skill-creator, provide the full entry for the missing skill as the
opening brief, then follow the skill-creator workflow to complete it.

This registry lists the skills that actually exist under `.claude/skills/`. Keep it in
sync when skills are added, merged, or deleted.

---

## Layer 0 — Foundation & Infrastructure

### `ttrpg-llm-wiki-init`
**Purpose:** Foundation skill for all TTRPG LLM-wiki operations. Validates vault
structure, auto-corrects deviations without asking, resumes interrupted work from
`wiki/work-queue.md`, and routes to the correct downstream skill. Modes: init, resume,
full audit, fast check.
**Trigger:** Any new wiki session; "set up the wiki", "initialize", "audit the wiki",
"check the wiki", "fix the structure", "what's the wiki status", "start fresh". Runs
first, every session.
**Critical behaviors:** Runs before any other skill or content task. The health check is
fast; the routing is mandatory. Never skip. Resumes interrupted work before starting new.
**Coordinates with:** every other skill — it routes to them.

### `continuous-self-improvement`
**Purpose:** Scheduled/autonomous improvement of wiki *infrastructure* (scripts, hooks,
lint rules, skills, CLAUDE.md, settings) — not content. Runs the loop
MEASURE → IDENTIFY → FIX → ENFORCE → VERIFY → LOG, one problem per run.
**Trigger:** "improve the wiki", "optimize the wiki", "self-improve", "kaizen",
"continuous improvement", scheduled routine invocations targeting infrastructure quality.
**Critical behaviors:** Must complete all six loop steps — skipping MEASURE or VERIFY
invalidates the run. Take a `sea health` snapshot before and after. Enforce every fix
in code so it can't regress.
**Coordinates with:** `enforced-in-code`, `ttrpg-wiki-lint`, `skill-creator`

### `enforced-in-code`
**Purpose:** Fix recurring problems once, permanently, at the lowest-context layer that
can catch them. Decide whether a fix belongs in a permission, PreToolUse hook,
PostToolUse hook, lint rule, rule file, CLAUDE.md, or skill.
**Trigger:** "enforce", "automate this check", "stop doing X", "this keeps happening",
"permanent fix", "make this automatic"; any time a convention is violated repeatedly.
**Critical behaviors:** Push enforcement down the stack — the best fix is one the agent
never sees. Prefer mechanical detection (regex, file check, schema) over guidance.
**Coordinates with:** `continuous-self-improvement`, `ttrpg-wiki-lint`

### `daily-update`
**Purpose:** Safe, additive, autonomous daily wiki maintenance. Triages the wiki, then
spends its budget on whatever matters most today (ingest backlog, lint, cross-linking).
Defers all judgment calls; invents no canon.
**Trigger:** "daily update", "daily maintenance", "garden the wiki", "routine
maintenance", "catch up the wiki", "morning update", any scheduled/cron upkeep invocation.
**Critical behaviors:** Idempotent and resumable. If a phase errors, log it, commit what's
clean, and continue — never abort the whole routine for one failure.
**Coordinates with:** `ttrpg-llm-wiki-init`, `ttrpg-wiki-ingest`, `ttrpg-wiki-lint`,
`cross-linker`

---

## Layer 1 — Ingest & Session Pipeline

### `ttrpg-wiki-ingest`
**Purpose:** Orchestrate source ingestion into the wiki — canon extraction, decomposition,
and writeback, not summarization. Find pending sources with `check_ingest.py`, classify,
digest durable claims, update the smallest necessary set of files, then archive each source.
**Trigger:** "ingest", "process this into the wiki", "digest this document", "decompose
this source", "what hasn't been ingested", "what's pending", "process the inbox", any new
file in `Inbox/`.
**Critical behaviors:** Run `check_ingest.py --count` first — it prunes duplicates. Treat
raw sources as immutable. Process one source at a time to full quality, committing each
before the next. Never invent missing canon to make a source fit.
**Coordinates with:** `ttrpg-llm-wiki-init`, `ttrpg-writing`, `world-update`, all `prep-*`
skills.

### `session-ingest`
**Purpose:** Multi-pass data mining of raw session transcript CSVs in `audio/sessions/`.
Resolve speakers, consolidate fragments, separate IC/OOC/canon, extract combat data, and
propagate to the wiki. Each part file is one chunk, processed sequentially with checkpoints.
**Trigger:** "process the transcript", "mine the session", "clean the transcript", "fix
speakers", "who is Speaker 1", new `session*.csv` files in `audio/sessions/`.
**Critical behaviors:** Checkpoint after every part so work survives context limits. Never
guess speaker attribution — flag it. Never invent words for unintelligible audio.
**Coordinates with:** `session-recap`, `world-update`, `pc-combat-primer`

### `session-recap`
**Purpose:** Post-session cascade — take session notes and propagate updates across the
wiki: recap file, `hot.md` updates, situation file updates, faction clock review, party
block update, spotlight tracking refresh. Ensures nothing drifts after a session.
**Trigger:** "session recap", "process session notes", "update the wiki after session",
"what changed this session", "post-session update", "cascade session".
**Critical behaviors:** Coordinated update across every file tracking current world state.
Read current state (hot.md, last recap, active situations) before writing. Defers canon
clock writes to `world-update`.
**Coordinates with:** `session-ingest`, `world-update`, `sandbox-narrative`

---

## Layer 2 — World Intelligence

### `world-update`
**Purpose:** Advance the living world — the canon owner of faction-clock writes. Two modes:
POST-SESSION full tick (triage all threads hot/warm/cold, roll d20 each, weave PC arcs,
write all changes) and ON-DEMAND/MID-SESSION clock advance (advance specific clocks without
the full ritual).
**Trigger:** "world update", "post-session update", "tick the world", "advance the world";
also "advance the factions", "advance the clocks", "what do the factions do", "what is
[faction] doing right now", "between sessions", "faction clock", "world tick".
**Critical behaviors:** Never advances a clock without citing the situation that justifies
it. Never fires a triggered (filled) clock without flagging it to the DM first. Core
question both modes: if the party had done nothing, what would have changed anyway?
**Coordinates with:** `sandbox-narrative`, `prep-situation`, `prep-faction`,
`session-recap`

### `pc-combat-primer`
**Purpose:** Produce agent-optimized combat intelligence — per-PC combat profiles
(theoretical maximums, observed performance, defensive thresholds, session log) compiled
into a single party combat profile that `prep-encounter` reads.
**Trigger:** "update combat primers", "update [PC] primer after session", "how hard should
this fight be", "recalibrate encounter difficulty", "what can [PC] actually do in combat",
"build combat profile for [PC]"; level-up events; new combat data ingested.
**Critical behaviors:** Empirical over theoretical — real dice, real damage, real tactics
from this table. Read the PC sheet and `combat-analytics.md` before any primer work.
**Coordinates with:** `prep-encounter`, `session-ingest`

---

## Layer 3 — Content Creation (`prep-*`)

> All `prep-*` skills share stub-check, interview + PC-connection requirement, combat
> calibration, prose pass, and filing conventions via
> `../ttrpg-llm-wiki-init/references/prep-family-standards.md`.

### `prep-npc`
**Purpose:** Create or expand a named NPC wiki page. Generate frontmatter, toy fields, lore
sheet, read-aloud appearance, voice notes, connections, and a DM companion page.
**Trigger:** "prep an NPC", "create a page for [NPC]", "flesh out [NPC]", "I need an NPC
who...", any NPC that will appear at the table. Also villain NPCs needing stat blocks.
**Critical behaviors:** Check `index.md` for an existing stub first. Every NPC must connect
to a specific PC's backstory, goal, or fear. Create the DM companion alongside the page.
**Coordinates with:** `ttrpg-writing`, `prep-creature`, `ttrpg-visual-aids`

### `prep-location`
**Purpose:** Create or expand a location wiki page (region, island, settlement, building,
dungeon, plane). Generate frontmatter, toy fields, read-aloud opening, lore, notable
sub-locations, inhabitants.
**Trigger:** "create a page for [place]", "detail [location]", "what does [place] look
like", "flesh out [settlement/building/dungeon/island]", "design this location".
**Critical behaviors:** Route multi-room explorable dungeons to `prep-dungeon`. Name the
connecting PC thread before generating.
**Coordinates with:** `prep-dungeon`, `prep-island`, `ttrpg-writing`

### `prep-faction`
**Purpose:** Create or expand a faction wiki page. Generate frontmatter, agenda, membership
structure, methods, public vs private face, clock, and relationships. Determine whether the
faction warrants a clock in `hot.md`.
**Trigger:** "create a page for [faction]", "detail [faction]", "who runs [organization]",
"what does [group] want", "add a faction clock", "flesh out [organization]".
**Critical behaviors:** Check `index.md` for an existing stub first. Agenda is a vector, not
a state. If the faction advances independently of the party, add a clock in `hot.md`.
**Coordinates with:** `world-update`, `ttrpg-writing`

### `prep-situation`
**Purpose:** Create or expand a situation file. Generate frontmatter with `lifecycle` and
`narrative_island` fields, clock definition, trigger conditions, involved entities, possible
outcomes, Three Clue placement (when applicable), and DM notes.
**Trigger:** "create a situation for [conflict]", "track [event] with a clock", "this needs
a lifecycle", "file this as a situation", any world pressure with a timeline or trigger.
**Critical behaviors:** Place in `active/` or `dormant/` per lifecycle. If the situation has
a hidden conclusion, the Three Clue Rule applies.
**Coordinates with:** `world-update`, `sandbox-narrative`, `prep-island`

### `prep-island`
**Purpose:** Create or expand a narrative island — a self-contained, portable cluster of
situations, NPCs, and locations around a coherent premise. A plot device, not a geographic
landmass. Files under `wiki/narrative-islands/` with `type: narrative-island`.
**Trigger:** "create a narrative island", "prep [location] as a sandbox node", "create a
portable scenario around [entity]", "design an island I can drop anywhere".
**Critical behaviors:** Islands contain situations — never the reverse. A single condition
with one clock is a situation (use `prep-situation`); a real landmass is a place (use
`prep-location`). Always loads `sandbox-narrative` for anti-railroading review.
**Coordinates with:** `prep-situation`, `prep-location`, `prep-npc`, `sandbox-narrative`

### `prep-ship`
**Purpose:** Create or expand a ship or vehicle wiki page at the correct detail tier (0:
embed in situation; 1: single file; 2: file + DM companion; 3: full subfolder suite). Also
handles travel encounters and sea events.
**Trigger:** "create the [ship name] wiki entry", "detail [ship]", "flesh out [vessel]",
"crew manifest for [ship]", "naval encounter with [vessel]", "design a ship".
**Critical behaviors:** Determine tier before generating; confirm Tier 2+ with the DM.
Include only history that affects current sandbox state.
**Coordinates with:** `prep-location`, `prep-encounter`, `ttrpg-writing`

### `prep-encounter`
**Purpose:** Design any encounter — combat, social, skill challenge, or hybrid. Read the
party combat primer and combat analytics, then calibrate enemy count, CR, terrain, and
mechanics to this party's empirical patterns.
**Trigger:** "design an encounter", "I need a fight", "build an encounter with [enemy]",
"how many [monsters] should I use", "balance this fight", "social encounter with [NPC]",
"skill challenge for [obstacle]". Also invoked by `prep-dungeon` and `prep-session`.
**Critical behaviors:** The party primer's **Avoid** section is binding — redesign if an
encounter would violate it. Calibrate to empirical patterns, not theoretical class features.
**Coordinates with:** `pc-combat-primer`, `prep-dungeon`, `prep-session`,
`sandbox-narrative`

### `prep-creature`
**Purpose:** Create or expand a creature or monster entry. Distinguish creature-type lore
(`wiki/lore/creatures/`) from a named creature entity (`wiki/entities/`). Includes statblock
integration for named villains.
**Trigger:** "create stats for [creature]", "I need a [monster] for the encounter", "make a
homebrew monster", "statblock for [enemy]", "bestiary entry for [creature]".
**Critical behaviors:** Read `party-combat-primer.md` before any stat calibration; Avoid
flags apply to creature design. Name the connecting PC thread.
**Coordinates with:** `prep-encounter`, `prep-npc`, `ttrpg-writing`

### `prep-dungeon`
**Purpose:** Design a dungeon, lair, ruin, or adventure site using the four-phase pipeline
(architecture → entities → spatial logic → micro-detail) with DM review between phases.
Files to `wiki/entities/places/dungeons/`.
**Trigger:** "design a dungeon", "prep an adventure site", "build a lair for [creature]",
"create a ruin", "key this dungeon", any multi-room site explored room-by-room.
**Critical behaviors:** Enforce the phase gates with DM review. Read `hot.md` and the party
combat primer (Avoid flags binding) first. Three Clue Rule when a hidden conclusion exists.
**Coordinates with:** `prep-encounter`, `prep-npc`, `prep-location`, `ttrpg-writing`,
`sandbox-narrative`

### `prep-hb-item`
**Purpose:** Design a homebrewed D&D 5e item. Enforce the one-thing constraint,
rarity-before-mechanics power budget, attunement rules, no class-feature mechanics, RAW
benchmark citation, and a DM review gate before any wiki commit.
**Trigger:** "homebrew an item for [PC]", "design a [item concept]", "make a custom [item]",
"create a magic item for [PC]". Not for RAW items that already exist.
**Critical behaviors:** Check `index.md` for existing item stubs first; a reskinned RAW item
beats homebrew. Set rarity before designing mechanics. Name the connecting PC.
**Coordinates with:** `prep-npc`, `prep-location`, `ttrpg-writing`, `ttrpg-visual-aids`

### `prep-session`
**Purpose:** Build the at-the-table operating document for one session — a scannable run
guide the DM runs cold, written like a published adventure module. Modes: `/run-guide`,
`/strong-start`, `/thread-review`, `/spotlight`.
**Trigger:** "prep for next session", "give me a session plan", "what do I run Saturday",
"help me run tonight", "build a run guide"; "/run-guide", "/strong-start", "/thread-review",
"/spotlight".
**Critical behaviors:** One file, one session. Max 5–7 scene cards, organized by thread not
by day. Inline what the DM needs to run each beat; link only for depth. Always spotlight the
PC who has been waiting. Present a scene menu, never a plot. Pending faction pressure shown
in a guide is non-canon — canon clock writes belong to `world-update`.
**Coordinates with:** `ttrpg-visual-aids`, `openrouter-image-gen`, `ttrpg-writing`,
`sandbox-narrative`, `prep-encounter`, `world-update`

---

## Layer 4 — Writing, Voice & Visuals

### `ttrpg-writing`
**Purpose:** Write, rewrite, or review any wiki content to the campaign's prose standards.
Two modes — DM-facing reference (dense, every sentence actionable) and player-facing prose
(evocative, experiential). Owns callout audits and publish/private decisions.
**Trigger:** "make this better", "punch this up", "this feels flat", "write a read-aloud",
"rewrite this as DM reference"; any content creation alongside a domain skill.
**Critical behaviors:** Identify audience mode before writing a word — applying one mode's
techniques to the other context degrades output. Consult the reference table for the task.
**Coordinates with:** all `prep-*` skills, `session-recap`, `ttrpg-visual-aids`

### `sandbox-narrative`
**Purpose:** Apply sandbox narrative principles — place loaded guns, let players decide when
they fire. Universal toy properties, Three Hooks Rule, anti-railroading check for any prep
review.
**Trigger:** Any session prep, arc, or situation design; "make this feel more sandbox", "is
this railroading?", strong-start review, faction clock design.
**Critical behaviors:** Before applying any device, ask: does this require a specific player
choice to pay off? If yes, it's a railroad — restructure so multiple paths lead to valid
outcomes.
**Coordinates with:** `prep-session`, `prep-island`, `prep-situation`, `world-update`

### `ttrpg-visual-aids`
**Purpose:** Generate, place, and embed visual aids — portraits, banners, scene and combat
art. Builds prompts from `wiki/system/art-style.md` and character pages, and defines storage
paths and embed syntax.
**Trigger:** "generate art for", "create a visual", "make a scene image", "add a portrait",
"illustrate this", "banner for", "combat art"; any prep or recap needing illustrations.
**Critical behaviors:** Read `art-style.md` before every generation and apply its directives
— no approximating. Pull character descriptions verbatim from wiki pages; never invent.
**Coordinates with:** `openrouter-image-gen`, `prep-session`, `prep-npc`, `ttrpg-writing`

### `openrouter-image-gen`
**Purpose:** Generate images from text prompts via OpenRouter's chat completions API (image
modality) using a bundled stdlib Python script. The low-level image generator that
`ttrpg-visual-aids` calls.
**Trigger:** "generate an image", "create a picture", "make art of", "draw", "illustrate",
any task requiring AI image generation.
**Critical behaviors:** Requires `OPENROUTER_API_KEY` in `.env`. Run the bundled
`generate-image.py`; it prints the saved image's absolute path to stdout.
**Coordinates with:** `ttrpg-visual-aids`

---

## Layer 5 — Maintenance, Search & Linking

### `ttrpg-wiki-lint`
**Purpose:** Lint the wiki and fix what's safe to fix. Auto-fixes file-local frontmatter;
reports (never silently changes) broken wikilinks, orphans, deadends, off-convention
filenames, stale stubs, tag variants, singleton properties, and lore/temporal consistency
issues.
**Trigger:** "lint the wiki", "check wiki health", "fix the frontmatter", "find broken
links", "find orphans", "find deadends", "lore consistency", "tag hygiene", "timeline
issues".
**Critical behaviors:** The `sea lint` CLI (`packages/cli/`) does the heavy lifting.
`--fix` is idempotent and never invents canon. `sea health` captures snapshots for
trend tracking.
**Coordinates with:** `cross-linker`, `tag-taxonomy`, `daily-update`

### `cross-linker`
**Purpose:** Add missing `[[wikilinks]]` between pages that reference each other but aren't
linked. Orphans (no inbound links) and deadends (no outbound links) are the primary targets.
**Trigger:** "link my pages", "find missing links", "cross-reference", "connect my wiki",
"weave this into the graph"; orphan/deadend reports from wiki-lint; after any ingest or
writing run.
**Critical behaviors:** Target a batch of 15–25 per run (orphans over deadends, entity pages
first). Always alias links, first mention per section, bidirectional for durable
relationships. Use `index.md` as the lookup catalog.
**Coordinates with:** `ttrpg-wiki-lint`, `ttrpg-wiki-query`, `daily-update`

### `tag-taxonomy`
**Purpose:** Enforce consistent tagging across the vault using a controlled vocabulary.
Normalizes tags to the canonical list, maps aliases, and applies tag rules.
**Trigger:** "fix my tags", "normalize tags", "clean up tags", "tag audit", "what tags
should I use", "tag taxonomy"; also whenever creating/updating a page that needs tags.
**Critical behaviors:** Always read `wiki/system/taxonomy.md` before tagging — it is the
source of truth. Respect reserved `visibility/` system tags. Max 5 tags per page.
**Coordinates with:** `ttrpg-wiki-lint`, all `prep-*` skills

### `ttrpg-wiki-query`
**Purpose:** The mandatory default method for finding anything in the wiki. Tiered search
(in-context index/hot → frontmatter → qmd semantic search) used before asserting,
inventing, or assuming any campaign fact.
**Trigger:** "look up", "what do we know about", "is there a page for", "find the entry
for", "search the wiki", "what's the current state of", "who is", "where is", "what happened
with"; and silently whenever you would otherwise guess a campaign detail.
**Critical behaviors:** Never assert an in-world fact not found in a wiki page. Gather
*complete* context, not the first hit — entities link to factions, situations, locations,
sessions. Every other Shattered Sea skill defers to this one for lookups.
**Coordinates with:** every skill that needs in-world facts.

---

## Layer 6 — Live Play & Tooling

### `live-co-dm`
**Purpose:** Real-time co-DM mid-session — fast, concise improv help — plus the home of the
DM's voice-transcription tools (voice profiling teleprompter, continuous overlap-aware
transcription).
**Trigger:** "co-DM the session", "live DM help", "I'm running right now", "mid-session",
"the players just...", "what happens next", "/live-dm", "/co-dm"; also "save a voice
profile", "set up a character voice", "start transcribing the session", "finalize the
transcript".
**Critical behaviors:** In live mode, deliberately skip wiki startup, init, lint, index
regen, and routine maintenance — read only the latest transcript plus minimal world state,
reply FAST and CONCISE, then wait. Grounding/agency non-negotiables shared with
`prep-session`.
**Coordinates with:** `prep-session`, `session-ingest`

### `roll-dice`
**Purpose:** Produce real random outcomes for any dice roll via the bundled `roll.sh`
script, which uses the system RNG. The agent cannot generate randomness.
**Trigger:** "roll", "check", "save", "attack", "damage", "d20", "advantage",
"disadvantage", any NdX notation; also whenever about to pick or invent a random number.
**Critical behaviors:** Never invent a roll — always call `roll.sh`. The result is canon.
Supports advantage/disadvantage and modifiers.
**Coordinates with:** `live-co-dm`, `prep-encounter`

### `skill-creator`
**Purpose:** Create new skills, modify and improve existing ones, and measure skill
performance — drafting, eval-running, benchmarking with variance analysis, and description
optimization for better triggering.
**Trigger:** "create a skill", "make a skill for X", "edit/optimize this skill", "run evals
on a skill", "benchmark skill performance", "improve a skill's description".
**Critical behaviors:** Figure out where the user is in the create→test→eval→iterate loop
and jump in there. Match jargon to the user's familiarity level. Use the bundled
description-improver script to optimize triggering.
**Coordinates with:** this registry (Missing Skill Protocol build briefs), `enforced-in-code`

---

## Layer 7 — Obsidian & App Development

### `obsidian-markdown`
**Purpose:** Write correct Obsidian Flavored Markdown — wikilinks, embeds, callouts,
properties, tags, highlights, math, canvas syntax. The syntax reference for any wiki page.
**Trigger:** "obsidian syntax", "wikilink", "callout", "embed", "obsidian markdown",
"obsidian formatting"; reference when creating or editing any wiki page.
**Critical behaviors:** Getting syntax wrong causes broken links, invisible callouts, or
malformed frontmatter. Match exact filenames; use aliased links.
**Coordinates with:** all content-writing skills.

### `obsidian-bases`
**Purpose:** Create and edit Obsidian Bases (`.base` files) — the native database layer for
dynamic tables, card/list views, filters, formulas, and summaries over vault notes.
**Trigger:** "create a base", "obsidian bases", "base view", "filter notes", "formula",
"database view", "dynamic table", "dashboard base".
**Critical behaviors:** `.base` files are valid YAML with roots `filters`, `formulas`,
`properties`, `summaries`, `views`. Requires Obsidian v1.9.10+.
**Coordinates with:** `obsidian-markdown`, `obsidian-cli`

### `obsidian-json-canvas`
**Purpose:** Create and edit Obsidian JSON Canvas files (`.canvas`) — nodes, edges, groups,
and connections per the JSON Canvas 1.0 spec. For spatial/visual node-and-edge layouts.
**Trigger:** "create a canvas", "edit a .canvas file", "make a mind map", "build a
flowchart", "node graph", "relationship map as a canvas", "obsidian canvas".
**Critical behaviors:** Generate unique 16-char hex IDs; validate that every edge's
`fromNode`/`toNode` resolves to an existing node. For prose notes use `obsidian-markdown`.
**Coordinates with:** `obsidian-markdown`

### `obsidian-cli`
**Purpose:** Interact with a running Obsidian vault from the command line (read, create,
search, manage notes/tasks/properties) and develop/debug plugins and themes (reload, run JS,
capture errors, screenshot, inspect the DOM).
**Trigger:** "obsidian cli", "open this note in Obsidian", "run obsidian command", "search
my vault", "set a property on", "reload my plugin", "run js in obsidian", "obsidian
screenshot", "debug my obsidian plugin/theme".
**Critical behaviors:** Requires Obsidian to be open. `obsidian help` is always the
up-to-date command reference. Use for the live app, not just editing `.md` files on disk.
**Coordinates with:** `obsidian-bases`, `obsidian-markdown`

### `player-view-dev`
**Purpose:** Launch and manage the player-view NiceGUI app for development — venv setup,
dependency install, dev server launch (localhost:8080), and test execution for the
`player-view/` subproject.
**Trigger:** "start the app", "run player-view", "dev server", "run the overlay", "test
player-view", "set up the app". (`disable-model-invocation` — explicit invocation only.)
**Critical behaviors:** Requires Python 3.11+, Apple Silicon (MLX), and `HF_TOKEN` in
repo-root `.env`. Key routes: `/dm`, `/save-speaker`.
**Coordinates with:** `tdd`

### `tdd`
**Purpose:** Test-driven development with the red-green-refactor loop for the player-view app
and `.claude/scripts`. Vertical slices via tracer bullets — one test → one implementation →
repeat.
**Trigger:** "use TDD", "test-first", "write the test first", "red-green-refactor", "write a
failing test", "TDD this", "add tests before the code", "I want integration tests for".
**Critical behaviors:** Never write all tests first then all code (horizontal slicing
produces crap tests). Test behavior through public interfaces, not implementation details.
**Coordinates with:** `player-view-dev`, `continuous-self-improvement`

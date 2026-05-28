# Skill Registry — TTRPG LLM-Wiki

Read when the Missing Skill Protocol is triggered and `skill-creator` needs a build brief.
Each entry defines the skill's name, purpose, trigger conditions, critical behaviors,
and which other skills it coordinates with. This is the starting context for building
any skill in the stack. The entries are ordered by the recommended build priority.

When handing off to skill-creator, provide the full entry for the missing skill as the
opening brief, then follow the skill-creator workflow to complete it.

---

## Layer 0 — Infrastructure

### `wiki-categorize`
**Purpose:** Apply the content categorization decision tree to any piece of novel content.
Given a file, description, or block of text: determine type, subtype, correct folder path,
required frontmatter defaults, whether to decompose into multiple files, and whether a
DM companion file or player-facing stub is needed.
**Trigger:** New content arrives in Inbox/; a file needs to be filed; agent is unsure where
content belongs; misplaced files found during audit; any time content categorization is needed.
**Critical behaviors:** Path is authoritative. Always apply the decision tree explicitly
before choosing a folder. When in doubt, place in Inbox/ with a note rather than guessing.
**Coordinates with:** `ttrpg-llm-wiki-init` (full audit), `prep-*` skills (after creation)

---

## Layer 1 — Session Pipeline

### `transcript-clean`
**Purpose:** Stage 1 and 2 of the transcript pipeline. Detect the transcript format
(Format A: no timestamps; Format B: with timestamps; detect unknowns). Consolidate
fragments from the same speaker. Normalize speaker names against the canonical speaker map.
Apply the inline tagging system: `[OOC]` `[IC]` `[TABLE]` `[RULING]` `[ROLL]` `[LORE]`
`[CANON]` `[UNCLEAR-SPEAKER]`. Segment into scenes. Generate the flags file for DM review.
**Trigger:** "clean the transcript", "process session audio", any raw transcript file
arriving in `.raw/sessions/`. Also triggered automatically after a new `.raw` file is detected.
**Critical behaviors:** Never edits the raw file — all work goes to `-clean.md` sibling.
Never guesses attribution — creates a flag entry instead. Never invents words for
unintelligible audio. Flag file is generated in parallel with the clean file, not after.
**Coordinates with:** None — runs standalone before any other session skill.

### `transcript-ingest`
**Purpose:** Stage 4 of the transcript pipeline. Read a fully reviewed, flag-resolved
clean transcript and propagate its content to the wiki. Extract `[CANON]`, `[LORE]`,
`[RULING]` blocks, NPC appearances, new entities, player decisions with forward consequences.
Update all affected entity files. Advance faction clocks. Update `hot.md` fully. Write
compiled session note. Mark session recap for generation. Log everything.
**Trigger:** DM marks flags file `review_status: complete`; "ingest this session."
**Critical behaviors:** Never runs from a raw or partially-reviewed transcript. Never runs
if `flags_resolved < flags_total` in the flags file. Generates "System File Updates Needed"
section for DM review — does not apply updates directly. Creates stubs for every new
entity before updating any existing file. Flags lore contradictions to `discrepancy-log.md`
immediately — never resolves them unilaterally.
**Coordinates with:** `wiki-categorize`, `faction-clock`, `player-interest-tracker`,
`combat-data-extract`, `session-summary-write`, `ingest-registry-update`

### `session-flags-review`
**Purpose:** Help the DM resolve ambiguous entries in a session flags file. Apply speaker
attribution heuristics (continuation, response, named address, table chatter). Suggest
IC/OOC classifications with explicit reasoning. Present one flag at a time. Wait for DM
confirmation before moving to the next.
**Trigger:** "help me review the flags", "let's go through the session flags", "who said this?"
**Critical behaviors:** Never auto-resolves flags — always presents and waits.
One flag at a time. DM has final say on every entry.
**Coordinates with:** `transcript-clean` (to understand flag format)

---

## Layer 1.5 — General Source Ingestion

### `ttrpg-wiki-ingest`
**Purpose:** Orchestrate source ingestion into the Shattered Sea wiki. Scan `.raw/`, `Inbox/`,
and optional top-level source documents for unprocessed files; classify each source; digest
and decompose durable claims; update the correct wiki files; maintain links, index, hot file,
log, and `wiki/ingest-registry.md`.
**Trigger:** "ingest this", "digest this document", "process this into the wiki",
"what hasn't been ingested?", "what's pending?", any new source file in `.raw/` or `Inbox/`,
or any source that must be decomposed into multiple wiki pages.
**Critical behaviors:** Treat raw sources as immutable. Do not summarize when decomposition is
needed. Do not ingest more than five pending files automatically; report the queue and ask
which source to process. Preserve the narrower `transcript-ingest` and
`ingest-registry-update` guidance by loading the reference files bundled inside this skill.
Never invent missing canon to make a source fit.
**Coordinates with:** `ttrpg-llm-wiki-init`, `ttrpg-writing`, `wiki-categorize`,
`transcript-ingest`, `ingest-registry-update`, `faction-clock`, `hot-update`, all `prep-*`
skills.

---

## Layer 2 — World Intelligence

### `faction-clock`
**Purpose:** Simulate what factions do between sessions. Read `hot.md` faction clocks and
active situation files. Determine what each faction does given what the party did (or
didn't do). Advance clocks accordingly. Identify triggered events. Produce "world while
the party rested" update. Update `hot.md`. Log all advances.
**Trigger:** "advance the factions", "what do the factions do", "update the clocks."
Automatically after `transcript-ingest` completes.
**Critical behaviors:** Never advances a clock without citing the situation file that
justifies the advance. Never fires a triggered event without flagging it to the DM first.
Core question: if the party had done nothing this session, what would have changed anyway?
**Coordinates with:** `sandbox-narrative`, `world-simulator`, `hot-update`

### `world-simulator`
**Purpose:** Simulate NPC and faction behavior off-screen. Given a time span and the
party's current location and activities, generate what specific NPCs are doing, what they
know, what decisions they've made. Answer "what is [NPC] doing right now?" or "what has
[faction] figured out about the party?"
**Trigger:** "what is [NPC] doing right now?", "what happens while the party rests?",
"simulate the world for two weeks."
**Critical behaviors:** Output feeds situation files and `hot.md` — always write results
somewhere, don't just answer in chat. Never simulate events that contradict established
canon without flagging the contradiction.
**Coordinates with:** `faction-clock`, `sandbox-narrative`

### `player-interest-tracker`
**Purpose:** Extract player engagement signals from session summaries and transcripts.
Categorize by weight (high: repeated questions, player-initiated investigation;
medium: in-character emotional response; low: passive engagement). Update
`wiki/dm/player-interests.md` content priority queue. Surface what to develop next.
**Trigger:** After every session ingestion. "Update player interests", "what are the
players interested in?", "what should I develop next?"
**Critical behaviors:** Distinguishes player engagement (what the player cares about)
from character motivation (what the PC wants). Both matter but differently.
**Coordinates with:** `transcript-ingest`, `prep-session`

### `combat-data-extract`
**Purpose:** Extract empirical combat data from clean session transcripts. Identify roll
results, HP thresholds, ability uses, positioning patterns, and player tendencies. Update
`wiki/dm/combat-analytics.md` with observed patterns — not theoretical class features.
**Trigger:** After each session ingestion. "Analyze the party's combat", "update combat
analytics."
**Critical behaviors:** Empirical only — what this player actually does at this table,
not what their class theoretically enables. Marks new patterns as `[unconfirmed]` until
seen across 2+ sessions.
**Coordinates with:** `transcript-ingest`, `prep-encounter`

### `hot-update`
**Purpose:** Perform a focused, targeted update to `wiki/hot.md` after a specific world
event — faction clock advance, situation resolution, session recap, or DM-declared change.
Read the event, identify which sections are affected, rewrite only those sections.
**Trigger:** A specific world event needs to be reflected in `hot.md` without running a
full session ingestion. Faction clock advanced manually. Situation resolved mid-session.
**Critical behaviors:** Surgical — only rewrite sections that are affected. Always update
the `updated` date. Always log the change.
**Coordinates with:** `faction-clock`, `transcript-ingest`

### `ingest-registry-update`
**Purpose:** Keep `wiki/ingest-registry.md` current. Add new files from `.raw/` with
`status: pending`. Update status, date, and wiki outputs list after any ingestion
operation. Generate Pending Queue section ordered by priority (sessions first).
**Trigger:** Automatically after any ingestion operation. "Update the ingest registry",
"what's pending?", "what hasn't been processed?"
**Coordinates with:** `transcript-ingest`, `ttrpg-llm-wiki-init`

---

## Layer 3 — Content Creation

### `prep-npc`
**Purpose:** Create or expand a named NPC wiki page. Generate frontmatter, summary,
wants/fears/knowledge, relationship links, voice/speech pattern, hooks. Create a DM
companion file. Ground the NPC in existing wiki entities before inventing anything.
**Trigger:** Creating any new NPC; expanding a stub NPC page; "flesh out [NPC]";
"I need a page for [NPC]."
**Critical behaviors:** Always check if a stub already exists before creating. Always
create the DM companion file alongside the player-facing file. Run lore-grounding check
before writing — no invented facts that contradict existing wiki content.
**Coordinates with:** `wiki-categorize`

### `prep-location`
**Purpose:** Create or expand a location wiki page. Generate frontmatter, summary,
sensory description, key features, contained NPCs and factions, entry points, situation
hooks. Ground the location in the existing world before inventing.
**Trigger:** Creating any new location; expanding a location stub; "detail [place]";
"what does [location] look like?"
**Coordinates with:** `prep-island`, `wiki-categorize`

### `prep-faction`
**Purpose:** Create or expand a faction wiki page. Generate frontmatter, summary,
membership structure, agenda, clocks, relationships to other factions, public vs private
face. Determine whether the faction warrants a clock in `hot.md`.
**Trigger:** Creating any new faction; expanding a faction stub; "detail [faction]";
"who runs [organization]?"
**Coordinates with:** `faction-clock`, `wiki-categorize`

### `prep-situation`
**Purpose:** Create or expand a situation file. Generate frontmatter with `lifecycle` and
`island` fields, clock definition, trigger conditions, involved entities, possible outcomes,
and DM notes. Place correctly in `active/` or `dormant/` based on whether the clock is
currently running.
**Trigger:** Creating any new situation; tracking a new world event with a clock;
"create a situation for [conflict]"; filing something that has a lifecycle.
**Coordinates with:** `wiki-categorize`, `faction-clock`

### `prep-island`
**Purpose:** Create or expand a narrative island — a self-contained, portable cluster of
interconnected content (situations, NPCs, locations, hooks) organized around a coherent
premise. Generate frontmatter with `portable`, `entry_points`, `contains_situations`
fields, run guide structure, scene spine, strong start, toy fields, and linked islands.
**Trigger:** Creating a new narrative island; "prep [location] as a sandbox node";
"create a portable scenario around [entity]."
**Critical behaviors:** Islands contain situations — never the reverse. If content is a
single condition with a clock, it's a situation, not an island.
**Coordinates with:** `prep-situation`, `prep-location`, `prep-npc`

### `prep-ship`
**Purpose:** Create or expand a ship or vehicle wiki page at the correct detail tier.
Tier 0: no file, embed in situation. Tier 1: single file. Tier 2: file + DM companion.
Tier 3: subfolder with index, layout, manifest, owners-manual, dm-guide.
Read the ship tier model from `CLAUDE.md` before generating.
**Trigger:** Creating any named vessel; expanding a vehicle entry; "detail [ship]";
"create the Uncertainty wiki entry."
**Coordinates with:** `prep-location` (for port/home-port entries)

### `prep-encounter`
**Purpose:** Design a combat encounter for the party. Read party combat primer, combat
analytics design flags, and current PC sheets before generating any content. Calibrate
enemy count, CR, terrain, and mechanics to the specific party's empirical combat patterns.
**Trigger:** "Design an encounter", "I need a fight for this session", "build a combat
encounter with [enemy]." Requires `combat-data-extract` to have run at least once.
**Critical behaviors:** Never skip reading the party combat primer and combat analytics.
The party primer's Avoid section is binding — if the encounter would violate it, redesign.
Calibrate to empirical patterns, not theoretical class features.
**Coordinates with:** `combat-data-extract`, `prep-session`, `sandbox-narrative`

### `prep-session`
**Purpose:** Generate a full session run guide — strong start, scene menu, faction
pressures, NPC beats, contingencies. Read party session primer, player interests, active
situations, and last session summary before generating.
**Trigger:** "Prep for next session", "give me a session plan", "what do I run Saturday?"
**Critical behaviors:** Identify which PC hasn't had a meaningful moment recently (from
spotlight tracking in `hot.md`) — build at least one scene that serves that player.
Prep should present options, not a plot. Player agency must have real consequences.
**Coordinates with:** `prep-strong-start`, `prep-encounter`, `player-interest-tracker`,
`sandbox-narrative`

### `prep-strong-start`
**Purpose:** Write the opening scene for the next session — already in motion, no preamble,
immediate stakes. Read `hot.md` current arc, last session "immediate next pressure", and
party primer before writing.
**Trigger:** "Write a strong start", "how do we open next session?", "give me an opening."
**Critical behaviors:** Drop into action already in motion. No "you are in a tavern."
The scene must create immediate pressure without forcing a single response.
**Coordinates with:** `prep-session`, `sandbox-narrative`

### `prep-scene`
**Purpose:** Design a specific scene within a session — social encounter, exploration beat,
NPC interaction, or dramatic moment. Read relevant NPC files, situation context, and PC
primer roleplay levers. Generate scene setup, NPC positioning, dramatic hooks, contingencies.
**Trigger:** "Write a scene between [PC] and [NPC]", "design the confrontation at [location]."
**Coordinates with:** `prep-npc`

### `lore-generation`
**Purpose:** Add new world lore — history, cosmology, cultural context, theology, magic
systems, geographic overview — grounded in existing wiki entities. Read campaign-timeline
and related entity summaries before generating. Flag any contradiction immediately.
**Trigger:** "Expand the lore on [topic]", "write the history of [faction/place]",
"what is the theology of [deity]?"
**Critical behaviors:** All new lore must connect to at least one existing wiki entity
via wikilink. Contradictions go to `discrepancy-log.md` immediately — never resolve
lore conflicts without DM confirmation. New lore that requires a new entity: create the
entity page before writing the lore.
**Coordinates with:** `wiki-categorize`, `prep-npc`, `prep-faction`

### `prep-creature`
**Purpose:** Create or expand a creature or monster entry. Generate stat block reference,
behavioral profile, encounter role, and lore notes. Distinguish between creature-type
lore (`wiki/lore/creatures/`) and a named creature entity (`wiki/entities/`).
**Trigger:** "Create stats for [creature]", "I need a [monster] for the encounter",
"expand the entry for [creature type]."
**Coordinates with:** `prep-encounter`, `lore-generation`

### `prep-dungeon`
**Purpose:** Design a keyed dungeon or exploration site. Generate room keys, connection
map, encounter density, treasure placement, faction occupancy. Apply LLM-wiki keyed format:
concise room descriptions optimized for agent recall, not human prose.
**Trigger:** "Design a dungeon", "key out [location]", "I need a keyed site for [place]."
**Coordinates with:** `prep-location`, `prep-encounter`

### `prep-deity`
**Purpose:** Create or expand a deity entry. Generate divine portfolio, alignment,
worshippers, divine manifestations, relationship to religious factions and lore.
Distinguish between the deity entity (`wiki/entities/deities/`) and theological lore
(`wiki/lore/religions/`).
**Trigger:** "Create a page for [deity]", "expand [god]'s entry", "I need a divine patron."
**Coordinates with:** `lore-generation`, `prep-faction`

### `prep-handout`
**Purpose:** Create a player-facing handout — in-world document, letter, map annotation,
notice, or artifact text. Written from the in-world perspective, spoiler-safe, `audience: players`.
**Trigger:** "Write a handout", "create an in-world letter from [NPC]", "make a readable
for [item]", "I need a notice for the party to find."
**Coordinates with:** `prep-npc`

### `prep-rumor-table`
**Purpose:** Generate a rumor table for a location or faction. Produce a mix of true,
partially true, and false rumors calibrated to what the party could realistically learn
from common sources. Weight rumors toward active situations and player interests.
**Trigger:** "Generate rumors for [location]", "what do people say about [entity]?",
"give me a rumor table."
**Coordinates with:** `player-interest-tracker`, `faction-clock`

---

## Layer 4 — Output & Voice

### `session-summary-write`
**Purpose:** Write the agent-facing session summary at `wiki/sessions/sNNN-summary.md`.
This is a structured intelligence document, not a narrative. Required sections: Fast Read
(arc, major outcome, next pressure), timeline (beat-by-beat with linked entities), canon
established, open threads, wiki updates made, system file updates needed.
Dense, efficient, no flourish.
**Trigger:** Automatically after `transcript-ingest`. "Write the session summary."
**Critical behaviors:** This is NOT a recap — it is an operational intelligence document
written for the agent's future use. Clarity and completeness over readability.
**Coordinates with:** `transcript-ingest`

### `session-recap-write`
**Purpose:** Write the player-facing session recap — narrative prose, past tense, evocative,
spoiler-safe. Written from the party's perspective, covering what the players experienced.
Should feel like the party's own bard retelling the session.
**Trigger:** "Write the session recap", "make the player recap for session N."
**Coordinates with:** `humanize-writing`

### `sandbox-narrative`
**Purpose:** Apply sandbox narrative principles to any content generation. Strong starts
that don't railroad. Situations with multiple genuine outcomes. Content that responds to
player agency rather than authorial intent. All prep is player-entry-point-first.
**Trigger:** Any session prep or situation creation; "make this feel more sandbox";
reviewing prep for railroading patterns.
**Coordinates with:** `prep-session`, `prep-island`, `world-simulator`

---

## Layer 5 — System Maintenance

### `system-file-update`
**Purpose:** Apply system file updates to PC sheets, primers, and party primers after
DM confirms the update list generated by `transcript-ingest`. Update HP, spell slots,
consumables, items, conditions on sheets. Add newly observed combat patterns and avoid
flags to primers. Never updates primers directly from transcript.
**Trigger:** After DM confirms system file updates. "Update the character sheets",
"apply the session updates to the system files."
**Coordinates with:** `transcript-ingest`, `combat-data-extract`

### `pc-primer-create`
**Purpose:** Create a new PC primer from scratch. Read player interview, PC entity page,
and any session data for this character. Generate all sections: Fast Read, Encounter
Levers, Roleplay Levers, Power Spikes table, Key Mechanics, Party Synergies. Mark
theoretical content `[unobserved]` — empirically confirmed patterns have higher design weight.
**Trigger:** New PC joining the campaign; any PC without a primer file;
"create a primer for [PC]."
**Coordinates with:** `combat-data-extract`, `player-interest-tracker`

### `dm-voice`
**Purpose:** Generate content written for read alout call outs and narration.

# Wiki DnD — Prep

Build volatile situations players can't help but mess with. Never write stories — prep reactive systems and get out of the way.

> **Prerequisite:** SKILL.md bootstrap complete — `wiki/index.md` and `CLAUDE.md` already read. Check `wiki/index.md` before naming any entity.

---

## Entity Routing

| Content type | Sub-document |
|---|---|
| NPC | `references/NPC.md` |
| Monster / homebrew creature | `references/MONSTER.md` |
| Encounter | `references/ENCOUNTER.md` |
| Location | `references/LOCATION.md` |
| Faction | `references/FACTION.md` |
| Travel events / session prep | `references/TRAVEL.md` |
| Condition, class, or rule reference page | `references/REFERENCE.md` |
| Ship | `templates/ship.md` + `references/SHIP-GENERATE.md` |
| Homebrew item | `prep-hb-item` skill |

---

## Core Philosophy

1. Prep situations, not scenes. Define pressures + timelines, not outcomes.
2. Every element acts on its own logic when players aren't watching.
3. Player characters are the center of mass. Everything else orbits them.
4. If you removed the players entirely and the world wouldn't change — you wrote a plot, not a sandbox.

**Plot vs. Situation:**
- ❌ "Players will discover the cult and stop the ritual."
- ✅ "There is a cult. They are recruiting. The ritual happens in 5 days. Here's what they want and what happens if no one stops them."

---

## Universal Toy Properties

Any prep element players can't help but interact with must satisfy all four:

1. **Clarity** — instantly understandable, zero lore dump required
2. **Agency** — fight it, negotiate it, exploit it, ignore it (with consequences for each)
3. **Reactivity** — moves even when untouched; the world pushes back
4. **Portability** — works in any town, any party, any campaign

**Three Hooks Rule:** Every major toy needs at least three entry points — moral, personal, opportunistic. Different players latch onto different motivations. If only one type of player would care, the toy will miss half the table.

**Don't wait for players to find your content.** The cult shouldn't just exist in the world — the cult kidnapped the paladin's mentor. The gang didn't just hire muscle — they hired the rogue's old crew. Make it personal before the session starts.

---

## Universal Rules

These apply to all content types. Not repeated per sub-document.

### Relevance Pre-Screen

Before generating anything: **which specific PC's backstory, goal, fear, or active thread does this directly touch?** Name the PC and the connection. If you cannot, do not generate — ask the GM for the PC link first. Content with no PC connection is wasted prep.

**Stakes first.** Lead with what a PC stands to gain or lose before writing lore, personality, or description.

### Interview Protocol

Ask all context questions in a single message. Do not generate until you have answers. If the user message already answers the questions, skip the interview and generate immediately. Never ask more than one clarifying question if you have enough to produce good output.

### Never

- Invent canonical facts — check `wiki/index.md` before naming any entity
- Generate plot — generate pressures, goals, and timelines only
- Skip the PC link — no exceptions
- Pad output — no preamble, no commentary after the content. Output and stop
- Hook to an NPC the party hasn't met — wire through PC backstory instead
- Give a faction a goal the party can't observe
- Use fantasy name slop (Aerin, Vex, Theron, Kael, Lyra, Draven, Zara), decorative apostrophes, or swapped letters
- Write purple prose, character studies, or thematic analysis in wiki pages — Wiki Voice only
- Use wrong callout types — only `[!read-aloud]`, `[!dm]`, `[!mechanic]`, and `[!check]` are valid (see `references/callout-standard.md`)
- Duplicate an existing entity — check `wiki/index.md` first
- Use pre-2024 rules for 5e content

### Reference Loading

Load only what the current task needs.

| Reference | Load when | Path |
|---|---|---|
| Player-facing prose | Writing read-aloud prose | `references/player-facing-prose.md` |
| CR tables | Monster stat design | `references/CR-TABLES.md` |
| Battlefield actions | Solo Boss or Elite monsters | `content/shattered-sea/reference/rules/Battlefield-Actions.md` |
| Pacing heuristics | Session prep thread selection | `references/PACING.md` |
| Strong Start types | Session prep | `references/STRONG-START.md` |
| Island template | Session prep | `references/ISLAND-TEMPLATE.md` |
| Stat block references | Encounter enemy citations | `references/STAT-BLOCKS.md` |
| Named enemies | Encounter with unique named antagonist | `references/NAMED-ENEMIES.md` |
| Universal toys | Campaign setup, Toy Chest, Session Zero, Clocks | `references/UNIVERSAL-TOYS.md` |

### Mechanical Validation

Before writing any stat block value, DC, damage die, spell, or mechanical effect: check existing reference files first.

- **Stat blocks**: Load `references/CR-TABLES.md` before setting HP, AC, attack bonus, or save DCs for any monster
- **Spells**: Use exact 5e spell names — never invent spell names or misremember effects
- **DCs**: Calibrate against DC 10 (easy), DC 15 (medium), DC 20 (hard), DC 25 (very hard)
- **Named rules**: If a rule exists in `content/shattered-sea/reference/rules/`, link to it rather than paraphrasing it

When uncertain whether a rule exists: grep before writing.

### Naming Conventions

Derive names from in-world cultural/linguistic roots matching the entity's origin. Never use fantasy slop (Aerin, Vex, Theron, Kael, Lyra, Draven, Zara), decorative apostrophes, or swapped letters. Rules by entity type:

- **NPC/PC:** First name from racial/cultural phoneme set + family name if setting uses them. No apostrophes unless the language actually elides.
- **Monster:** Derives from geographic or cultural origin — what the local people call it, or a descriptor in their language.
- **Location:** Named by builders or dominant inhabitants. Corrupted over time is fine (e.g., Old Elvish word mispronounced for generations).
- **Faction:** Culturally earned — proper noun group name, title/role collective, corrupted historical, or geographic anchor.

Load `references/NAMES.md` for race-by-race linguistic root table and phonetic principles. When unsure of cultural root, ask before generating.

### World-Building Orientation

| Element | Approach |
|---|---|
| Travel | Speed of plot. Theme, not logistics. |
| Combat | Enemies reflect world themes. |
| Magic | Reflavour to match character backstory where possible. |
| Architecture | Communicates emotion, not engineering. |

Keep underlying math standard 5e. Reskin everything else.

### Toy Fields

Every in-world entity has **toy fields** — frontmatter values that define its active narrative state. Keep frontmatter and body `## Toy Chest` table synchronized so Bases stay queryable and at-table scanning stays fast.

The `appearance` frontmatter field is a single-sentence evocative visual present on all in-world entity types. No plot, no drama.

### Vault Filing

Use the appropriate template from `templates/` (vault root). File to the correct directory per `wiki-core/SKILL.md` vault structure.

**New entity — use Templater (preferred when Obsidian is open):**

Read the matching template in `templates/` before generating content — it defines required frontmatter and section structure. Then create the file:
```bash
# Creates the file from template; then write full content with replace_string_in_file
obsidian templater:create-from-template \
  template="templates/npc.md" \
  file="content/shattered-sea/npcs/Entity-Name.md"
```
For monsters, ships, locations, factions — swap `npc.md` for the matching template. See `templates/CLAUDE.md` for the full template→directory map.

**New entity — direct create (fallback or for full content in one shot):**
```bash
obsidian create name="Entity-Name" path="content/shattered-sea/npcs/Entity-Name.md" \
  content="<full frontmatter + body>" silent
```

**Existing entity — never delete and recreate.** Use `replace_string_in_file`. For frontmatter-only updates, prefer targeted property commands:
```bash
obsidian property:set name="updated" value="2026-05-15" path="content/shattered-sea/npcs/Entity-Name.md"
obsidian property:set name="status" value="active" path="content/shattered-sea/npcs/Entity-Name.md"
```

After writing:
```bash
cd /Users/nick/ai-os/shattered-sea && git add wiki/ && git commit -m "new-<type>: <Name>"
```

`wiki/index.md` is updated by the init skill on every write.

---

## PC Gravity

Every prep element must be wired to a PC's internal tensions.

### Gravity Well Extraction

For each PC, identify from their entity pages:

- **Two Dials** — two core behavioral axes defining their decision-making (e.g., family loyalty / reckless ambition). Must be internal tensions, not surface traits.
- **Terminal Node** — single deepest long-term desire. Asymptotic — the PC approaches but never cleanly arrives.
- **Active Friction** — what currently blocks them. This is where you place toys.

### The Gravity Filter

Every entity must pass: **does this pull on at least one PC's dials or terminal node?**

- Yes → include it, note which PC and how
- No → cut it, or retrofit a connection

### Anti-Patterns

| Bad Prep | Why It Fails |
|---|---|
| Content unconnected to PC wells | Players drift past it |
| Hooks requiring players to care about strangers | No internal gravity |
| All pulls in the same direction | Removes meaningful choice |
| Terminal Node treated as solvable | Kills the gravity well |
| Only one dial threatened | Half as interesting as both dials in opposition |

---

## Roleplay Method — Pop Culture Mashup

Every NPC and intelligent monster gets a **Roleplay Concept**: a mashup that loads voice and energy in one line.

**Formula:** `[unexpected animal/archetype/vibe] + [pop culture character/persona]`

Examples: *owl Obi-Wan Kenobi* · *rat grandma Scarface* · *southern golden retriever lawyer* · *burned-out vice principal Voldemort* · *yoga instructor who is also a hitman*

The mashup is the character's **operating system** — not look, not job, not backstory. Every choice flows from it. The two halves must create tension (warm AND territorial, menacing AND exhausted). If a line could belong to any character, rewrite it.

### Voice & Delivery Block

For every performed character, output:

- Speech patterns, vocabulary, verbal tics
- 2–3 actual lines the DM can say at the table
- Physical mannerisms (hands, eye contact, posture)
- Emotional default + what cracks it

### Performance Hooks

2–3 specific DM moves: when to lean into the bit, when to let the crack show, when to surprise. Write these as felt actions, not clinical instructions.

**Skip the mashup** for mindless beasts, constructs with no dialogue, or entities with no speaking role.

**Gimmick rule:** A gimmick is a launchpad, not a ceiling. One-time NPCs can live entirely in the bit — that's fine and often hilarious. Recurring characters need to eventually surprise even you; the moment their choices stop being predictable, the gimmick did its job. A recurring character who never develops past their gimmick becomes annoying, not memorable.

---

## Narrative Mindset

Narrative devices are tools for world-building, not plot control. Place loaded guns — players decide when they fire.

| Device | How to apply |
|---|---|
| **Chekhov's Gun** | Seed elements with future weight; don't aim them |
| **Foreshadowing** | Hint at conditions and threats, not scripted events |
| **Ticking Clock** | Factions pursue goals on timelines; inaction has visible consequences |
| **Reversal** | Give NPCs/factions hidden layers that produce genuine surprise when revealed |
| **The Iceberg** | Build more world than players will see; depth makes the visible tip feel real |
| **In Medias Res** | Start scenes mid-action, not at the beginning |

After generating content: which devices are present? Which are missing? What would make this feel more alive?

---

## PC Sheet

File: `content/shattered-sea/party/[Character-Name].md`. Template: `templates/pc-sheet.md`.

### Required frontmatter

| Field | Notes |
|---|---|
| `type` | Always `pc` |
| `name` | Character name |
| `player` | Player name |
| `class` / `subclass` | Both required even if subclass is TBD |
| `level` | Integer |
| `race` / `subrace` | Both fields; subrace may be `null` |
| `background` | PHB background name |
| `alignment` | Two-word alignment or `unaligned` |
| `xp` | Integer |
| `status` | `active`, `retired`, or `deceased` |
| `campaign` | Slug of the campaign page |
| `tags` | Minimum: `pc`, campaign slug |

### Filling the sheet

- **Ability scores:** Include both score and modifier. Modifier = `floor((score - 10) / 2)`.
- **Saving throws:** Mark `Prof?` with `Y` for proficient saves; add proficiency bonus.
- **Skills:** `Y` = proficient; `E` = expertise (doubles proficiency bonus).
- **Passive Perception:** `10 + WIS modifier + proficiency (if proficient) + bonuses`.
- **Spell slots:** Include only levels with slots. Remove unused rows.
- **Features & Traits:** One mechanical sentence per feature. Wikilink to rules pages where they exist.
- **Session Notes callout:** Live scratchpad — update each session; don't create separate note files.

### Updating an existing sheet

1. Read the current file before writing.
2. Update only changed fields — do not regenerate the full sheet.
3. Bump `updated` frontmatter date.
4. If `level` increases, recalculate proficiency bonus, saving throws, skill modifiers, and spell slots.

# World Update Workflow

Complete post-session ritual. Follow in order. Do not skip steps.

---

## Canon Discipline

Every claim must be grounded in something you have read. Not inferred. Not extrapolated.

Before proposing a thread's advancement, read its situation file. Before naming an NPC's
status, read their page. If you don't have a file that supports the claim, either go read
it or don't make the claim.

**Failure modes to avoid:**
- **Timing errors** — a clock doesn't start until its trigger fires. Read the situation
  file to verify before assuming it's in motion.
- **DM notes leaking into world state** — intent is not fact. It hasn't happened until a
  session log says it happened.
- **Invented consequences** — an unresolved event has no consequences yet.
- **Assumed destinations** — never state or imply where the party goes next.

---

## Step 1: Load Context

Read in this order:

1. Most recent session recap (`wiki/sessions/session-NN-recap.md`)
   - If recap doesn't exist, ask the DM for a summary before proceeding
2. `wiki/hot.md` — current world state, faction clocks, live situations, spotlight
3. All files in `wiki/situations/active/` — read at minimum the frontmatter, summary,
   and current state of each
4. Relevant narrative island files referenced by active situations

From the session recap, extract:

- **Situations engaged** — which threads the party directly interacted with
- **Durable changes** — what permanently changed (ship state, NPC relationships, items,
  levels, location)
- **PC moments** — per-PC spotlight beats and character-defining choices
- **Threads left open** — what the recap flags as unresolved

---

## Step 2: Triage Threads

Classify every active or brewing thread into one tier.

### HOT — Engaged This Session

The party directly interacted with this thread. A faction, NPC, or force must react to
what they did.

**Identify from:** Session recap names the situation, NPC, or faction. The party took
action that changes the thread's state.

### WARM — Previously Engaged, Not This Session

The party knows about this thread but didn't engage this session. The faction continues
its agenda in their absence.

**Identify from:** Listed in hot.md live situations with party awareness not "none", but
the session recap doesn't mention it.

### COLD — Brewing, Party Unaware

The party hasn't engaged with this thread. A villain, faction, or force is advancing its
plan. Effects are subtle — ripples the party won't notice unless they're looking.

**Identify from:** Dormant situations, unactivated narrative island threads, faction plans
the party hasn't encountered. Not every dormant thread qualifies — only those with active
momentum: a faction pursuing a goal, a timer counting down, a force in motion.

### Present for Confirmation

Before rolling, present the full triage:

> **HOT threads (engaged this session):**
> 1. [Thread] — [what the party did]
>
> **WARM threads (party aware, not engaged):**
> 1. [Thread] — [faction's likely action]
>
> **COLD threads (brewing):**
> 1. [Thread] — [what's advancing]
>
> Anything to add, remove, or reclassify?

Wait for DM confirmation before proceeding.

---

## Step 3: Process Each Thread

Work through all tiers in order: HOT first, then WARM, then COLD.

### 3a. Read and Propose

Read the situation file in full. Read the relevant faction or NPC file. Only after reading
both, form one clear sentence about what this entity was trying to accomplish.

Frame by tier:

- **HOT:** "In response to [party action], [entity] attempts to [concrete action]."
- **WARM:** "While the party is elsewhere, [entity] pursues [concrete goal]."
- **COLD:** "Unopposed, [entity] advances [concrete plan]."

### 3b. Roll

```bash
.claude/skills/roll-dice/roll.sh d20
```

The result is canon. No re-rolling. No softening. No "that doesn't fit the narrative."

### 3c. Interpret

| Roll | Outcome |
|------|---------|
| 1–5 | **Setback.** Attempt failed or backfired. Plans exposed, resources wasted, opposition stiffened, an unexpected complication arose. |
| 6–15 | **Partial.** Real progress but friction. Something worked, something didn't. A cost or complication accompanies the advance. |
| 16–20 | **Full success.** They accomplished what they set out to do. The world shifts. |

**Interpretation varies by tier:**

- **HOT threads:** A setback means the faction's response to the party is weak or
  misdirected — the party's action was more effective than expected. A success means
  the faction responds powerfully — new pressure, new consequences the party will feel.

- **WARM threads:** A setback means the faction hit internal resistance or external
  interference while the party was occupied. A success means they advance cleanly — the
  party returns to find changed ground.

- **COLD threads:** A setback means the plan stalls from friction (infighting, resource
  shortage, bad luck). A success means the villain advances significantly — the ripples
  grow stronger, the hooks sharpen.

**Every result must change something.** A setback is not "nothing happened." It's a
faction that overreached, tipped their hand, got hit from a direction they didn't see,
or lost a resource they'll need later. Even failures create new world state.

Follow faction logic, not narrative convenience. The world is honest, and honesty is
more interesting than managed drama.

### 3d. Write Immediately

Update every relevant wiki page before moving to the next thread:

- **Situation file** — append a session log entry. Update current state, pressures, clocks
  if changed. Format:

  ```markdown
  ### World Update — Session NN
  **Roll:** [N] — [Setback / Partial / Full Success]
  [2–4 sentences: what happened, what changed, what becomes visible]
  ```

- **NPC files** — update status, location, relationships, or active goal if changed
- **Faction files** — update agenda, resources, off-screen action if changed
- **Location files** — update current hooks if the ground situation changed

For **COLD threads**, add a hook escalation note:

```markdown
### World Update — Session NN (Cold)
**Roll:** [N] — [Outcome]
[One sentence: what the faction did]
**Hook strength:** [Whisper / Ripple / Wave / Collision] — [what the party could notice]
```

### 3e. Collisions

If two threads act against each other in the same time window, resolve as one beat:

- Roll once for the collision
- High roll favors the faction with better position/resources/information
- Low roll favors the weaker or more desperate faction (upsets are interesting)
- Write the collision result to both situation files

### 3f. Continue

Move to the next thread. No confirmation needed between threads — the DM approved the
triage in Step 2.

---

## Step 4: Cold Thread Escalation

Cold threads accumulate advances across world updates. Track the count by counting
world update entries in each situation file's session log. As advances accumulate,
hooks grow:

| Advances | Hook Strength | What changes |
|----------|---------------|-------------|
| 0–1 | **Whisper** | Only visible if someone is looking. A rumor in a tavern the party won't visit. A distant ship sighting no one reports. |
| 2–3 | **Ripple** | Noticeable to an attentive party. An NPC mentions something unusual. A price shifts. A familiar name surfaces in unfamiliar context. |
| 4–5 | **Wave** | Hard to miss. Faction agents appear near the party. An ally reports trouble. A resource the party relies on is affected. |
| 6+ | **Collision** | Forces engagement. The thread directly impacts something the party cares about — their ship, their allies, their plans. |

When a cold thread reaches **Wave** strength, reclassify it as WARM in hot.md —
party awareness shifts to "rumors" or "indirect pressure."

When a cold thread reaches **Collision** strength, reclassify as HOT. The thread is
now in the party's face whether they like it or not.

This is the mechanical heart of living world design: villains continue their plans,
and those plans inevitably reach the party. Not because the DM steers them there, but
because the world is small enough that power moves create waves.

---

## Step 5: PC Arc Weaving

After all threads are processed, step back and look at the campaign's emerging narrative.

### 5a. Convergence Scan

Review the thread outcomes. Do any threads from different PCs naturally point toward
the same place?

**What to look for:**
- Two PC-connected threads share a faction, location, or NPC
- A thread's outcome creates pressure on a second PC's dials or terminal node
- Two consequences point at the same event, location, or discovery
- A COLD thread's ripple reaches into a HOT thread's space

If convergence is natural — it emerged from actual events and roll outcomes, not from
you looking for it — note it in hot.md predictions. One line: what threads, how they
intersect, what could happen if the party follows both.

**Do not manufacture convergence.** If two threads don't intersect, they don't intersect.
The campaign has time. Forced convergence is a railroad by another name.

### 5b. Spotlight Balance

From hot.md spotlight tracking:

- Which PC has gone longest without a meaningful moment?
- Did this session's events advance all four PCs, or did development cluster?

If a PC is falling behind, note which WARM or COLD thread could naturally pull on their
specific tensions. Don't force the thread — flag the opportunity for next session's prep.

### 5c. Narrative Device Seeding

Review thread outcomes against the sandbox narrative device catalog (load
`sandbox-narrative` if not already loaded):

| Device | What to look for | Where to note it |
|---|---|---|
| **Chekhov's Gun** | Something placed this session that could fire later | hot.md predictions |
| **Foreshadowing** | Thread outcomes that hint at conditions developing | hot.md predictions |
| **Ticking Clock** | A faction timeline creating urgency the party can feel | hot.md faction clocks |
| **Dramatic Irony** | Party knows something a faction doesn't, or vice versa | Situation file DM notes |
| **Slow Burn** | Elements seeded across 2+ sessions approaching critical mass | hot.md predictions |
| **Convergence Arc** | Independent threads beginning to collide on a shared timeline | hot.md predictions |

These observations feed directly into `prep-session` for the next session. They are
suggestions, not mandates — the DM uses them or discards them.

### 5d. The Weaving Principle

The goal across many sessions of world updates is not to write a plot. It is to track
what the world does honestly and watch the narrative patterns that emerge from the
collision of player choices and world momentum.

When two PCs' stories start orbiting the same pressure — not because you steered them
there but because the world is a connected place — that is the campaign writing itself.
Note it. Protect it. Let it breathe.

The party becomes heroes not because you cast them as heroes but because the pressures
the world applies to them demand heroic response. The world-update skill's job is to
apply those pressures honestly and watch what happens.

---

## Step 6: Close Out

### 6a. Update hot.md

Refresh every section with the new world state:

- **Current Arc** — party's position and immediate situation
- **Open PC Threads** — per-PC active friction, updated from this session and world update
- **Faction Clocks** — new states, updated triggers, If Ignored consequences
- **Live Situations** — status changes, awareness changes, next beats updated
- **Predictions** — revised with thread outcomes, convergence notes, and narrative device
  observations
- **Spotlight Tracking** — reset sessions-since for PCs who had moments; increment others

### 6b. Situation Lifecycle

- **Resolved:** Move from `active/` to `resolved/`, set `lifecycle: resolved`
- **Activated:** Move from `dormant/` to `active/`, set `lifecycle: active`
- **New situations:** If a cold thread generated a new visible pressure, create a new
  situation file using `prep-situation` format. File it in `wiki/situations/active/`
  or `wiki/situations/dormant/` based on lifecycle.

### 6c. Index

If new files were created:

```bash
python3 .claude/scripts/regen_index.py --write
```

### 6d. Commit

Stage and commit all wiki changes:

```bash
git add wiki/
git commit -m "world-update: session NN — [brief summary of major changes]"
```

---

## Quality Checks

Before committing, verify:

- [ ] Every thread had a d20 roll via `.claude/skills/roll-dice/roll.sh d20`
- [ ] Every state claim was read from a wiki page, not assumed or inferred
- [ ] No DM design note was treated as established world fact
- [ ] No thread assumed where the party goes next
- [ ] Every changed state was written to its owning page — not just hot.md
- [ ] Every result changed something — no "nothing happened" outcomes
- [ ] Faction collisions (if any) were resolved once, not double-counted
- [ ] Cold thread hook strengths were updated based on accumulated advances
- [ ] PC arc weaving observations are in hot.md predictions
- [ ] Spotlight tracking was updated
- [ ] Roll results were treated as canon — no softening, no re-rolling

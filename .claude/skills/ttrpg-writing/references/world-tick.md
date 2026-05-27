# World Tick

The world didn't pause while the party played. Now you find out what happened offscreen.

This is a collaborative ritual — efficient, methodical, one thread at a time. You read the
situation, propose what that faction or NPC was trying to do, the DM confirms or redirects,
the dice decide the outcome, and you write every change directly to the wiki. No gaps, no
deferred updates, no vague notes.

---

## Canon Discipline

Every claim you make must be grounded in something you have read. Not inferred. Not extrapolated. Read.

Before proposing a thread, read its situation file. Before naming an NPC's status, read their
page. Before describing what anyone knows or doesn't know, verify it in the wiki. If you don't
have a file open that supports the claim, either go read it or don't make the claim.

**Specific failure modes to avoid:**
- **Timing errors** — a clock doesn't start until its trigger fires. Read the situation file
  to find the trigger before assuming it's in motion.
- **DM notes leaking into world state** — if something is in a DM design note, it is intent,
  not fact. It has not happened until a session log entry says it happened.
- **Invented consequences** — a fight in open water is invisible. A missed check-in that hasn't
  happened yet has no consequences yet.
- **Assumed destinations** — never state or imply where the party is going next.

When in doubt: read the file, then speak. Never the other way around.

---

## Step 1: Find the Session Recap

Look for the most recent session material in this order:

1. `content/shattered-sea/private/sessions/` — agent-facing session summary (preferred)
2. `content/shattered-sea/sessions/` — player-facing recap as fallback

If neither exists, ask:

> "I don't have a session recap to work from. Give me a quick rundown — what the party did,
> who they interacted with, what threats are active, what they ignored — and I'll work from that."

You need: who the party engaged with, what locations they were in, what threats are visibly
in motion, what they left alone.

---

## Step 2: Identify Active Threads

Read `content/shattered-sea/situations/index.md` alongside the recap. Then read the situation
file for any thread you're considering before proposing it — don't propose a thread based on
the index summary alone.

**Only tick threads the party has touched.** A faction the party has never encountered doesn't
get a turn — their drama belongs to a session where it can matter.

A thread qualifies if:
- The party directly engaged with it this session or in recent sessions
- A faction or NPC the party knows has clear motivation to react to what the party just did
- The party's absence from a thread they were previously involved in is itself meaningful

**Before proposing any thread, verify:**
- The thread's current state is actually what you think it is
- Any clocks or triggers you're referencing have actually fired
- The thread's key actors are doing what their file says, not what seems narratively logical

Order by proximity to the party's active interests. Leave dormant threads, distant factions,
and NPCs the party hasn't met out of the tick entirely.

Present your list before proceeding:

> "I'm planning to tick these threads: [list with one-line summaries]. Anything to add, skip,
> or reorder?"

Wait for confirmation.

---

## Step 3: Tick Each Thread

Work through the list one at a time. Don't move to the next thread until the current one is
fully written.

### 3a. Read and Propose

Read the situation file in full. Read the NPC or faction file if one exists. Only after reading
both, form a single clear sentence about what this entity was trying to accomplish during this
interval. Do not rely on what you remember from earlier in the conversation — re-read the file.

> "[Entity] was trying to [specific concrete action] this week. Does that track, or do you
> see it differently?"

Keep it tight — one action, one sentence. The DM may redirect. Use their version. This is their
world. The goal you confirm here is what the roll resolves.

### 3b. Roll

> "Roll a d20."

Wait for the number. Don't interpret yet.

### 3c. Interpret

| Roll | Outcome |
|------|---------|
| 1–5 | **Setback.** Their attempt failed or backfired. Plans exposed, resources spent badly, opposition stiffened, or an unexpected complication arose. |
| 6–15 | **Partial.** Real progress but friction. Something worked, something didn't. A complication or cost accompanies the advance. |
| 16–20 | **Full success.** They accomplished what they set out to do. The world shifts. |

Be specific and interesting. Every result — including setbacks — should shift something the
party will eventually feel. Name what changed: which NPC moved and where, what was learned
or exposed, what resource was spent or gained, what the party will walk into differently.

A low roll isn't "nothing happened" — it's a faction that overreached, tipped their hand,
or got hit from a direction they didn't see.

Follow faction logic, not narrative convenience. The world is honest, and honesty is more
interesting than managed drama.

**What the result must not do:**
- Reference DM design notes as established world facts
- Imply consequences from unresolved events
- State or imply where the party goes next
- Invent NPC knowledge, locations, or status not in their file

### 3d. Write Immediately

Update every relevant page before moving to the next thread:

- **Situation file** — update the Current State section; append a `### World Tick — [YYYY-MM-DD]`
  entry in the session log
- **NPC files** — update status, location, relationships, or active goal if involved
- **Faction files** — update resources, power, active goal, or known state
- **Location files** — update Current Hooks if the action changed the situation on the ground

Set `updated: YYYY-MM-DD` on every page you touch. Do not leave gaps.

### 3e. Confirm and Continue

After writing:

> "Done — [one sentence on what changed]. Next up: [Thread Name]. Ready?"

Wait for go, then move to the next thread.

---

## Step 4: Close Out

After all threads are ticked:

1. Update `content/shattered-sea/situations/index.md` if any threads resolved, escalated, or
   changed status
2. Refresh `content/hot.md` with the new world state
3. Commit: `git add content/ && git commit -m "world-tick: [session number or date] offscreen advancement"`

# Manual lore consistency review

The script catches structural lore drift (dead-entity-ref, island-situation-mismatch,
status-drift, parent-gap) but cannot read prose for meaning — and it cannot reason
about time. After working the automated report, do a manual pass over files the
script flagged or that you touched during fixes. Temporal consistency (when things
happened, whether movements and durations are physically possible, whether "current
state" claims have decayed) is the highest-value part of this pass. This is where
an LLM-wiki agent earns its keep — the compounding knowledge base is only as
reliable as its internal coherence.

## What to check

**Contradicted facts across files.** When a file states a fact about another entity
(location, allegiance, status, event), open the target entity's page and verify the
claim matches. Common drift patterns:

- An NPC page says they're in Calveno, but a situation page places them at sea
- A session recap says an event happened during Session 02, but the NPC's page
  describes it as Session 03
- A faction page says NPC X is a member, but NPC X's page says they left
- A place's body says it's governed by faction A, but faction A's page doesn't
  list that place
- An item page says it was found in location X, but the session where it was
  found places the party somewhere else

When you find a contradiction: check session notes (the primary source) to determine
which version is correct. Fix the wrong one. If both could be right (ambiguous source
material), append to `wiki/discrepancy-log.md` — don't guess.

**Temporal consistency.** This is judgment work that no script can do — it requires
understanding when things happened in-world, what was physically possible given
distances and durations, and whether entity pages reflect the world as it stands
after the most recent session.

Session notes are the authoritative timeline. The in-world clock is layered:
sessions map to stretches of in-world time, and within a session the day structure
(e.g. Session 04's Day 1–5 files) establishes what happens when. Reconstructing
the timeline for a specific entity or event means reading the session files that
touch it and building a sequence: where were they, what happened, how much time
passed.

**What to check:**

*Session-number accuracy.* When a page cites "Session 02" or "in Session 03,"
verify the event actually occurred in that session. Open the session recap or
scene file and confirm. Common drift: events get attributed to the session where
they were *discussed* rather than the session where they *happened*.

*In-world day sequencing.* When session files use day numbering (Day 1, Day 2),
entity and situation pages that reference those events should be consistent with
the day they occurred. A ship that docks on Day 1 cannot have a completed 5-day
refit on Day 3. An NPC who departs at dawn on Day 2 should not appear in a scene
set on Day 1 evening as already gone.

*Location-time plausibility.* If an NPC is established as being in location A
during a specific session or day, they cannot simultaneously be in location B
unless travel is plausible in the elapsed time. This applies to the party too —
check that "the party did X in Calveno" claims don't conflict with travel
timelines. The campaign is nautical; sea travel takes days, not hours.

*"Current state" decay.* Entity pages, situation files, and hot.md all carry
claims about the present: "currently docked at La Vasca," "Grigori is aboard,"
"the favor has not been named." Each of these has a session-of-origin. When a
later session changes the state, every page that cached the old state needs
updating. The most dangerous form is a callout or info box labeled
"post-Session N" — these read as authoritative but rot silently.

*Causal ordering.* Some events depend on others: Nona calling off the attacks
requires Perrin to have met her first. The sending stone can't be used before
it's given. When a page describes consequences, verify the cause has already
occurred in the timeline. This catches cases where world-building pages
(written ahead of play) describe outcomes that haven't happened yet in the
session record.

*Concurrent timeline plausibility.* Multiple threads run simultaneously in
Calveno (ship repair, festival days, raid prep, NPC movements). When two
threads reference the same in-world day, their claims must be compatible.
The raid prep timeline in one file and the festival schedule in another should
agree on which day is which.

**How to do it:** Don't try to audit the entire timeline at once. Start from
the files the automated lint flagged or the files you touched during fixes.
For each temporal claim, trace it back to its session source. Use
`qmd query` or `obsidian search` to find cross-references efficiently. When
you find a mismatch, check the session recap (primary source) to determine
which version is correct. Fix the wrong one. If both could be right, or if
the timeline is genuinely ambiguous in the source material, append to
`wiki/discrepancy-log.md`.

**hot.md coherence.** After any batch of fixes, scan `wiki/hot.md` for claims that
conflict with what you just corrected. hot.md is the most-read file and the most
likely to go stale. If it references a dead NPC as active, a resolved situation as
live, or a ship's captain who's been killed — fix it.

**Entity identity.** Two pages may describe the same entity under different names or
from different angles (e.g. `leviathan.md` creature vs NPC — see
`wiki/discrepancy-log.md` for the live example). When you suspect identity overlap:

- Do NOT merge or resolve on your own
- Append to `wiki/discrepancy-log.md` with both file paths, what overlaps, and
  your recommendation
- Leave both pages intact until the DM decides

## When to do a manual pass

- **After ingest** — new source material is the #1 cause of lore drift. The ingest
  skill creates/updates entity pages from session notes, which may contradict existing
  content written from earlier sessions or world-building.
- **After working the automated report** — the files the script flagged are already
  open in your context. Scan their prose while you're there.
- **After a world-update** — faction clock advances and situation resolution can
  invalidate claims in entity pages.
- **When the DM asks** — "check consistency", "anything contradictory", "does this
  all hang together" all trigger this manual pass.

## What NOT to do

- Don't read every file in the vault looking for contradictions. Use the script output
  and `qmd query` / `obsidian search` to target files that reference each other.
- Don't invent lore to resolve a gap. If two files disagree and the session notes don't
  clarify, escalate — don't pick a side.
- Don't silently change established facts. If an NPC's allegiance needs updating because
  of session events, that's a legitimate correction. If two world-building files
  disagree about geography and neither has session backing, that's a discrepancy-log
  entry.

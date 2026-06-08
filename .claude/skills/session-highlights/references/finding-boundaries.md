# Finding highlight boundaries

The detector gives you the laugh. You decide where the **bit** starts and ends.

## Where the setup STARTS

The laugh fires on the payoff; the setup is whatever made the payoff land. Read the
transcript backward from the laugh until you hit the **premise** — the line a listener
needs to find the punchline funny — and start one beat before it, at a natural
conversational boundary (a new topic, a question, a scene-set).

Heuristics:
- **A callback** needs the thing it calls back to. Include it even if it's 40s earlier.
- **An in-character bit** needs its framing — the DM's scene-set that makes the line land
  ("you walk into the crowded Calveno market and announce…").
- **A deadpan beat** needs the tension it breaks — include the in-game stakes it punctures.
- Stop walking back when earlier lines are unrelated table talk (and if the whole bit is
  table talk, it's OOC — discard the moment per the in-world requirement).

There is no fixed window. 60s is the script's default scaffold, not the answer. Some bits
are 15s; some are 75s.

## The run-on row trap

The transcription packs long uninterrupted speech into a **single CSV row** spanning 30s+.
A line-count window ("grab the previous 20 rows") will silently skip the whole setup because
it lives in one row. Always read the *text and End−Start span* of each row near the laugh —
a 32-second row is a monologue, not a one-liner. The setup may be entirely inside it.

## Where it ENDS (use `laugh_end`, then capture the follow-on)

The scan gives you a data-driven forward boundary: each burst's **`laugh_end`** (in
`laughs.json` and the draft context) is where the laughter decays back to the track's average —
i.e. where the room goes quiet again. Because laughter stays elevated *between* back-to-back
jokes, `laugh_end` naturally spans the whole cascade: the punchline, the room's reaction, AND
the immediately-following jokes/riffs that ride the same wave.

**Extend the script and the clip forward to `laugh_end`** (plus a beat). Read the transcript
forward through `laugh_end` and include every follow-on joke and reaction in that window —
don't stop at the first button. The detected burst is where laughter was *heard*, often slightly
behind the line that caused it, so the funniest line and its follow-ups frequently land at or
after the burst; `laugh_end` is past all of them.

A mechanical "cut on the laugh" clip fails twice: it ends as (or before) the funniest line
lands, and it drops the follow-on jokes the table was still laughing at.

If a purely-meta aside (a pop-culture reference, a rules quip) falls *inside* the `laugh_end`
window, keep extending the clip/boundary to `laugh_end`, but trim that aside from the *quoted
script* — keep the in-world spine. The audio span and the written script don't have to be
line-for-line identical when a stray meta line is in the middle.

## Translating to clip times

Burst `part_time` is mm:ss local to the part. Convert your chosen setup-start and button-end
to local seconds, then cut with ffmpeg (`-ss start -t duration`). The clip and the chat log
must cover the **same** span — if you extended the dialogue back to 13:49, the clip starts at
13:49 too.

# Finding highlight boundaries

The detector gives you the laugh. You decide where the **bit** starts and ends.

## Where the setup STARTS

The laugh fires on the payoff; the setup is whatever made the payoff land. Read the
transcript backward from the laugh until you hit the **premise** — the line a listener
needs to find the punchline funny — and start one beat before it, at a natural
conversational boundary (a new topic, a question, a scene-set).

Heuristics:
- **A callback** needs the thing it calls back to. Include it even if it's 40s earlier.
- **A deadpan deflation** ("So… eel.") needs the tall thing it deflates — include the
  full rant it punctures.
- **An in-character line** needs its framing ("you walk into a crowded market and say…").
- Stop walking back when earlier lines are unrelated table talk.

There is no fixed window. 60s is the script's default scaffold, not the answer. Some bits
are 15s; some are 75s.

## The run-on row trap

The transcription packs long uninterrupted speech into a **single CSV row** spanning 30s+.
A line-count window ("grab the previous 20 rows") will silently skip the whole setup because
it lives in one row. Always read the *text and End−Start span* of each row near the laugh —
a 32-second row is a monologue, not a one-liner. The setup may be entirely inside it.

## Where it ENDS (the button)

**The detected burst is where laughter was *heard*, which is often slightly behind the line
that caused it — so the actual punchline may fall AT or AFTER the burst start.** Always read
*forward* past the burst until the bit is clearly over. End a beat after the button — the
reaction line or DM response the laugh fires on ("You're at 30 already. He's still going.";
"Get two birds stoned at once."). Don't cut on the burst timestamp; cut after the line that
earned it, even if that line is several seconds past the burst.

This is why a mechanical "cut on the laugh" clip fails: it ends right as (or before) the
funniest line lands.

## Translating to clip times

Burst `part_time` is mm:ss local to the part. Convert your chosen setup-start and button-end
to local seconds, then cut with ffmpeg (`-ss start -t duration`). The clip and the chat log
must cover the **same** span — if you extended the dialogue back to 13:49, the clip starts at
13:49 too.

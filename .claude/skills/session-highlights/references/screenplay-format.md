# Screenplay format for highlight scene files

Each highlight is its own scene file written as a **short screenplay** — a self-contained,
drawable scene a downstream art agent can illustrate without chasing wikilinks. The screenplay
is an *adaptation*: faithful to what happened and what was said, staged with detail pulled from
the wiki.

## The fidelity contract (read this first)

Two sources of truth, two jobs:

| Element | Source of truth | Rule |
|---|---|---|
| **In-character dialogue** | the embedded audio clip | Keep it **faithful** — what the speaker actually said, lightly cleaned (filler/false-starts), never reworded for flavor. The clip is provenance; the script must not drift from it. |
| **Events / actions** | the transcript | Render what the players *declared* happens, nothing more. Never invent an outcome, a line, or a beat that didn't occur. |
| **Setting & appearance** | the wiki (`ttrpg-wiki-query`) | This is the enrichment. Slugline, location look, weather/light, and each character's appearance come from their canonical pages. |

The screenplay reads cinematically, but it invents **nothing** about the story. You are
re-staging a real moment, not writing fan fiction.

## Translating table-talk into screenplay

Players narrate in first person, mixing speech and stage-direction. Split that stream:

- **In-character speech → dialogue.** "I take a long, deep drag on my cigarette" describes an
  action, so it becomes an action line — but "*Hello. I am looking for a bird, a rat, and a sexy
  human*" is something the character *says*, so it stays dialogue, verbatim.
- **First-person action declarations → action lines.** "I reach up and pull the dagger out"
  becomes: *Jean-Claude plucks the dagger from his shirt; it dissolves into smoke in his hand.*
  Third person, present tense, faithful to the declared action.
- **DM narration → action lines or a parenthetical** depending on whether it's world description
  or an NPC speaking. NPC speech (DM "as the grung") is **dialogue** under the NPC's name.
- **The laugh beat stays.** Mark where the table laughter lands with `> 😂 **— big table laugh —**`
  on its own line, in script order. It is part of the scene's rhythm and tells the art agent which
  beat is the punchline. If one scene has two laughs of different size, distinguish them —
  `> 😂 **— table laugh —**` for the smaller, `> 😂 **— big table laugh —**` for the peak.

## Layout

```markdown
---
{frontmatter — see SKILL.md output contract}
---

# Session {NN} · Highlight {n} — "{title}"

> [!info] Setting
> **Where:** {location, wikilinked} — {one line of look/light/atmosphere from the wiki}
> **Who:** {each character in the scene, wikilinked, + a half-line of appearance from their page}
> **Beat:** {one sentence — what makes this funny / what the art should capture}

## Screenplay

**{INT./EXT. LOCATION — TIME}**

*{action line: stage the opening — who's where, what the place looks like}*

**{CHARACTER}** *(parenthetical: tone/business)*
{faithful in-character dialogue}

*{action line}*

**{NPC}** *(as voiced by the DM)*
{faithful dialogue}

> 😂 **— big table laugh —**

*{action line: the follow-on beat / button that rides the same laugh}*

## Audio
![[{rank}_{slug}_part{P}.m4a]]
**From:** session{NN}-part{P} @ {mm:ss}–{mm:ss}  (peak {p}, intensity {i}; laugh_end {mm:ss}) — provenance only, not a listening cue.
```

## Notes

- **Audio goes at the END**, under its own `## Audio` heading — the screenplay reads top to
  bottom, then you can press play to hear the real thing.
- **Wikilink on first mention** per scene file (the Setting block is the natural spot); plain text
  thereafter. Resolve every name to its canonical page — never the transcript's phonetic spelling.
- **Appearance lines are for the art agent.** One concrete half-line each (species, build, signature
  gear/colour) pulled from the character's page — enough to draw them, not a biography.
- **Keep it tight.** A highlight is 15–75s of table time. The screenplay is a page, not an act.
- **Span matches the clip.** Script from scene-start through `laugh_end` (+a beat); the embedded
  clip covers the same span. A stray purely-meta aside inside the window may be trimmed from the
  script while the clip still runs to `laugh_end`.

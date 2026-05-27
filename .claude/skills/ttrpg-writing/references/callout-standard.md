# Callout Standard

Four types. Nothing else. Auto-correct any deviation you find without asking.

The quick reference is in SKILL.md. This file covers content rules, examples, the conversion
table, and per-domain defaults.

---

## Content Rules

### `[!read-aloud]`

Apply player-facing prose mode (SKILL.md) when writing or rewriting read-aloud content.

Write for the mouth. The DM reads this exactly; players hear it. Max 4 sentences. No conditional
framing. No stage directions in the text. Nothing that only makes sense on a page.

**Good:**
```
> [!read-aloud]
> The harbour opens around you — stone quays stacked with barrels, a dozen languages, gulls
> working the fish market at the south end. The Surety slides into her berth like she belongs there.
```

**Bad:**
```
> [!READ-ALOUD]
> [If the party succeeded at the approach] The harbour opens around you, if you made it this
> far, and the city seems to breathe with possibility and mystery as the ship finds her place.
```

Fix: lowercase the type. Strip conditional framing — that's a `[!dm]`. Cut "possibility and mystery."

---

### `[!dm]`

One directive per callout. Start with a verb or concrete noun. Max 3 sentences. Dense,
scannable — the DM reads this mid-scene. No atmosphere, no hedging, no "consider whether."

**Good:**
```
> [!dm]
> Don't explain Grigori's healing. Move on — Sem needs help, or Noor drops something. Grigori
> watches the horizon.
```

**Bad:**
```
> [!dm]
> At this point you might want to consider whether the players are ready to receive this
> information, as it could potentially be something they find surprising.
```

Fix: one sentence. "Hold this until the party asks directly."

---

### `[!mechanic]`

Lead with the trigger or condition. Consequence follows. Tables beat prose. No narrative
padding — just the rule and what it does.

**Good:**
```
> [!mechanic]
> Patrol-Lieutenant sounds alarm round 2 if party boards toward the wheel. Harbour response:
> 6 rounds. Running viable; Crown Governor would accept surrender before cannon fire.
```

**Bad:**
```
> [!warning] Mortis Mark
> Disadvantage on all Wisdom saving throws...
```

Fix: `[!mechanic] Mortis Mark` as title. Rule in the body, no prose.

---

### `[!check]`

Format: `[!check] Skill (or Skill/Skill) — Brief label`

Body uses this structure — keep each line tight:
- **DC range:** low–mid–high based on relevant factors (familiarity, conditions, visibility)
- **Crit fail** (≤5 below DC or nat 1): what the character gets wrong or what goes bad
- **Fail** (miss DC): what they don't learn or what doesn't happen
- **Near miss** (1–2 below DC): partial info or partial success — optional but useful
- **Success** (meet DC): what they learn or gain
- **Crit success** (≥5 above DC or nat 20): additional detail, advantage downstream, or DM option

**Good:**
```
> [!check] Nature/Survival — Identify the creature
> DC 10 open water, DC 14 poor visibility, DC 18 night/storm.
> Crit fail: misidentifies as aggressive — party may act on bad intel.
> Fail: real species, no useful details.
> Success: breathing cycle and size mark it non-predatory.
> Crit success: same species as Perrin's dream. Perrin recognizes it on sight — no roll needed.
```

**Bad:**
```
> [!skillcheck]
> Players who succeed on a DC 12 Nature check might be able to identify this creature as
> something real rather than something dangerous.
```

Fix: rename to `[!check]`. Add skill and contextual DC range to the title line. Convert
outcomes to the tiered structure.

---

## Conversion Table

Correct these automatically when encountered:

| Found | Convert to | Notes |
|---|---|---|
| `[!READ-ALOUD]` | `[!read-aloud]` | Normalize case only |
| `[!secret]` | `[!dm]` or prose | DM knows everything. If body is an actionable note, use `[!dm]`. If it's lore context, strip callout and leave prose. |
| `[!note]` | `[!dm]` or prose | If it tells the DM to do something or watch for something, use `[!dm]`. If it's a stub or plain information, strip to prose. |
| `[!warning]` | `[!mechanic]`, `[!dm]`, or prose | Mortis marks and conditions → `[!mechanic]`. Timing notes → `[!dm]`. Metadata ("Superseded") → strip to prose inline. |
| `[!skillcheck]` | `[!check]` | Rename. Reformat title to `Skill — Label` if missing. |
| `[!appearance]` | `[!read-aloud]` or prose | If read at the table, use `[!read-aloud]`. If DM reference only, strip to prose. |
| `[!quote]` | `[!read-aloud]` or prose | Same judgment as appearance. |
| `[!DM]` | `[!dm]` | Normalize case only |

---

## `[!secret]` Is Always Wrong

Nothing should be secret to the DM. Visibility is controlled by `publish: false` / `publish: true`
in frontmatter — not by callout type. A `[!secret]` callout means the original author was
thinking about what players can see, which is the wrong frame for a DM reference file.

When you encounter `[!secret]`:
- If it's telling the DM what to do or not do → `[!dm]`
- If it's GM-only lore, discoverable plot, or NPC hidden knowledge → strip the callout, leave
  the text as prose under a heading like `## Hidden Context` or `## What the DM Knows`
- Never preserve `[!secret]`

---

## Per-Domain Defaults

| File type | Expected types |
|---|---|
| Session run guide | `[!read-aloud]`, `[!dm]` |
| Scene file | `[!read-aloud]`, `[!dm]`, `[!check]`, `[!mechanic]` |
| Situation file | `[!read-aloud]`, `[!dm]`, `[!mechanic]` |
| Ship page | `[!read-aloud]`, `[!mechanic]`, `[!dm]` (sparingly) |
| NPC page | `[!dm]`, `[!mechanic]` (Mortis/conditions) |
| Location page | `[!read-aloud]`, `[!dm]` |
| PC sheet | `[!mechanic]`, `[!dm]` (timing notes) |

---

## Quality Gate

Before finalizing any callout:

- One job per callout — if it's doing two things, split it
- `[!read-aloud]`: reads clean aloud, no conditional framing, player-facing prose mode applied
- `[!dm]`: starts with a verb or noun, ≤3 sentences, no hedging language
- `[!mechanic]`: trigger stated first, consequence follows, no prose padding
- `[!check]`: skill named, contextual DC range given, tiered outcomes present (at minimum fail/success/crit success)
- `[!secret]` is gone

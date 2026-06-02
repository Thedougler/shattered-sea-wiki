---
name: ttrpg-visual-aids
description: >
  Use when generating, placing, or embedding visual aids for the Shattered Sea campaign.
  Triggers: "generate art for", "create a visual", "make a scene image", "add a portrait",
  "illustrate this", "banner for", "combat art", any session prep or recap needing
  illustrations, any entity page needing a portrait or banner, any question about where
  to store generated images or how to embed them in wiki pages. Also use when building
  image prompts for the campaign.
---

# Visual Aids

## Before Generating

Read `wiki/system/art-style.md` before every generation task. It defines the campaign's
visual style, negative constraints, category overrides, and character appearance references.
Apply its directives to every prompt — no exceptions, no "I'll use a similar style."

If `wiki/system/art-style.md` does not exist, stop and tell the DM.

## Prompt Construction

Build every generation prompt by combining — in this order:

1. **Base style** — `style_prompt` from art-style.md
2. **Category modifiers** — aspect ratio and rules from the matching category override
3. **Scene-specific content** — composition, characters, action, lighting, environment
4. **Character descriptions** — pulled verbatim from wiki pages, never invented
5. **Negative constraints** — `negative` field from art-style.md, appended at the end

Read every character's wiki page before including them. If a character lacks sufficient
visual description on their page, ask the DM — do not approximate.

## Storage Paths

All generated images go inside `wiki/assets/`. Create subdirectories as needed.

| Category | Path | Naming Pattern | Slideshow Folder |
|---|---|---|---|
| Portraits | `wiki/assets/portraits/` | `Entity-Name.webp` | Character gallery |
| Banners | `wiki/assets/banners/` | `Entity-Name.webp` | — |
| Session art | `wiki/assets/sessions/session-NN/` | `NN-description.webp` | Per-session slideshow |
| Scene art | `wiki/assets/scenes/location-slug/` | `description.webp` | Per-location slideshow |
| Combat art | `wiki/assets/combat/encounter-slug/` | `description.webp` | Per-encounter slideshow |
| Maps | `wiki/assets/maps/` | `area-name.webp` | — |
| Handouts | `wiki/assets/handouts/` | `handout-name.webp` | — |

**Naming rules:**
- Kebab-case, lowercase: `kyzil-reunion.webp`, `market-ambush.webp`
- Portraits and banners use the entity's display name: `Master-Kyzil.webp`, `Calveno.webp`
- Session folders use zero-padded numbers: `session-01/`, `session-04/`
- Location slugs match the wiki filename: `calveno`, `la-vasca`, `le-paludi`
- Prefer `.webp` for all art. Use `.png` only for maps or handouts needing lossless detail.

**Why this structure:** Each subfolder is a self-contained slideshow source. Point OBS,
a media player, or Obsidian's image gallery at any folder to get a thematic slideshow
(all Calveno scenes, all Session 04 art, all combat images for an encounter).

## Embedding in Markdown

**Syntax:** Obsidian wikilink embed. Path from vault root.

```markdown
![[wiki/assets/portraits/Master-Kyzil.webp|Full generation prompt used as alt text]]
```

**Alt text is the prompt.** Write the full generation prompt as alt text — this is the
project convention. It serves as both accessibility text and a regeneration record.
Long embed lines are expected and intentional — do not truncate or summarize the prompt.

**Width control** (optional, only when the default is too large):

```markdown
![[wiki/assets/portraits/Master-Kyzil.webp|Full prompt text|400]]
```

### Placement Rules

| Document type | Where to embed | Limit |
|---|---|---|
| NPC page | After Roleplay Concept + Quote, before Lore Sheet | 1 portrait |
| Location page | After opening `[!read-aloud]` callout | 1 banner or establishing shot |
| Session recap | Between narrative sections, at the scene break it illustrates | 1 per major scene beat |
| Run guide | Inline with the scene it supports | 1 per scene |
| Encounter page | Top, before tactical details | 1 scene-setter |

**Never:**
- Embed images inside callouts
- Place more than one image between consecutive prose paragraphs
- Embed without a blank line above and below the embed line

## When to Generate

**Do generate** when:
- Prepping a session — scene art for key beats in the run guide
- Creating or expanding an NPC — portrait
- Creating or expanding a location — establishing shot or banner
- Writing a session recap — scene illustration for each major beat
- DM explicitly requests art

**Do not generate** when:
- Doing structural edits (frontmatter fixes, wikilink repairs, lint)
- The page already has appropriate art for that element
- The entity is minor and won't appear at the table

## Image Generation

**REQUIRED SUB-SKILL:** Invoke `openrouter-image-gen` to generate images.

After constructing the prompt per the Prompt Construction rules above:

1. Determine the output path from the Storage Paths table and naming rules
2. Determine the aspect ratio from the Category Overrides in `art-style.md` (e.g. `3:4` for portraits, `16:9` for scenes, `3:1` for banners)
3. Run the generation script:

```bash
python3 .claude/skills/openrouter-image-gen/generate-image.py \
  "your constructed prompt here" \
  --aspect 16:9 \
  --output wiki/assets/sessions/session-04/kyzil-reunion.webp
```

4. Send the image to the user with `SendUserFile` so they can see it in chat
5. Use the Read tool on the output path to verify the result yourself
6. If the result is poor, refine the prompt and regenerate
7. Embed per the Embedding in Markdown rules above

For Gemini models (the default), write prompts as natural-language scene descriptions
rather than keyword lists. See `openrouter-image-gen/references/prompting-best-practices.md`
for model-specific guidance.

### Fulfilling `[!visual-aid]` Callouts

When you encounter an existing `[!visual-aid]` callout, use its prompt text to generate
the image via the workflow above, then replace the callout with a standard embed.

### Fallback

If generation fails (no API key, API error, insufficient credits), write the full
prompt as a `> [!visual-aid]` callout where the image would go:

```markdown
> [!visual-aid] Scene: Kyzil Reunion
> Archer-style adult animated illustration, widescreen cinematic scene, ...
> [full prompt incorporating all art-style.md directives]
```

A capable agent or the DM replaces this callout with an embed later.

## Legacy Assets

Older images live in `.raw/assets/` (subdirectories: `session-art/`, `banners/`,
`portraits/`, `maps/`, `handouts/`). These are referenced in existing pages as
`![[raw/assets/...]]`. Do not move legacy files — new images go in `wiki/assets/`.

When generating new art for a scene that already has a legacy embed, **replace** the
legacy embed with the new one. Do not keep both — the placement rules limit each
slot to one image.

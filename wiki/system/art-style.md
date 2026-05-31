---
type: system
subtype: system-file
campaign: shattered-sea
status: active
audience: dm
publish: false
summary: Visual style guide for AI-generated campaign art — agents read this before every image generation task
created: 2026-05-30
updated: 2026-05-31
tags: []
sources: []
system_role: style-guide
token_profile: on-demand
mandatory_for: [ttrpg-visual-aids]
update_trigger: "when the DM changes art style preferences"
---

# Art Style Guide

Agents generating visual aids for the Shattered Sea **must** apply these directives.
Edit this file to change the campaign's visual identity globally.

---

## Base Style

All generated images use this foundation unless a category override says otherwise.

**style_prompt:** Archer-style adult animated illustration, clean vector-like linework, strong ink contours, cel-shaded lighting, poster-composition staging, expressive grounded faces, saturated adventure palette

**aspect_ratio:** 16:9 widescreen cinematic

**negative:** no text, no watermarks, no logos, no gore, no photorealism, no anime/chibi, no pixel art, no stock-photo aesthetic

### Style Definition

The campaign's visual identity follows the reference style shown in the Archer
season and poster images: adult animated adventure art with crisp comic-book
draftsmanship, clean digital color, and cinematic ensemble staging. It should
look like polished television animation adapted into a dramatic TTRPG still,
not painterly fantasy illustration.

Use these traits consistently:

- Thick-to-medium black outlines with confident contour shapes and smaller interior line detail for faces, clothing folds, hair, and equipment
- Cel-shaded forms with hard shadow edges, limited soft blending, and readable highlights on skin, fabric, metal, and wet surfaces
- Expressive faces with clear eyes, arched brows, distinct noses, and grounded adult proportions; avoid cute, simplified, or exaggerated cartoon anatomy
- Graphic poster composition: strong foreground subject, readable silhouettes, diagonal action lines, and supporting figures placed to clarify the scene
- Saturated but controlled color: teal seas, warm sunsets, crisp whites, deep blacks, rich reds, and selective bright accents rather than muddy realism
- Backgrounds rendered as stylized sets with enough detail to identify place, era, weather, and tactical layout without stealing focus from the action
- Adventure-serial mood: competent, wry, dangerous, and cinematic; no slapstick distortion unless the scene itself calls for comedy

Avoid these drift points:

- Painterly brush texture, oil-paint fantasy rendering, watercolor, or loose concept-art strokes
- Photorealistic faces, 3D-rendered lighting, plastic skin, or stock-photo composition
- Anime, chibi, manga speed-line language, superhero muscle exaggeration, or children's-cartoon softness
- Overly grim dark fantasy palettes that bury linework and facial expression

---

## Category Overrides

### Portraits

- Aspect ratio: 3:4 (vertical)
- Character fills the frame from chest up
- Neutral or characteristic expression — never mid-action
- Background suggests their environment but stays muted
- Lighting: dramatic side-light or environmental match

### Banners

- Aspect ratio: 3:1 or wider (panoramic)
- Establishing shot — location or concept, not tight character focus
- More atmospheric, less detailed than scene art
- Used as page headers for locations, factions, concepts

### Scene Art

- Aspect ratio: 16:9 (widescreen)
- Environmental storytelling — setting carries as much weight as characters
- Lighting matches time of day and mood of the scene
- When characters are present, show them in context, not isolated

### Combat Art

- Same as scene art
- Emphasize spatial relationships and tactical positions
- Show the environment the fight takes place in
- Action mid-beat, not posed

### Maps

- Override: does **not** use Archer style
- Top-down or slight isometric perspective
- Labeled if player-facing; unlabeled if DM reference
- Aged parchment or clean cartographic aesthetic — DM's choice

---

## Character Rendering

When including PCs or named NPCs, their visual description **must** come from their
wiki page. Never invent or approximate character appearances.

If the wiki page lacks a physical description sufficient for generation, stop and ask
the DM before generating.

### Party Reference

| PC | Key Visuals |
|---|---|
| Crissdalynn Khinriss | Dark blue-black crow aarakocra monk, folded wings, talons, geometric leatherwork, chart satchel |
| Perrin Black-Jaw | Very small (3 ft) black-and-white fancy-rat Rattkin sailor, olive-drab hooded cloak, cream shirt, bodhran drum, long pink tail, oversized longsword |
| Jean-Claude Tabarnack | Three-foot lean humanoid poison dart frog (electric-blue skin, large black underside patches, geometric black bands), red beret, false black moustache, ranger harness, shortbow and quiver |
| Delmar Fisk | Sandy red hair in messy topknot, thick sandy-red beard and curled moustache with grey edges, salt-stiff scarlet admiral coat with gold epaulettes, musket |

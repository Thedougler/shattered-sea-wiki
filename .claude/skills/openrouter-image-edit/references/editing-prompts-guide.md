# Image Editing Prompts Guide

## How Editing Differs from Generation

When generating, you describe the entire image from scratch. When editing, the image already exists — your prompt describes **what to change**, not the whole scene. The model sees the original and applies your instruction to it.

**Generation prompt:** "a scarred half-orc berserker with a braided beard, standing in a tavern, oil painting"
**Edit prompt:** "add a long scar running diagonally across the left cheek"

## Prompt Structure for Edits

```
[action] + [target region] + [desired result] + [style anchor]
```

**Example:**
> Change the background from a plain wall to a stormy sea with crashing waves, maintaining the existing cel-shaded illustration style

### The Four Components

**Action** — what operation to perform:
- Add / place / insert — put something new in the image
- Remove / delete / erase — take something away
- Change / replace / swap — substitute one thing for another
- Adjust / shift / modify — alter a property (color, lighting, size)

**Target region** — where in the image to apply the change:
- Be spatially specific: "the character's left hand," "the upper-right corner," "the sky behind the ship"
- Use relative positioning: "above the castle," "between the two figures," "along the bottom edge"
- Reference existing elements: "the sword the figure is holding," "the door in the background"

**Desired result** — what it should look like after the edit:
- Describe the end state, not the process
- Be concrete: "a deep orange sunset with purple clouds" not "make the sky prettier"

**Style anchor** — keep visual consistency:
- "Maintain the existing art style"
- "In the same watercolor medium as the original"
- "Keep the cel-shaded look and saturated color palette"

## Common Edit Types

### Adding Elements

```
Add a glowing magical aura around the character's raised hands, soft blue-white light,
maintaining the existing oil painting style

Place a compass rose in the bottom-right corner, ornate brass design with cardinal
directions labeled, matching the parchment map style

Insert a small black cat sitting on the tavern windowsill in the background
```

**Tips:**
- Specify size relative to existing elements ("about half the height of the door")
- Describe how the new element interacts with lighting ("lit by the same warm firelight")
- The model handles blending — you describe what, it figures out how

### Removing Elements

```
Remove the text overlay from the image, fill the area with the surrounding background

Erase the watermark in the bottom-right corner

Remove the third figure on the left, extend the stone wall behind where they were standing
```

**Tips:**
- Tell the model what to fill the gap with — otherwise it guesses
- Simple removals against uniform backgrounds work best
- Complex removals (figure from a crowd) may need Nano Banana Pro

### Changing Colors and Lighting

```
Shift the lighting from midday sun to golden hour — warm amber tones, long shadows
cast to the right, everything slightly more saturated

Change the character's cloak from blue to deep crimson, keep the same fabric texture
and shadow patterns

Make the scene darker and moodier — reduce brightness by half, add volumetric fog,
cold blue-gray color grading
```

**Tips:**
- Lighting changes affect the entire image — be specific about the mood you want
- Color changes to specific objects work well when you name the object precisely
- "Warmer" and "cooler" are understood but vague — specify the color temperature

### Background Replacement

```
Replace the plain gray background with a sunset over a calm harbor, sailing ships
in the distance, matching the painterly style of the character portrait

Change the background to a dense forest interior with dappled sunlight filtering
through the canopy
```

**Tips:**
- Always include a style anchor — background replacements are where style drift is worst
- Describe depth: "distant mountains" vs "close underbrush" affects the composition
- The model preserves the foreground subject automatically

### Style Transfer

```
Redraw this photograph in the style of a watercolor painting with visible brushstrokes
and soft edges

Convert this to cel-shaded animation style — bold outlines, flat color fills,
limited shadow palette like Archer or Into the Spider-Verse
```

**Tips:**
- Style transfer changes the entire image — there's no "change just this part's style"
- Name specific art styles or reference artists/shows for consistency
- The output quality depends heavily on how well the model knows the target style

### Composition and Framing

```
Zoom out to show more of the environment below the character's feet — extend the
image downward with cobblestone street and market stalls

Crop tighter on the character's face, turning this into a close-up portrait with
the background softly blurred
```

**Tips:**
- Outpainting (extending the image) works but quality varies — Nano Banana Pro is best for this
- Reframing changes are better handled by regenerating with a new prompt than editing

## Gemini-Specific Editing Tips

The default Nano Banana model (`google/gemini-2.5-flash-image`) has these editing characteristics:

**Strengths:**
- Excellent at color and lighting adjustments
- Good at adding small elements to existing scenes
- Handles style anchoring well when explicitly told
- Understands spatial descriptions ("upper left," "behind the figure")

**Limitations:**
- No inpainting masks — the model decides what to modify based on your text alone
- Complex multi-region edits may produce inconsistent results — do them one at a time
- Text rendering in edits is poor (same as generation)
- May subtly alter areas you didn't ask it to change — check the full image, not just the edited region

**Nano Banana Pro** (`google/gemini-3-pro-image-preview`) adds:
- Localized edits with better precision
- Lighting and focus adjustments
- Camera transform simulation (slight angle changes)
- Higher fidelity preservation of unedited regions

## Iterative Editing Strategy

When an edit doesn't land on the first try:

1. **Simplify.** If you asked for three changes, ask for one.
2. **Be more spatial.** "The left side of the image" → "the character's left hand, which is raised above their head"
3. **Describe the end state.** Instead of "make it look better," say "the lighting should be warm golden hour with long shadows to the right"
4. **Add a style anchor.** If the style drifted, explicitly state "maintain the original [style] throughout"
5. **Try a different model.** If Nano Banana can't handle a precise edit, try Nano Banana Pro

## What Doesn't Work Well

| Desire | Reality |
|--------|---------|
| Pixel-perfect placement | Models approximate — ±10% positional accuracy |
| "Don't change anything else" | Models may subtly alter unedited regions |
| Multiple unrelated edits at once | Do them sequentially — one edit per pass |
| Adding readable text to images | AI text rendering is poor; composite text afterward |
| Precise color matching (#FF5733) | Describe colors naturally ("warm orange-red") |
| Undo just one part of a previous edit | Re-edit from the pre-edit version in git history |

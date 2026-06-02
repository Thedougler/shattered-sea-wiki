# Image Prompting Best Practices

## Prompt Structure

Build prompts in layers — each layer adds specificity:

```
[subject] + [action/pose] + [setting/background] + [style/medium] + [lighting/mood] + [camera/framing]
```

**Example:**
> an elderly dwarf blacksmith hammering a glowing blade, cluttered stone forge with hanging tools, oil painting style, warm firelight from below, close-up portrait framing

## Subject

Be specific. Vague subjects produce generic results.

| Weak | Strong |
|------|--------|
| "a warrior" | "a scarred half-orc berserker with a braided beard" |
| "a castle" | "a crumbling seaside fortress with barnacle-covered walls" |
| "a ship" | "a three-masted brigantine with patched black sails" |

## Style & Medium Keywords

These steer the visual treatment more than any other element.

**Traditional art:** oil painting, watercolor, ink wash, charcoal sketch, woodcut print, gouache, fresco
**Digital art:** digital painting, concept art, matte painting, 3D render, cel-shaded
**Photography-like:** photorealistic, DSLR photograph, macro photography, aerial drone shot
**Stylized:** art nouveau, ukiyo-e, pixel art, stained glass, tarot card illustration
**Artist references:** "in the style of [public domain artist]" — e.g. Alphonse Mucha, Hokusai, John Singer Sargent

## Lighting & Atmosphere

Lighting sells the mood. Always specify it.

**Warm:** golden hour, candlelight, firelight, warm lantern glow, amber sunset
**Cool:** moonlight, overcast, blue hour, foggy, underwater caustics
**Dramatic:** chiaroscuro, rim lighting, silhouette against bright sky, single harsh spotlight
**Neutral:** soft diffused light, overcast even lighting, studio lighting

## Composition & Camera

**Framing:** extreme close-up, portrait, medium shot, wide establishing shot, bird's-eye view, worm's-eye view
**Depth:** shallow depth of field, bokeh background, tilt-shift, deep focus
**Angle:** low angle (heroic), high angle (vulnerable), dutch angle (unease), straight-on (neutral)

## TTRPG-Specific Tips

**Character portraits:**
- Include species/ancestry, distinguishing features, gear, expression
- Specify background (transparent, tavern interior, battlefield)
- "Character portrait" or "bust portrait" anchors the framing

**Battle scenes:**
- Name the terrain and weather
- Specify scale — "two figures locked in combat" vs "a massive army clashing"
- Dynamic poses: "mid-swing," "dodging," "casting with hands raised"

**Maps & locations:**
- Specify perspective: "top-down dungeon map," "isometric town," "cross-section"
- "Annotated" or "labeled" rarely works — generate the map art, label it separately
- For world maps: "fantasy cartography style, parchment texture, compass rose"

**Items & artifacts:**
- "Isolated on a dark background" or "displayed on velvet cloth"
- Describe material, glow effects, runes, wear/patina
- "Prop photograph" or "museum display" for clean presentation

## Quality Boosters

Append these when you want higher fidelity:

- `highly detailed`
- `4k` / `8k resolution`
- `intricate`
- `masterwork`
- `award-winning`

## What to Avoid

**Overloading:** More than ~60 words and models start dropping details. Front-load the important elements.

**Negation:** "no text," "without wings" — most models handle negative prompts poorly through the main prompt.

**Ambiguity:** "cool scene" means nothing. "A frost giant standing knee-deep in a frozen lake, aurora borealis overhead, cinematic wide shot" means everything.

**Text in images:** Most AI models render text poorly. Flux models are an exception — they handle text reasonably well. For other models, generate the image clean and composite text afterward.

## Model-Specific Notes

### Gemini "Nano Banana" Models (Default)

The Gemini image generation family on OpenRouter:

| Model ID | Codename | Notes |
|----------|----------|-------|
| `google/gemini-2.5-flash-image` | Nano Banana | Fast, cheap, good quality — the default |
| `google/gemini-3.1-flash-image-preview` | Nano Banana 2 | Newer, slightly pricier |
| `google/gemini-3-pro-image-preview` | Nano Banana Pro | Highest quality Gemini, most expensive |

**Prompting tips for Gemini image models:**

- **Use natural language, not keyword lists.** Gemini understands full sentences and scene descriptions better than comma-separated tags. Write "a weathered pirate captain standing at the helm of his ship during a storm" not "pirate, captain, helm, ship, storm, weathered."
- **Be conversational about what you want.** You can say things like "Make the lighting dramatic with the storm clouds backlit by lightning" — Gemini parses intent well.
- **Scene descriptions work better than art direction.** Instead of naming specific techniques ("use chiaroscuro lighting with a 3/4 view"), describe the scene as you see it ("the figure is lit from below by a lantern, casting long shadows up the walls").
- **Style references stick.** "Archer-style adult animated illustration" or "in the style of a Moebius comic" — Gemini follows these consistently without needing reinforcement keywords.
- **Negative prompts go in the main text.** Gemini has no separate negative prompt field. Phrase exclusions as "do not include text or watermarks" rather than listing negatives.
- **Spatial relationships are a strength.** Gemini handles "the figure on the left is taller than the one on the right" and multi-character compositions better than many models.
- **Aspect ratio via `--aspect`.** Gemini respects the `image_config.aspect_ratio` parameter well. Use `16:9` for cinematic scenes, `3:4` for portraits, `3:1` for banners.
- **Keep prompts under ~80 words.** Gemini handles slightly longer prompts than Stable Diffusion but still loses details past this point. Front-load the most important elements.

### GPT-5 Image (`openai/gpt-5-image`, `openai/gpt-5-image-mini`)

- Natural language prompts, may rewrite your prompt internally
- High quality but more expensive

### Flux (`black-forest-labs/flux.2-pro`, `flux.2-max`)

- Very good at rendering text in images
- Natural language prompts work well
- Megapixel-based pricing

### Recraft (`recraft/recraft-v4.1`)

- Supports additional `style` parameter in image_config
- Good for consistent style across multiple images
- Flat per-image pricing

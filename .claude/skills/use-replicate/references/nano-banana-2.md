# Nano Banana 2 — Prompting & Usage Reference

Google's fastest image generation model (Gemini 3.1 Flash Image). Pro-level quality at Flash-level speed. Combines generation, editing, multi-image fusion, text rendering, and real-time web grounding in one model.

## When to Use Nano Banana 2

| Scenario | Use nano-banana? | Why |
|---|---|---|
| Fast iteration / drafts | **Yes — default choice** | Fastest model, cheapest per-image |
| Product photography with text on packaging | **Yes** | Strong text rendering + compositional control |
| Multi-image reference (style transfer, character consistency) | **Yes — up to 14 refs** | Best multi-image fusion of any model |
| Conversational editing (iterative refinement) | **Yes** | Native edit-in-place without re-prompting the whole scene |
| SVG vector output | No | Use recraft-svg |
| Highest possible photorealism (skin/hair/fabric) | Maybe | Try first; fall back to imagen-ultra if insufficient |
| Extreme text precision (menus, data tables) | Test first | Strong but ideogram may beat it on dense text |

## CLI Usage

```bash
# Basic generation
gen-image.mjs "prompt" --model nano-banana

# With aspect ratio and resolution
gen-image.mjs "prompt" --model nano-banana --aspect 16:9 --size 4K

# Save to file
gen-image.mjs "prompt" --model nano-banana --save generated-images/product.jpg

# With format override
gen-image.mjs "prompt" --model nano-banana --format png
```

## Parameters

| Param | CLI Flag | Values | Default | Notes |
|---|---|---|---|---|
| `prompt` | positional | string | required | Natural language description |
| `aspect_ratio` | `--aspect` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`, `match_input_image` | `1:1` | Extreme ratios (1:4, 4:1, 1:8, 8:1) are NB2-exclusive |
| `output_resolution` | `--size` | `512px`, `1K`, `2K`, `4K` | `1K` | 512px for cheap batch iteration |
| `output_format` | `--format` | `jpg`, `png` | `jpg` | No webp — use jpg for photos, png for transparency |
| `image` | via SDK | file/URL | — | Input image for editing or reference (up to 14) |

**Note:** `output_resolution` maps to the `--size` flag in gen-image.mjs. The script passes `size` through as an input parameter.

## Prompt Structure

### Formula

```
[Subject + specific details] + [Action/state] + [Setting/context] + [Composition/camera] + [Style/lighting]
```

**Start with a strong opening clause.** The model prioritizes the first clause — put the subject and dominant action/state first.

### Rules

1. **Be specific and literal** — concrete details on subject, material, color, texture, spatial layout
2. **Use positive framing** — describe what you want, not what to avoid ("empty street" not "no cars")
3. **Control the camera** — use photographic/cinematic terms (low angle, 85mm, shallow DoF)
4. **Specify materials** — "navy blue tweed" not "suit jacket"; "kraft brown matte box" not "box"
5. **Include lighting** — "three-point softbox setup", "golden hour backlight", "chiaroscuro"

### Text Rendering

Nano Banana 2 has strong text rendering — it CAN render readable text, unlike FLUX.

**Rules for text in images:**
- Wrap exact text in **quotation marks**: `box reads "ORDURE & CO" in gold serif font`
- Specify font style: bold sans-serif, elegant serif, modern geometric, hand-lettered
- Define placement: centered, bottom-left, integrated into the label
- Keep text concise: **3–5 words maximum** for reliable rendering
- For multilingual text: write prompt in English, specify target language for text output

**Example — product label:**
```
A premium kraft brown gift box with a round gold wax seal on the lid reading "ORDURE & CO" in elegant serif capitals, cream crinkled tissue paper inside, warm studio lighting, overhead 45-degree angle, product photography
```

### Multi-Image Reference

Upload up to **14 reference images** and assign roles explicitly:

```
Using the attached product photo as the subject and the attached mood board as the style reference,
place the gift box on a marble surface with warm editorial lighting, shot on medium-format film
```

**Role types for references:**
- Identity/Character — facial features, product appearance
- Pose/Composition — positioning, layout
- Style/Aesthetic — color palette, treatment
- Lighting/Atmosphere — direction, mood
- Environment/Background — setting, surface

### Conversational Editing

After generating, refine without re-prompting the whole scene:

```
"Keep everything but change the background to dark charcoal"
"Move the wax seal to the center of the lid"
"Make the tissue paper more crinkled and voluminous"
```

**Editing rules:**
- Be explicit about what stays the same
- Use positive framing ("add X" not "remove the absence of X")
- Reference specific parts of the image
- Use semantic masking: describe the region to edit in natural language

## Example Prompts

### Product Photography (Ordure house style)
```
An open kraft brown gift box with a matte finish, cream crinkled tissue paper spilling over the edges, a specimen of dehydrated horse dung centered inside on a bed of wood shavings, the kraft lid placed beside it at a slight angle with a round gold wax seal embossed with an elephant silhouette, warm editorial studio lighting with soft shadows, light grey-white seamless background, shot overhead at 45 degrees on medium-format film, product photography, rich textures, 4K
```

### Fashion Editorial
```
A striking fashion model wearing a tailored brown dress, sleek boots, and holding a structured handbag, posing with a confident statuesque stance slightly turned, deep cherry red studio backdrop, medium-full shot center-framed, fashion magazine style editorial, shot on medium-format analog film, pronounced grain, high saturation, cinematic lighting effect
```

### Text-Heavy Marketing
```
A high-end glossy commercial shot of a minimalist face moisturizer jar on a warm studio background with soft radiant lighting, next to the product render three lines of text: top line the word "GLOW" in a flowing elegant Brush Script font, middle line "10% OFF" in heavy blocky Impact font, bottom line "Your First Order" in thin minimalist Century Gothic font
```

### Extreme Aspect Ratio (Banner)
```
Create a 4-panel horizontal comic strip (aspect ratio 4:1), the story follows a mischievous cat trying to steal a fish from a kitchen counter, warm kitchen lighting, cartoon illustration style
```

### Film & Texture Control
```
A child's crayon drawing on white lined notebook paper of maple taffy on snow, chunky wax-crayon strokes, wobbly outlines, bright bold colors that messily overflow the lines
```

## Cost Optimization

- **Batch at 512px first** — generate many variations cheaply, then upscale the winner to 2K/4K
- **Conversational editing** saves re-generation cost — refine instead of re-rolling
- **Multi-image fusion** can replace multi-step workflows (separate generation + compositing)

## Thinking Mode

**Keep OFF by default** for standard image generation. Enable only when:
- Model produces nonsensical results requiring reasoning support
- Generating highly complex infographics or data visualizations
- Combining complex image grounding with spatial reasoning

## Image Grounding (Web Search)

Nano Banana 2 can search the web for visual references to produce accurate depictions of real-world subjects.

**Good for:** specific buildings, landmarks, animal species, plant varieties, product designs
**Cannot search for:** people (privacy restriction)

```
Generate a cinematic golden-hour photograph of the main historical church in Voiron, France, ensure the architectural details, spire, surrounding square, and mountain landscape are accurate to reality
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Used `--format webp` | NB2 outputs jpg or png only — use `--format jpg` or `--format png` |
| Text not rendering | Wrap exact text in quotation marks; keep to 3–5 words; specify font style |
| Assumed FLUX prompt style | NB2 handles natural language well but prioritizes the first clause — lead with the subject |
| Ignored `--size` for production | Default is 1K — set `--size 4K` for production assets |
| Re-rolled instead of editing | Use conversational editing to refine — faster and cheaper |
| Sent 15+ reference images | Max 14 reference images per prompt |
| Used euphemisms in prompt | Diffusion prompts need literal descriptions — "elephant dung" not "specimen" |

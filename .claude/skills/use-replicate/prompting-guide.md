# Prompting Guide for Replicate Models

How to get best results from key model families.

## Nano Banana 2 (google/nano-banana-2)

Google's fastest image model (Gemini 3.1 Flash Image). Pro-level quality, text rendering, multi-image fusion, conversational editing.

### Prompt Structure

**Pattern**: `[Subject + details] + [Action/state] + [Setting] + [Composition/camera] + [Style/lighting]`

**Lead with the subject** — the model prioritizes the first clause.

```
An open kraft brown gift box with a matte finish, cream crinkled tissue paper spilling over the edges, 
a dehydrated horse dung specimen centered inside on wood shavings, the kraft lid placed beside it 
with a round gold wax seal, warm editorial studio lighting, light grey-white background, 
overhead 45-degree angle, product photography, rich textures, 4K
```

### Key Parameters

| Param | Values | Default | Notes |
|---|---|---|---|
| `prompt` | string | required | Natural language; lead with subject |
| `aspect_ratio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1` | `1:1` | Extreme ratios (1:4, 4:1, 1:8, 8:1) are NB2-exclusive |
| `output_resolution` | `512px`, `1K`, `2K`, `4K` | `1K` | 512px for cheap batch iteration |
| `output_format` | `jpg`, `png` | `jpg` | No webp support |
| `image` | file/URL | — | Up to 14 reference images |

### Text Rendering

NB2 renders readable text (unlike FLUX). Rules:
- Wrap exact text in **quotation marks**: `the label reads "PREMIUM BLEND"`
- Specify font style: "bold sans-serif", "elegant serif capitals", "hand-lettered"
- Define placement: "centered at top", "on the label", "bottom-left"
- Keep text to **3–5 words** for reliable rendering
- Multilingual: write prompt in English, specify target language for output text

```
A poster with the title "COSMIC DRIFT" in bold retro font, deep space background, astronaut floating
```

### Multi-Image Reference (Up to 14)

Assign explicit roles to reference images:

```
Using the attached product photo as the subject and the attached mood board as the style reference,
place the gift box on a marble surface with warm editorial lighting, shot on medium-format film
```

Roles: identity/character, pose/composition, style/aesthetic, lighting/atmosphere, environment/background.

### Conversational Editing

Refine a generated image without re-prompting from scratch:
- `"Keep everything but change the background to dark charcoal"`
- `"Move the wax seal to the center of the lid"`
- `"Make the lighting warmer and more golden"`

Be explicit about what stays the same. Use positive framing.

### Image Grounding (Web Search)

NB2 can search the web for visual accuracy on real-world subjects:
- Specific buildings, landmarks, churches, bridges
- Animal species, plant varieties, insects
- **Cannot search for people** (privacy restriction)

```
A cinematic golden-hour photograph of the main historical church in Voiron, France,
architectural details accurate to reality, mountain landscape in background
```

### Cost Optimization

- **Batch at 512px** — generate many variations, upscale the winner to 2K/4K
- **Edit, don't re-roll** — conversational editing is cheaper than regeneration
- **Multi-image fusion** replaces separate generation + compositing steps

### Tips
- Lead with subject in the first clause (model prioritizes it)
- Use positive framing ("empty" not "no people")
- Specify materials, textures, surfaces — "kraft brown matte" not "brown box"
- Include camera/lens terms: "85mm f/1.4", "overhead 45°", "medium-full shot"
- Include lighting: "three-point softbox", "golden hour backlight", "chiaroscuro"
- Film stock for mood: "shot on medium-format analog film, pronounced grain"
- Keep thinking mode OFF unless generating complex infographics or spatial reasoning tasks

### NB2 vs Other Models

| Need | Best choice | Why |
|---|---|---|
| Fast iteration | **nano-banana** | Fastest, cheapest, good quality |
| Text on packaging | **nano-banana** or ideogram | Both handle text well; NB2 is faster |
| Multi-image fusion | **nano-banana** | Only model with 14 reference image support |
| Iterative editing | **nano-banana** | Native conversational editing |
| Highest photorealism | imagen-ultra | More detail on skin/hair/fabric |
| SVG vector | recraft-svg | NB2 outputs raster only |
| Budget draft | flux-schnell | Slightly cheaper per-image |

---

## FLUX Image Models (flux-schnell, flux-2-pro, flux-2-max)

### Prompt Structure
FLUX follows natural language well. No need for comma-separated tag lists like SD.

**Pattern**: `[subject], [style/medium], [lighting], [composition], [quality modifiers]`

```
a golden retriever sitting in a cafe, watercolor painting, warm afternoon light, close-up portrait, highly detailed
```

### Key Parameters

| Param | Values | Notes |
|---|---|---|
| `prompt` | string | The description |
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` | Default 1:1 |
| `output_format` | `webp`, `jpg`, `png` | webp default, smallest |
| `output_quality` | 1-100 | For webp/jpg compression |
| `num_outputs` | 1-4 | Multiple images per run |
| `seed` | integer | Reproducibility |

### FLUX Tips
- Be descriptive and specific — FLUX handles long prompts well
- Include lighting direction: "dramatic side lighting", "golden hour backlight"
- Include camera details: "shot on 85mm f/1.4", "wide angle", "macro"
- Medium matters: "oil painting", "digital art", "product photography", "pencil sketch"
- Negative concepts: describe what you want, not what you don't want (no negative prompt param in FLUX)

### FLUX Kontext (Image Editing)

Takes `image` + `prompt` describing the edit.

```
# Good editing prompts:
"Change the background to a beach sunset"
"Make the person wear a red hat"
"Convert to black and white except the roses"
"Add snow falling in the scene"
```

The prompt should describe the desired change, not the full image.

### Transparent Backgrounds (gpt-image only)

GPT-Image is the only Replicate generation model that outputs native alpha transparency. Use `--bg transparent` (sets `background: "transparent"` API param). Output auto-forces PNG.

```bash
gen-image.mjs "elephant dung specimen in open kraft box, cream tissue, gold wax seal, studio lighting" \
  --model gpt-image --bg transparent --save product-cutout.png
```

Prompt the subject normally — no need to mention "transparent background" in the text. The `background` param handles it. Keep the composition focused on the subject since there's no background to describe.

For other models: generate normally, then strip bg with `edit-image.mjs rembg output.png`.

## Ideogram (Text in Images)

Best at rendering readable text within images.

```
# Good:
"A vintage movie poster with the title 'COSMIC DRIFT' in bold retro font, space background, astronaut floating"

# Key: put text in quotes within the prompt
"A coffee shop chalkboard menu reading 'ESPRESSO $4 | LATTE $5 | MOCHA $6', hand-drawn style"
```

### Key Parameters

| Param | Values |
|---|---|
| `prompt` | string |
| `aspect_ratio` | same as FLUX |
| `style_type` | `auto`, `general`, `realistic`, `design`, `3d`, `anime` |
| `negative_prompt` | string (supported, unlike FLUX) |
| `magic_prompt_option` | `auto`, `on`, `off` — auto-enhance prompt |

## Recraft SVG (Vector Output)

Only model that outputs actual SVG files.

```
"minimalist logo of a mountain, single color, flat design"
"icon set: house, tree, car, bicycle — outline style, consistent stroke width"
```

### Key Parameters

| Param | Values |
|---|---|
| `prompt` | string |
| `style` | `any`, `icon`, `illustrated`, `hand_drawn`, `stamp`, `line` |
| `size` | `1024x1024`, `1365x1024`, `1024x1365`, etc. |

### SVG Tips
- Keep prompts simple — complex scenes produce messy SVG
- "flat design", "minimalist", "icon" produce cleaner vectors
- "single color" or "two-tone" reduce path complexity
- Output is actual SVG XML, not raster

## Video Generation (Veo, Seedance, Kling)

### Prompt Structure
Video prompts need temporal language.

**Pattern**: `[camera motion], [subject action], [scene], [style], [mood]`

```
"Slow dolly forward through a misty forest at dawn, sunlight filtering through trees, cinematic 4K, ethereal atmosphere"
```

### Camera Motion Terms
- `slow zoom in/out`, `dolly forward/backward`
- `pan left/right`, `tilt up/down`
- `tracking shot`, `orbit around`
- `crane shot`, `aerial view descending`
- `static/locked camera`, `handheld`
- `first person POV`

### Key Parameters (vary by model)

| Param | Veo | Seedance | Kling |
|---|---|---|---|
| `prompt` | ✓ | ✓ | ✓ |
| `duration` | 5-10s | 5-10s | 5-15s |
| `aspect_ratio` | 16:9, 9:16, 1:1 | varies | varies |
| `image` | ✓ (i2v) | ✓ | ✓ |

### Video Tips
- Be specific about motion — "camera slowly pans" beats "panning shot"
- Include temporal progression: "starting with..., transitioning to..."
- Mood words matter: "cinematic", "dreamlike", "documentary", "energetic"
- Shorter prompts often work better than image-gen-length prompts
- Most models generate 5-10s clips; plan for short scenes

## Text-to-Speech

### Kokoro (Default)
Simple: just pass `text`. Voice selection via `voice` param.

```json
{"text": "Welcome to Ordure and Company.", "voice": "af_heart"}
```

### ElevenLabs v3 (Most Control)
Supports audio tags in text for emotion/pacing control:

```
"<dramatic-pause/> Welcome. <soft> To the finest collection </soft> of curated specimens."
```

Available tags: `<dramatic-pause/>`, `<soft>`, `<whisper>`, `<emphasis>`, `<slow>`, `<fast>`

### Minimax Speech
Supports voice cloning via `voice_id` or SSML-like control.

| Param | Purpose |
|---|---|
| `text` | The text to speak |
| `voice_id` | Voice selection |
| `speed` | 0.5-2.0 |
| `language_boost` | Force specific language |

## Music Generation

### MusicGen (Default)
```json
{
  "prompt": "upbeat jazz piano trio, walking bass line, lo-fi recording quality",
  "duration": 30
}
```

Can also condition on melody by passing `input_audio` (will match rhythm/melody).

### Prompt Structure for Music
**Pattern**: `[genre], [instruments], [mood/energy], [production quality]`

```
"ambient electronic, soft pads, gentle arpeggios, dreamy, reverb-heavy"
"aggressive hip-hop beat, 808 bass, hi-hat rolls, trap, 140 BPM"
"orchestral film score, strings and brass, epic rising tension, Hans Zimmer style"
```

### Music Tips
- BPM helps: "120 BPM", "slow tempo", "uptempo"
- Name instruments: "acoustic guitar", "Rhodes piano", "808 bass"
- Production terms: "lo-fi", "studio quality", "vinyl crackle", "reverb-heavy"
- Reference styles: "in the style of jazz fusion", "synthwave aesthetic"

## Transcription (Whisper)

### Key Parameters

| Param | incredibly-fast-whisper | whisper-diarization |
|---|---|---|
| `audio` | file/URL | file/URL |
| `language` | ISO code or auto | auto |
| `batch_size` | 1-64 (speed vs memory) | — |
| `timestamp` | `chunk`, `word` | — |
| `num_speakers` | — | expected count |

### Tips
- Pass audio URL when possible (faster than file upload)
- For meetings: use `diarize` model to identify speakers
- For subtitles: use `subtitles` model (SRT/VTT output)
- For accuracy on accents: use `gpt-transcribe`

## OCR

### text-extract-ocr
Simple: pass `image`, get text back.

```json
{"image": "screenshot.png"}
```

### marker (PDF Processing)
Converts PDF pages to markdown with layout preservation.

```json
{"document": "report.pdf", "output_format": "markdown"}
```

### Tips
- For screenshots/photos: text-ocr
- For PDFs/documents: marker or deepseek-ocr
- For structured data (tables): datalab-ocr (preserves layout)

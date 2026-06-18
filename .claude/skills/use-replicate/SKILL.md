---
name: use-replicate
description: Use when generating images, video, audio, speech, music, 3D assets, or doing transcription, OCR, upscaling, background removal, image editing, or any AI task beyond text generation. Also use when the user asks to run a model on Replicate or mentions Replicate by name.
---

# use-replicate

Multimodal AI via Replicate. Generate images, video, audio, music. Edit, upscale, transcribe, OCR. Pay-per-use, no GPU needed.

## Setup

Token in `.env` (starts with `r8_`). Get at replicate.com/account/api-tokens. SDK installed via `replicate` in package.json. Scripts auto-load `.env` and `.env.local`.

## Task → Command

Scripts at `.claude/skills/use-replicate/scripts/`. All support `--save path` (target directory must exist).

| Task | Command | Default Model | Cost |
|---|---|---|---|
| Generate image | `gen-image.mjs "prompt"` | flux-schnell | ~$0.003 |
| Generate SVG | `gen-image.mjs "prompt" --model recraft-svg` | recraft-svg (v4.1-pro) | ~$0.04 |
| Generate video | `gen-video.mjs "prompt"` | veo-fast | ~$0.10/s |
| Animate image | `gen-video.mjs --image img.jpg "motion"` | wan-i2v-fast | ~$0.05 |
| Text-to-speech | `gen-audio.mjs tts "text"` | kokoro | ~$0.002 |
| Generate music | `gen-audio.mjs music "prompt" --duration 30` | musicgen | ~$0.05 |
| Transcribe | `transcribe.mjs audio.mp3` | whisper-fast | ~$0.01 |
| Edit image | `edit-image.mjs edit img.jpg "instruction"` | kontext-pro | ~$0.04 |
| Upscale | `edit-image.mjs upscale img.jpg` | topaz | ~$0.02 |
| Remove bg | `edit-image.mjs rembg img.jpg` | 851-rembg | ~$0.002 |
| Face restore | `edit-image.mjs restore face.jpg` | gfpgan | ~$0.002 |
| OCR | `edit-image.mjs ocr screenshot.png` | text-ocr | ~$0.002 |
| Inpaint | `edit-image.mjs inpaint img.jpg "fill grass"` | flux-fill | ~$0.04 |
| Any model | `replicate-run.mjs owner/model --input k=v` | — | varies |

## Prompting Rules

**Diffusion prompts are machine instructions, not customer-facing copy.** Brand voice rules (euphemisms, tone, word bans) apply to text humans read — NOT to image/video generation prompts. A diffusion model needs literal visual descriptions to produce correct output.

If the product is elephant feces in a luxury box, the prompt MUST say "elephant dung" or "elephant feces" — not "specimen" or "curated piece." The model has no idea what "specimen" looks like. Describe exactly what should appear in the image. The brand voice is applied AFTER generation, in alt text, captions, and copy — never in the prompt itself.

### Model Selection (images)

Pick by need, not by default:
- **Speed + quality balance**: nano-banana — fastest model, pro-level quality, text rendering, up to 14 reference images, conversational editing. Best all-rounder for iteration AND production
- **Simple subject, no text**: flux-schnell (cheapest iteration) or flux-2-pro (production)
- **Text on packaging/labels/signs**: nano-banana, gpt-image, or ideogram — FLUX cannot render readable text
- **Complex multi-element scenes** (product + props + certificates + packaging): nano-banana or gpt-image — both handle compositional complexity well
- **Photo-realism, fine detail**: imagen-ultra or flux-2-max
- **Multi-image fusion / style transfer**: nano-banana (up to 14 reference images)
- **Iterative refinement**: nano-banana (conversational editing — refine without re-prompting)
- **Transparent background (alpha channel)**: see Transparent Output below

### Transparent Output (Alpha Channel)

Only **gpt-image** generates images with native transparency on Replicate. No other generation model outputs alpha — not FLUX, not nano-banana, not imagen, not ideogram (Ideogram has a `/generate-transparent` endpoint in its native API, but it's not exposed via Replicate).

**Two paths to transparency:**

| Path | How | When |
|---|---|---|
| **Native generation** | `gen-image.mjs "prompt" --model gpt-image --bg transparent --save out.png` | Subject isolated on transparent bg from the start |
| **Generate + remove bg** | Generate with any model → `edit-image.mjs rembg img.png` | Need a model gpt-image can't match (e.g. flux photorealism), then strip bg |

**Native (gpt-image):** The `--bg transparent` flag sets `background: "transparent"` and auto-forces PNG output (alpha requires PNG or WebP — JPEG has no alpha channel). Prompt as usual — don't put "transparent background" in the prompt text, the parameter handles it.

**Post-processing (any model → rembg):** Generate the image normally, then pipe through background removal:
```bash
gen-image.mjs "product on white background" --model flux-2-pro --save tmp.webp
edit-image.mjs rembg tmp.webp --save product-transparent.png
```
Background removal models: `851-rembg` (default, 25M runs), `bria-rembg` (256 alpha levels, commercial-safe), `recraft-ai/recraft-remove-background` (cleanest edges).

**Common mistake:** Putting "transparent background" in the prompt does NOT produce alpha. Diffusion models render pixels, not alpha channels — the prompt just makes a white/grey background. Use `--bg transparent` (gpt-image) or post-process with rembg.

### Nano Banana 2: Fastest all-rounder + text + multi-image
```
"[Subject + specific details], [action/state], [setting/context], [composition/camera], [style/lighting]"
```
- **Lead with the subject** — model prioritizes the first clause
- **Positive framing** — "empty street" not "no cars"
- **Text in quotes** — `box reads "ORDURE & CO" in gold serif font` (3–5 words max for reliability)
- **Specify materials** — "kraft brown matte box" not "box"
- **Multi-image**: pass up to 14 reference images with explicit role assignments (style, identity, lighting)
- **Conversational editing**: refine after generation ("change the background to dark charcoal") — cheaper than re-rolling
- Output: jpg or png only (no webp). Default resolution 1K — set `--size 4K` for production

Key params: `--aspect 1:1|16:9|9:16|4:3|21:9|1:4|4:1|1:8|8:1` `--format jpg|png` `--size 512px|1K|2K|4K`

Full reference: `references/nano-banana-2.md`

### FLUX (images): Natural language, be specific
```
"[subject — literal visual description], [style/medium], [lighting], [camera], [quality]"
```
- **Be literal**: describe the actual object, material, color, texture, shape
- Include lighting: "dramatic softbox", "golden hour backlight"
- Include camera: "shot on 85mm f/1.4", "macro", "wide angle"
- Include medium: "product photography", "oil painting", "pencil sketch"
- No negative prompt param — describe what you want, not what to avoid
- Best for single-subject compositions without text

Key params: `--aspect 16:9|9:16|4:3|1:1` `--format webp|jpg|png`

### GPT-Image / Ideogram: Complex scenes + text
For product photography with packaging, labels, props, and readable text:
```
"[detailed scene layout: surface, product, packaging with text, props] [lighting setup] [camera] [style]"
```
- Describe every element: box material + finish (matte, glossy, gold foil), interior lining, text on labels, props, surface
- Specify text content in quotes: `box reads "PRODUCT NAME" in gold serif font`
- Describe spatial relationships: "ribbon draped beside box", "certificate leaning against"
- Include atmosphere: surface material (marble, wood), background foliage, color palette
- **Luxury product photography**: specify warm editorial lighting (not cold studio), material finishes (gold foil, embossed, satin), multiple styled props (glass cloches, brass dishes, wax seals, botanical elements), and rich textures

### Ideogram/GPT-Image (text in images): Put text in quotes
```
"A poster with the title 'COSMIC DRIFT' in bold retro font, space background"
```

### Recraft SVG (vectors): Keep simple, specify transparent
Default model: `recraft-svg` → recraft-v4.1-pro-svg (best SVG quality). Budget: `--model recraft-svg-v4`.
```
"minimalist elephant silhouette icon, single solid black color, transparent background, flat design, clean geometric lines"
```
- **Always include "transparent background"** — recraft defaults to filled black canvas
- Use terms: "flat", "icon", "outline", "two-tone", "silhouette", "geometric"
- Complex scenes → messy SVG paths. Keep to single subject
- For brand marks: specify "single solid color" to get monochrome output usable with `currentColor`

**Post-processing (required before embedding in production code):**
1. Strip `<metadata><recraft-signature>...</metadata>` block
2. Remove artifact paths — any `<path>` with `fill-opacity` attribute (partial transparency = rendering artifact)
3. Replace `fill="rgb(0,0,0)"` and `fill="rgb(2,0,0)"` with `fill="currentColor"` for theme compatibility
4. Remove `transform="translate(0,0)"` (no-ops from recraft export)
5. Set `preserveAspectRatio="xMidYMid meet"` and desired display `width`/`height`
6. ViewBox is 2048×2048 — paths are verbose; minify for inline use

### Video: Include camera motion + temporal language
```
"Slow dolly forward through misty forest at dawn, cinematic 4K"
```
Motion terms: slow zoom, dolly forward, pan left, tracking shot, orbit, crane shot, aerial, static, handheld, POV

### Music: Genre + instruments + mood + production
```
"upbeat jazz piano trio, walking bass, lo-fi recording, 120 BPM"
```

### ElevenLabs TTS: Supports audio tags
```
"<dramatic-pause/> Welcome. <soft>To the finest collection.</soft>"
```

## Model Upgrades (when default isn't enough)

| Need | Switch to | Flag |
|---|---|---|
| Higher quality image | flux-2-pro | `--model flux-2-pro` |
| Highest fidelity | flux-2-max | `--model flux-2-max` |
| Text in image | ideogram or gpt-image | `--model ideogram` |
| SVG vector (best) | recraft-svg | `--model recraft-svg` (v4.1-pro) |
| SVG vector (budget) | recraft-svg-v4 | `--model recraft-svg-v4` |
| Top video quality | runway | `--model runway` |
| Voice cloning | chatterbox | `--model chatterbox` |
| Studio TTS | minimax-hd | `--model minimax-hd` |
| Speaker ID | diarize | `--diarize` |
| Subtitles (SRT) | subtitles | `--model subtitles` |

Full model catalog: `models-reference.md`. Detailed prompting: `prompting-guide.md`.

## Inline SDK (when scripts don't fit)

```typescript
import Replicate from "replicate";
const replicate = new Replicate({ auth: process.env.REPLICATE_API_TOKEN });
const output = await replicate.run("owner/model", { input: { prompt: "..." } });
```

Stream: `for await (const c of replicate.stream(model, { input })) { ... }`
File input: `{ image: createReadStream("photo.jpg") }` or URL string.
Create+poll: `replicate.predictions.create({...})` then `replicate.wait(pred)`.

## Quality Check

After generation, visually inspect output for:
1. **Subject accuracy** — does the image contain what the prompt described? (literal objects, not abstractions)
2. **Text legibility** — if text was requested, is it readable and spelled correctly?
3. **Composition** — are all requested elements present and properly arranged?
4. **Production value** — does it match the target use case? (product photography needs editorial quality, not clip-art)

If quality is insufficient: upgrade model tier, add more scene detail to prompt, or regenerate. Don't ship mediocre output.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Token not found | Uncomment `REPLICATE_API_TOKEN` in `.env` — scripts auto-load it |
| Brand-sanitized prompt | Diffusion prompts need literal descriptions, not euphemisms — see Prompting Rules |
| Used FLUX for text-heavy scene | FLUX can't render readable text — use gpt-image or ideogram |
| Underprompted complex scene | Describe every element: surface, props, lighting, spatial layout, text content |
| Ran gen-image in parallel → 429 | Replicate burst-limits to **1 concurrent prediction** on low credit. Generate images **one at a time, never in parallel** (no `&`, no parallel tool calls); `sleep 12` between calls. |
| Output URL expired | URLs expire in 1h — always `--save` to disk |
| File as base64 | Pass ReadStream or URL — SDK auto-uploads |
| Complex SVG prompt | Keep recraft-svg prompts minimal |
| Assumed array output | Some models return string/object — check type |

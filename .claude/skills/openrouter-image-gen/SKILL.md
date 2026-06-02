---
name: openrouter-image-gen
description: Use when needing to generate, create, or produce images from text descriptions. Triggers on requests like "generate an image", "create a picture", "make art of", "draw", "illustrate", or any task requiring AI image generation. Requires OPENROUTER_API_KEY in .env.
---

# OpenRouter Image Generation

Generate images from text prompts via OpenRouter's chat completions API with image modality. Bundled Python script — pure stdlib, no dependencies.

## Setup

Add to `~/.env` or your project's `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_IMAGE_MODEL=google/gemini-2.5-flash-image
```

`OPENROUTER_API_KEY` is required. Model defaults to `google/gemini-2.5-flash-image` if not set.

## How to Generate an Image

Run the bundled script via Bash:

```bash
python3 .claude/skills/openrouter-image-gen/generate-image.py "your prompt here"
```

The script prints the absolute path of the saved image to stdout. Use the Read tool on that path to view the result.

### Options

| Flag | Purpose | Default |
|------|---------|---------|
| `--output`, `-o` | Output file path | `./generated-image.{ext}` |
| `--model`, `-m` | Model ID override | `$OPENROUTER_IMAGE_MODEL` or `google/gemini-2.5-flash-image` |
| `--aspect`, `-a` | Aspect ratio (1:1, 16:9, 4:3, etc.) | Model default |
| `--image-size`, `-s` | Resolution: 0.5K, 1K, 2K, 4K | Model default |

### Examples

```bash
# Basic generation
python3 .claude/skills/openrouter-image-gen/generate-image.py "a dragon on a lighthouse"

# With options
python3 .claude/skills/openrouter-image-gen/generate-image.py \
  "portrait of an elven ranger, oil painting style" \
  --output ~/Pictures/ranger.png \
  --aspect 9:16 \
  --image-size 2K

# Different model
python3 .claude/skills/openrouter-image-gen/generate-image.py \
  "cyberpunk cityscape at night" \
  --model black-forest-labs/flux.2-pro
```

### Workflow

1. Craft a detailed prompt (see references/prompting-best-practices.md)
2. Run the script — it saves the image and prints the path
3. Send the image to the user with `SendUserFile` so they can see it in chat
4. Use the Read tool on the output path to verify the result yourself
5. Any text the model returns alongside the image is logged to stderr

## Writing Good Prompts

Structure: `[subject] + [action] + [setting] + [style] + [lighting] + [framing]`

See **references/prompting-best-practices.md** for detailed guidance on style keywords, lighting, composition, TTRPG-specific tips, and model-specific notes.

Key rules:
- Be specific — "scarred half-orc with a braided beard" not "a warrior"
- Always specify style/medium — "oil painting," "concept art," "photorealistic"
- Always specify lighting — "warm firelight," "moonlit," "chiaroscuro"
- Keep under ~60 words — models drop details from long prompts
- Avoid asking for text in images — AI renders text poorly (Flux models are an exception)

## Available Models

Query live: `curl -s https://openrouter.ai/api/v1/models?output_modalities=image | python3 -m json.tool`

| Model ID | Notes | Cost |
|----------|-------|------|
| `google/gemini-2.5-flash-image` | Good balance of cost/quality, natural language | $0.30/$2.50 per M tokens |
| `openai/gpt-5-image-mini` | GPT-5 image gen, smaller | $2.50/$2 per M tokens |
| `openai/gpt-5-image` | GPT-5 image gen, full | $10/$10 per M tokens |
| `black-forest-labs/flux.2-pro` | Flux, good at text rendering | ~$0.015-0.03/megapixel |
| `black-forest-labs/flux.2-max` | Flux, highest quality | ~$0.03-0.07/megapixel |
| `recraft/recraft-v4.1` | Recraft, supports style param | $0.04/image |
| `x-ai/grok-imagine-image-quality` | Grok Imagine, image-only modality | $0.05/image |
| `bytedance-seed/seedream-4.5` | Seedream | $0.04/image |

## Environment Variables

All optional except API key:

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | **Required.** Your OpenRouter API key |
| `OPENROUTER_IMAGE_MODEL` | Default model ID |
| `OPENROUTER_IMAGE_ASPECT` | Default aspect ratio |
| `OPENROUTER_IMAGE_SIZE` | Default image size (0.5K/1K/2K/4K) |

## Troubleshooting

| Error | Fix |
|-------|-----|
| "OPENROUTER_API_KEY not set" | Add key to `~/.env` or project `.env` |
| API error 401 | Key is invalid or expired — check OpenRouter dashboard |
| API error 402 | Insufficient credits — top up at openrouter.ai |
| API error 400 | Prompt rejected or model doesn't support image output — try a different model |
| "Could not extract image" | Model may not support image modality — check available models list above |
| Network error | Check internet connectivity |

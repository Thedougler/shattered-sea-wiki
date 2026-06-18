# Replicate Models Reference

Quick-lookup for the best model per task. Models listed by category with cost tier and recommended default.

## Image Generation

| Shorthand | Model ID | Speed | Cost | Best For |
|---|---|---|---|---|
| **flux-schnell** | `black-forest-labs/flux-schnell` | ⚡ Fast | ~$0.003 | Default. Quick drafts, iteration |
| flux-2-pro | `black-forest-labs/flux-2-pro` | Medium | ~$0.04 | High quality, JSON prompting, 8 ref images |
| flux-2-max | `black-forest-labs/flux-2-max` | Slow | Premium | Highest fidelity FLUX |
| flux-2-flex | `black-forest-labs/flux-2-flex` | Medium | Premium | Typography specialist, 10 ref images |
| seedream | `bytedance/seedream-4.5` | Medium | Per-image | Cinematic, up to 4K |
| seedream-5 | `bytedance/seedream-5-lite` | Medium | Per-image | Built-in reasoning, multi-image blend |
| imagen-fast | `google/imagen-4-fast` | ⚡ Fast | Per-image | Quick Google-quality iteration |
| imagen-ultra | `google/imagen-4-ultra` | Slow | Premium | Fine detail (skin/hair/fabric) |
| gpt-image | `openai/gpt-image-1.5` | Medium | Per-image | Complex prompts, text rendering in images |
| ideogram | `ideogram-ai/ideogram-v3-turbo` | Medium | $0.03 | Precise text in images |
| recraft | `recraft-ai/recraft-v4` | Medium | Per-image | Design-first, print-ready |
| **recraft-svg** | `recraft-ai/recraft-v4.1-pro-svg` | Medium | Per-image | **Best SVG vector** (default) |
| recraft-svg-v4 | `recraft-ai/recraft-v4-svg` | Medium | Per-image | Budget SVG vector |
| recraft-svg-v41 | `recraft-ai/recraft-v4.1-svg` | Medium | Per-image | Mid-tier SVG vector |
| recraft-svg-20b | `recraft-ai/recraft-20b-svg` | Slow | Per-image | Largest SVG model |
| nano-banana | `google/nano-banana-2` | ⚡⚡ Fastest | Per-image | Fastest gen, text rendering, multi-image fusion (14 refs), conversational editing, web grounding. Outputs jpg/png only, up to 4K. See `references/nano-banana-2.md` |

### Decision Guide
- **Best all-rounder (speed + quality + features)**: nano-banana — text rendering, 14 reference images, conversational editing, web grounding, up to 4K
- **Prototyping / iteration**: nano-banana (fastest) or flux-schnell (cheapest)
- **Production quality**: nano-banana, flux-2-pro, or seedream
- **Text in images**: nano-banana, ideogram, or gpt-image
- **Multi-image fusion / style transfer**: nano-banana (up to 14 refs)
- **Iterative editing**: nano-banana (conversational editing)
- **SVG/vector output**: recraft-svg (v4.1-pro default, best quality; v4/v41/20b also available)
- **Highest photo-realism (skin/hair/fabric)**: imagen-ultra or flux-2-max
- **Complex scenes with many props**: nano-banana or gpt-image
- **Transparent background (alpha)**: gpt-image (`--bg transparent`) — only gen model with native alpha. All others: generate then `edit-image.mjs rembg` to strip bg

## Image Editing

| Shorthand | Model ID | Best For |
|---|---|---|
| **kontext-pro** | `black-forest-labs/flux-kontext-pro` | Default. Text-based editing |
| kontext-max | `black-forest-labs/flux-kontext-max` | Premium text editing, typography |
| p-edit | `prunaai/p-image-edit` | Sub-1s editing, $0.01/edit |
| qwen-edit | `qwen/qwen-image-edit` | Precise text-guided editing |
| qwen-edit-plus | `qwen/qwen-image-edit-plus` | Multi-image + ControlNet |
| flux-fill | `black-forest-labs/flux-fill-pro` | Inpainting/outpainting |
| eraser | `bria/eraser` | Object removal |
| genfill | `bria/genfill` | Object addition |
| expand | `bria/expand-image` | Outpainting/canvas expansion |
| gen-bg | `bria/generate-background` | Background swap via text/ref |

## Image Upscaling

| Shorthand | Model ID | Best For |
|---|---|---|
| **topaz** | `topazlabs/image-upscale` | Default. Professional-grade |
| real-esrgan | `nightmareai/real-esrgan` | Classic, reliable |
| p-upscale | `prunaai/p-image-upscale` | Fastest (<1s), up to 128MP |
| recraft-crisp | `recraft-ai/recraft-crisp-upscale` | Sharper, cleaner |
| crystal | `philz1337x/crystal-upscaler` | Portraits, faces, products |
| google | `google/upscaler` | Simple 2x or 4x |

## Background Removal

| Shorthand | Model ID | Runs |
|---|---|---|
| **851-rembg** | `851-labs/background-remover` | 25M |
| rembg | `cjwbw/rembg` | 11M |
| bria-rembg | `bria/remove-background` | 2M |

## Face Restoration

| Shorthand | Model ID | Best For |
|---|---|---|
| **gfpgan** | `tencentarc/gfpgan` | Default. Real face restoration |
| codeformer | `sczhou/codeformer` | AI-generated faces too |

## Video Generation (Text-to-Video)

| Shorthand | Model ID | Speed | Best For |
|---|---|---|---|
| **veo-fast** | `google/veo-3.1-fast` | Fast | Default. Native audio |
| veo | `google/veo-3.1` | Medium | Higher fidelity + context audio |
| seedance | `bytedance/seedance-2.0` | Medium | Multimodal + native audio |
| seedance-fast | `bytedance/seedance-2.0-fast` | Fast | Speed variant |
| kling | `kwaivgi/kling-v3-omni-video` | Medium | Multimodal + editing + audio |
| runway | `runwayml/gen-4.5` | Slow | #1 ranked, realistic physics |
| sora | `openai/sora-2` | Medium | OpenAI video gen |
| p-video | `prunaai/p-video` | ⚡ Fast | Fast + draft mode |

## Video Generation (Image-to-Video)

| Shorthand | Model ID | Best For |
|---|---|---|
| **wan-i2v-fast** | `wan-video/wan-2.2-i2v-fast` | Default. Fast, cheap |
| wan-i2v | `wan-video/wan-2.7-i2v` | First+last frame, continuation |
| grok-video | `xai/grok-imagine-video` | Fast clips + audio (~30s) |
| seedance-lite | `bytedance/seedance-1-lite` | Budget option |

## Text-to-Speech

| Shorthand | Model ID | Best For |
|---|---|---|
| **kokoro** | `jaaari/kokoro-82m` | Default. Fast, lightweight |
| chatterbox | `resemble-ai/chatterbox-turbo` | Fastest open-source, voice cloning |
| minimax | `minimax/speech-2.8-turbo` | 40+ langs, low latency |
| minimax-hd | `minimax/speech-2.8-hd` | Studio-grade, #1 benchmark |
| gemini-tts | `google/gemini-3.1-flash-tts` | 30 voices, 70+ langs |
| elevenlabs | `elevenlabs/v3` | Audio tags, 70+ langs, 26 voices |

### Decision Guide
- **Quick narration**: kokoro
- **Voice cloning**: chatterbox
- **Multilingual**: minimax or gemini-tts
- **Maximum quality**: minimax-hd
- **Most control (tags/emotions)**: elevenlabs

## Speech-to-Text / Transcription

| Shorthand | Model ID | Best For |
|---|---|---|
| **whisper-fast** | `vaibhavs10/incredibly-fast-whisper` | Default. 150min<2min, 98 langs |
| whisper | `openai/whisper` | Original, reliable |
| whisperx | `victor-upmeet/whisperx` | Word timestamps + diarization |
| diarize | `thomasmol/whisper-diarization` | Speaker identification |
| gpt-transcribe | `openai/gpt-4o-transcribe` | Accents, reasoning |
| subtitles | `m1guelpf/whisper-subtitles` | SRT/VTT output |

## Music Generation

| Shorthand | Model ID | Best For |
|---|---|---|
| **musicgen** | `meta/musicgen` | Default. Text/melody conditioning |
| stable-audio | `stability-ai/stable-audio-2.5` | Open-source, inpainting |
| lyria | `google/lyria-2` | 30s clips, negative prompts |
| minimax-music | `minimax/music-2.5` | Full songs, 14+ section tags |
| elevenlabs-music | `elevenlabs/music` | 5min studio-grade |
| ace-step | `lucataco/ace-step` | Full songs in ~20s |

## 3D Generation

| Shorthand | Model ID | Best For |
|---|---|---|
| trellis | `firtoz/trellis` | Image-to-3D in <1min |
| hunyuan-3d | `tencent/hunyuan-3d-3.1` | Text+image, configurable poly |
| rodin | `hyper3d/rodin` | Up to 5 refs, GLB/USDZ/FBX/OBJ/STL |

## OCR & Document Processing

| Shorthand | Model ID | Best For |
|---|---|---|
| **text-ocr** | `abiruyt/text-extract-ocr` | Default. Simple versatile OCR |
| marker | `datalab-to/marker` | PDF to markdown + JSON |
| deepseek-ocr | `lucataco/deepseek-ocr` | Documents to markdown |
| datalab-ocr | `datalab-to/ocr` | 90 languages, tables, layout |

## Object Detection & Segmentation

| Model ID | Best For |
|---|---|
| `adirik/grounding-dino` | Open-vocab detection with language |
| `meta/sam-2` | Segment Anything v2 (images) |
| `meta/sam-2-video` | Segment Anything v2 (video) |
| `lucataco/florence-2-large` | Unified vision tasks |

## Embeddings

| Model ID | Best For |
|---|---|
| `andreasjansson/clip-features` | CLIP image/text embeddings |
| `replicate/all-mpnet-base-v2` | Semantic search text embeddings |
| `zsxkib/jina-clip-v2` | 89-lang multimodal, 512x512 |
| `daanelson/imagebind` | Text/audio/image unified space |

## Face Swap

| Model ID | Runs |
|---|---|
| `codeplugtech/face-swap` | 2.3M |

## Lipsync

| Model ID | Best For |
|---|---|
| `pixverse/lipsync` | General purpose |
| `bytedance/omni-human` | High quality |
| `sync/lipsync-2-pro` | Professional |

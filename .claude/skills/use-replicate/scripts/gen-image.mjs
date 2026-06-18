#!/usr/bin/env node
/**
 * gen-image.mjs "prompt" [--save out.webp] [--model flux-schnell] [--aspect 16:9] [--format webp]
 *
 * Models: flux-schnell (default/$0.003), flux-2-pro, flux-2-max, seedream, imagen-fast,
 *         imagen-ultra, gpt-image, ideogram, recraft, recraft-svg, nano-banana
 */
import { runWithRetry, saveOutput, printOutput, parseArgs } from "./lib.mjs";

const MODELS = {
  "flux-schnell": "black-forest-labs/flux-schnell",
  "flux-2-pro": "black-forest-labs/flux-2-pro",
  "flux-2-max": "black-forest-labs/flux-2-max",
  "flux-2-flex": "black-forest-labs/flux-2-flex",
  "seedream": "bytedance/seedream-4.5",
  "seedream-5": "bytedance/seedream-5-lite",
  "imagen-fast": "google/imagen-4-fast",
  "imagen-ultra": "google/imagen-4-ultra",
  "gpt-image": "openai/gpt-image-1.5",
  "ideogram": "ideogram-ai/ideogram-v3-turbo",
  "recraft": "recraft-ai/recraft-v4",
  "recraft-svg": "recraft-ai/recraft-v4.1-pro-svg",
  "recraft-svg-v4": "recraft-ai/recraft-v4-svg",
  "recraft-svg-v41": "recraft-ai/recraft-v4.1-svg",
  "recraft-svg-20b": "recraft-ai/recraft-20b-svg",
  "nano-banana": "google/nano-banana-2",
};

const a = parseArgs(process.argv, { model: "flux-schnell", save: null, aspect: null, format: null, quality: null, size: null, bg: null });
if (a._help || !a._positional[0]) {
  console.log(`Usage: gen-image.mjs "prompt" [--save path] [--model name] [--aspect 16:9] [--format webp|jpg|png] [--quality hd] [--size 1536x1024] [--bg transparent]`);
  console.log(`Models: ${Object.keys(MODELS).join(", ")}`);
  process.exit(0);
}

const model = MODELS[a.model] || a.model;
const isNanoBanana = model === "google/nano-banana-2";
const input = { prompt: a._positional[0] };
if (a.aspect) input.aspect_ratio = a.aspect;
if (a.format) input.output_format = a.format;
if (a.quality) input.quality = a.quality;
if (a.size) input[isNanoBanana ? "output_resolution" : "size"] = a.size;
if (a.bg) {
  input.background = a.bg;
  if (a.bg === "transparent" && !a.format) input.output_format = "png";
}

console.error(`Model: ${model} | Prompt: ${input.prompt.slice(0, 80)}...`);
const output = await runWithRetry(model, { input });
await saveOutput(output, a.save);
printOutput(output);

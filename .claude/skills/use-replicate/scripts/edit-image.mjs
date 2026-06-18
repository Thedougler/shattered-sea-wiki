#!/usr/bin/env node
/**
 * edit-image.mjs <mode> <image> [prompt] [--save path] [--model name] [--mask path] [--scale N]
 *
 * Modes:
 *   edit      — text-based editing (kontext-pro default)
 *   upscale   — enhance resolution (topaz default)
 *   rembg     — remove background (851-rembg default)
 *   restore   — face restoration (gfpgan default)
 *   ocr       — extract text (text-ocr default)
 *   inpaint   — fill/replace regions (flux-fill default)
 */
import { createReadStream, writeFileSync } from "fs";
import { resolve } from "path";
import { runWithRetry, saveOutput, printOutput, parseArgs } from "./lib.mjs";

const MODELS = {
  edit: { "kontext-pro": "black-forest-labs/flux-kontext-pro", "kontext-max": "black-forest-labs/flux-kontext-max", "p-edit": "prunaai/p-image-edit", "qwen-edit": "qwen/qwen-image-edit" },
  upscale: { "topaz": "topazlabs/image-upscale", "real-esrgan": "nightmareai/real-esrgan", "p-upscale": "prunaai/p-image-upscale", "crystal": "philz1337x/crystal-upscaler" },
  rembg: { "851-rembg": "851-labs/background-remover", "rembg": "cjwbw/rembg", "bria-rembg": "bria/remove-background" },
  restore: { "gfpgan": "tencentarc/gfpgan", "codeformer": "sczhou/codeformer" },
  ocr: { "text-ocr": "abiruyt/text-extract-ocr", "marker": "datalab-to/marker", "deepseek-ocr": "lucataco/deepseek-ocr" },
  inpaint: { "flux-fill": "black-forest-labs/flux-fill-pro", "bria-genfill": "bria/genfill" },
};
const DEFAULTS = { edit: "kontext-pro", upscale: "topaz", rembg: "851-rembg", restore: "gfpgan", ocr: "text-ocr", inpaint: "flux-fill" };

const a = parseArgs(process.argv, { model: null, save: null, mask: null, scale: null });
const mode = a._positional[0];
const imageFile = a._positional[1];
const prompt = a._positional[2];
if (a._help || !mode || !imageFile) {
  console.log(`Usage: edit-image.mjs <edit|upscale|rembg|restore|ocr|inpaint> <image> [prompt] [--save path] [--model name] [--mask path] [--scale N]`);
  process.exit(0);
}

if (!a.model) a.model = DEFAULTS[mode];
const modelMap = MODELS[mode] || {};
const model = modelMap[a.model] || a.model;
const img = createReadStream(resolve(imageFile));
const input = {};

if (mode === "edit") { input.image = img; if (prompt) input.prompt = prompt; }
else if (mode === "upscale") { input.image = img; if (a.scale) input.scale = Number(a.scale); }
else if (mode === "rembg") { input.image = img; }
else if (mode === "restore") { input.img = img; }
else if (mode === "ocr") { input.image = img; }
else if (mode === "inpaint") { input.image = img; if (prompt) input.prompt = prompt; if (a.mask) input.mask = createReadStream(resolve(a.mask)); }

console.error(`Mode: ${mode} | Model: ${model}`);
const output = await runWithRetry(model, { input });

if (mode === "ocr") {
  const text = typeof output === "string" ? output : output?.text || JSON.stringify(output, null, 2);
  if (a.save) { writeFileSync(resolve(a.save), text); console.error(`Saved: ${a.save}`); }
  console.log(text);
} else {
  await saveOutput(output, a.save);
  printOutput(output);
}

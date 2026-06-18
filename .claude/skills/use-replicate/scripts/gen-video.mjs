#!/usr/bin/env node
/**
 * gen-video.mjs "prompt" [--save out.mp4] [--model veo-fast] [--image photo.jpg] [--duration 5]
 *
 * T2V: veo-fast (default), veo, seedance, seedance-fast, kling, runway, sora, p-video
 * I2V: wan-i2v-fast (default w/ --image), wan-i2v, grok-video, seedance-lite
 */
import { createReadStream } from "fs";
import { resolve } from "path";
import { runWithRetry, saveOutput, printOutput, parseArgs } from "./lib.mjs";

const MODELS = {
  "veo-fast": "google/veo-3.1-fast", "veo": "google/veo-3.1",
  "seedance": "bytedance/seedance-2.0", "seedance-fast": "bytedance/seedance-2.0-fast",
  "kling": "kwaivgi/kling-v3-omni-video", "runway": "runwayml/gen-4.5",
  "sora": "openai/sora-2", "p-video": "prunaai/p-video",
  "wan-i2v-fast": "wan-video/wan-2.2-i2v-fast", "wan-i2v": "wan-video/wan-2.7-i2v",
  "grok-video": "xai/grok-imagine-video", "seedance-lite": "bytedance/seedance-1-lite",
};

const a = parseArgs(process.argv, { model: null, save: null, image: null, duration: null });
if (a._help || (!a._positional[0] && !a.image)) {
  console.log(`Usage: gen-video.mjs "prompt" [--save path] [--model name] [--image path] [--duration sec]`);
  console.log(`Models: ${Object.keys(MODELS).join(", ")}`);
  process.exit(0);
}

if (!a.model) a.model = a.image ? "wan-i2v-fast" : "veo-fast";
const model = MODELS[a.model] || a.model;
const input = {};
if (a._positional[0]) input.prompt = a._positional[0];
if (a.image) input.image = createReadStream(resolve(a.image));
if (a.duration) input.duration = Number(a.duration);

console.error(`Model: ${model} | ${a.image ? "I2V" : "T2V"}`);
const output = await runWithRetry(model, { input });
await saveOutput(output, a.save);
printOutput(output);

#!/usr/bin/env node
/**
 * transcribe.mjs <audio-file> [--save transcript.txt] [--model whisper-fast] [--diarize] [--language en]
 *
 * Models: whisper-fast (default), whisper, whisperx, diarize, gpt-transcribe, subtitles
 */
import { createReadStream } from "fs";
import { resolve } from "path";
import { writeFileSync } from "fs";
import { runWithRetry, parseArgs } from "./lib.mjs";

const MODELS = {
  "whisper-fast": "vaibhavs10/incredibly-fast-whisper", "whisper": "openai/whisper",
  "whisperx": "victor-upmeet/whisperx", "diarize": "thomasmol/whisper-diarization",
  "gpt-transcribe": "openai/gpt-4o-transcribe", "subtitles": "m1guelpf/whisper-subtitles",
};

const a = parseArgs(process.argv, { model: "whisper-fast", save: null, language: null, diarize: false });
if (a._help || !a._positional[0]) {
  console.log(`Usage: transcribe.mjs <audio-file> [--save path] [--model name] [--diarize] [--language en]`);
  console.log(`Models: ${Object.keys(MODELS).join(", ")}`);
  process.exit(0);
}

if (a.diarize) a.model = "diarize";
const model = MODELS[a.model] || a.model;
const input = { audio: createReadStream(resolve(a._positional[0])) };
if (a.language) input.language = a.language;

console.error(`Model: ${model} | File: ${a._positional[0]}`);
const output = await runWithRetry(model, { input });
const result = typeof output === "string" ? output : output?.text || output?.transcription || JSON.stringify(output, null, 2);
if (a.save) { writeFileSync(resolve(a.save), typeof result === "string" ? result : JSON.stringify(result, null, 2)); console.error(`Saved: ${a.save}`); }
console.log(result);

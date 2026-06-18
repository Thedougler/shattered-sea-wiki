#!/usr/bin/env node
/**
 * gen-audio.mjs <tts|music> "text" [--save out.wav] [--model kokoro] [--duration 30] [--voice name]
 *
 * TTS: kokoro (default), chatterbox, minimax, minimax-hd, gemini-tts, elevenlabs
 * Music: musicgen (default), stable-audio, lyria, minimax-music, elevenlabs-music, ace-step
 */
import { runWithRetry, saveOutput, printOutput, parseArgs } from "./lib.mjs";

const TTS = {
  "kokoro": "jaaari/kokoro-82m", "chatterbox": "resemble-ai/chatterbox-turbo",
  "minimax": "minimax/speech-2.8-turbo", "minimax-hd": "minimax/speech-2.8-hd",
  "gemini-tts": "google/gemini-3.1-flash-tts", "elevenlabs": "elevenlabs/v3",
};
const MUSIC = {
  "musicgen": "meta/musicgen", "stable-audio": "stability-ai/stable-audio-2.5",
  "lyria": "google/lyria-2", "minimax-music": "minimax/music-2.5",
  "elevenlabs-music": "elevenlabs/music", "ace-step": "lucataco/ace-step",
};

const a = parseArgs(process.argv, { model: null, save: null, duration: null, voice: null });
const mode = a._positional[0];
const text = a._positional[1];
if (a._help || !mode || !text) {
  console.log(`Usage: gen-audio.mjs <tts|music> "text" [--save path] [--model name] [--duration sec] [--voice name]`);
  console.log(`TTS: ${Object.keys(TTS).join(", ")} | Music: ${Object.keys(MUSIC).join(", ")}`);
  process.exit(0);
}

const map = mode === "tts" ? TTS : MUSIC;
if (!a.model) a.model = mode === "tts" ? "kokoro" : "musicgen";
const model = map[a.model] || a.model;
const input = mode === "tts" ? { text } : { prompt: text };
if (a.duration) input.duration = Number(a.duration);
if (a.voice) input.voice = a.voice;

console.error(`Model: ${model} | ${mode}`);
const output = await runWithRetry(model, { input });
await saveOutput(output, a.save);
printOutput(output);

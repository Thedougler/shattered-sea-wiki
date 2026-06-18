#!/usr/bin/env node
/**
 * replicate-run.mjs <model> [--input key=value ...] [--save path] [--stream] [--json '{...}']
 *
 * Universal runner for any Replicate model. Use when no dedicated script exists.
 * File inputs: --input audio=@file.mp3 (prefix with @)
 */
import { createReadStream } from "fs";
import { resolve } from "path";
import { replicate, runWithRetry, saveOutput, printOutput, parseArgs } from "./lib.mjs";

const a = parseArgs(process.argv, { save: null, stream: false, json: null });
const model = a._positional[0];
if (a._help || !model) {
  console.log(`Usage: replicate-run.mjs <owner/model> [--input key=value ...] [--save path] [--stream] [--json '{...}']`);
  process.exit(0);
}

let input = {};
if (a.json) input = JSON.parse(a.json);

// Parse --input key=value pairs from raw argv (parseArgs doesn't handle this pattern)
const raw = process.argv.slice(2);
for (let i = 0; i < raw.length; i++) {
  if (raw[i] === "--input" || raw[i] === "-i") {
    while (i + 1 < raw.length && !raw[i + 1].startsWith("--")) {
      i++;
      const eq = raw[i].indexOf("=");
      if (eq === -1) continue;
      const k = raw[i].slice(0, eq);
      let v = raw[i].slice(eq + 1);
      if (v.startsWith("@")) v = createReadStream(resolve(v.slice(1)));
      else if (v === "true") v = true;
      else if (v === "false") v = false;
      else if (/^\d+(\.\d+)?$/.test(v)) v = Number(v);
      input[k] = v;
    }
  }
}

console.error(`Model: ${model}`);
if (a.stream) {
  for await (const chunk of replicate.stream(model, { input })) process.stdout.write(chunk.toString());
  process.stdout.write("\n");
} else {
  const output = await runWithRetry(model, { input });
  await saveOutput(output, a.save);
  printOutput(output);
}

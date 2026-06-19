#!/usr/bin/env node
/**
 * beautify.mjs <base.png> <legend.txt> --out art.png [--model id] [--res 1K|2K|4K] [--in px]
 *
 * Controlled img2img beautify. The segmentation key owns 100% of the geometry; the model only
 * styles. We downsample the key to the model's working area, pass it as a data-URI, and LOCK the
 * output aspect ratio to the key (no reframing). Default model is a SOTA image-edit model with
 * web/image search OFF so it cannot invent geometry.
 *
 * Verified live against the Replicate model schema (2026-06): google/nano-banana-2 takes
 * `image_input` (array of data-URI/URL strings), `aspect_ratio` (incl. `match_input_image`),
 * `resolution` (1K|2K|4K), and `image_search`/`google_search` booleans.
 */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import sharp from "sharp";
import { runWithRetry, saveOutput } from "../../use-replicate/scripts/lib.mjs";

function parseArgs(argv) {
  const o = { _: [], model: "google/nano-banana-pro", res: "2K", in: 1536, out: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--model") o.model = argv[++i];
    else if (a === "--res") o.res = argv[++i];
    else if (a === "--in") o.in = Number(argv[++i]);
    else if (a === "--out") o.out = argv[++i];
    else o._.push(a);
  }
  return o;
}

const args = parseArgs(process.argv.slice(2));
const [basePath, legendPath] = args._;
if (!basePath || !legendPath) {
  console.error("usage: beautify.mjs <base.png> <legend.txt> --out art.png [--model id] [--res 1K|2K|4K] [--in px]");
  process.exit(1);
}

const prompt = readFileSync(resolve(legendPath), "utf8");
// Downsample the key to the model's working area (preserves aspect; never enlarge a small key).
const small = await sharp(readFileSync(resolve(basePath)))
  .resize(args.in, args.in, { fit: "inside", withoutEnlargement: true })
  .png()
  .toBuffer();
const meta = await sharp(small).metadata();
const dataUri = `data:image/png;base64,${small.toString("base64")}`;
console.error(`beautify: ${args.model} @ ${args.res} — key ${meta.width}x${meta.height}, aspect LOCKED to input`);

const input = {
  prompt,
  image_input: [dataUri],
  aspect_ratio: "match_input_image",
  resolution: args.res,
  output_format: "png",
};
// nano-banana-2 takes web/image search flags — turn them OFF so it can't invent geometry.
// nano-banana-pro has no such params (don't send them), and follows the prompt more reliably.
if (/nano-banana-2/.test(args.model)) {
  input.image_search = false;
  input.google_search = false;
}

const output = await runWithRetry(args.model, { input });
const out = args.out || resolve(basePath.replace(/\.png$/i, ".art.png"));
await saveOutput(output, out);
console.error(`saved: ${out}`);

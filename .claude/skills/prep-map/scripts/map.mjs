#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, join, basename } from "node:path";
import { loadManifest } from "./lib/manifest.mjs";
import { parseGrid, validateGrid, geometry, asciiPreview } from "./lib/grid.mjs";
import { buildLegendPrompt } from "./lib/legend.mjs";
import { renderLayers, compositePng } from "./lib/render.mjs";

function parseArgs(argv) {
  const out = { _: [], ppi: 300, out: ".", legend: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--ppi") out.ppi = Number(argv[++i]);
    else if (a === "--out") out.out = argv[++i];
    else if (a === "--legend") out.legend = argv[++i];
    else out._.push(a);
  }
  return out;
}

function loadLegendFile(path) {
  if (!path) return {};
  return JSON.parse(readFileSync(resolve(path), "utf8"));
}

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

const args = parseArgs(process.argv.slice(2));
const [cmd, csvPath] = args._;
if (!cmd || !csvPath) fail("usage: map.mjs <preview|render> <tiles.csv> [--ppi N] [--out dir] [--legend f]");

const manifest = loadManifest();
const grid = parseGrid(readFileSync(resolve(csvPath), "utf8"));
const legend = loadLegendFile(args.legend);
const report = validateGrid(grid, manifest, legend);

if (cmd === "preview") {
  console.log(asciiPreview(grid, manifest));
  console.log("");
  for (const w of report.warnings) console.log(`warning: ${w}`);
  for (const e of report.errors) console.log(`error:   ${e}`);
  console.log(report.ok ? `valid — ${grid.width}x${grid.height} tiles` : `INVALID — ${report.errors.length} error(s)`);
  process.exit(report.ok ? 0 : 1);
}

if (cmd === "render") {
  if (!report.ok) {
    for (const e of report.errors) console.error(`error: ${e}`);
    fail("refusing to render an invalid map");
  }
  const geo = geometry(grid, args.ppi);
  const { base, grid: gridL, dm } = await renderLayers(grid, manifest, geo.tilePx);
  const flat = await compositePng(base, [gridL]);
  const prompt = buildLegendPrompt(grid, manifest, { legend });

  mkdirSync(resolve(args.out), { recursive: true });
  const stem = basename(csvPath).replace(/\.csv$/i, "");
  const w = (suffix, buf) => writeFileSync(join(resolve(args.out), `${stem}.${suffix}`), buf);
  w("base.png", base);
  w("grid.png", gridL);
  w("dm.png", dm);
  w("flat.png", flat);
  w("legend.txt", prompt);

  console.log(`rendered ${stem} @ ${geo.widthPx}x${geo.heightPx}px (${args.ppi} ppi) → ${args.out}`);
  for (const wn of report.warnings) console.log(`warning: ${wn}`);
  process.exit(0);
}

fail(`unknown command: ${cmd}`);

#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve, join, basename, dirname } from "node:path";
import { loadManifest } from "./lib/manifest.mjs";
import { parseGrid, validateGrid, geometry, asciiPreview } from "./lib/grid.mjs";
import { renderLayers, compositePng, finishMap } from "./lib/render.mjs";
import { assembleDungeon } from "./lib/compose.mjs";

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

const loadLegendFile = (path) => (path ? JSON.parse(readFileSync(resolve(path), "utf8")) : {});

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

/** Load a tile grid from either a single-room CSV or a dungeon JSON (assembled). Returns { grid, stem }. */
function gridFromInput(inputPath) {
  const abs = resolve(inputPath);
  if (/\.json$/i.test(inputPath)) {
    const spec = JSON.parse(readFileSync(abs, "utf8"));
    const baseDir = dirname(abs);
    const { grid, collisions } = assembleDungeon(spec, (n) => readFileSync(resolve(baseDir, n), "utf8"));
    if (collisions.length) {
      for (const c of collisions) console.error(`collision: (${c.x},${c.y}) ${c.existing} vs ${c.incoming}`);
      fail(`refusing: dungeon has ${collisions.length} collision(s)`);
    }
    return { grid, stem: spec.name || basename(inputPath).replace(/\.json$/i, "") };
  }
  return { grid: parseGrid(readFileSync(abs, "utf8")), stem: basename(inputPath).replace(/\.csv$/i, "") };
}

/** Render a validated grid to base/grid/DM-overlay/flat files. Shared by `render` and `compose`. */
async function writeRenderArtifacts(grid, manifest, _legend, ppi, outDir, stem) {
  const geo = geometry(grid, ppi);
  const { base, grid: gridL, dm } = await renderLayers(grid, manifest, geo.tilePx);
  const flat = await compositePng(base, [gridL]);
  mkdirSync(resolve(outDir), { recursive: true });
  const w = (suffix, buf) => writeFileSync(join(resolve(outDir), `${stem}.${suffix}`), buf);
  w("base.png", base); // the guide → the beautify input
  w("grid.png", gridL); // transparent grid layer
  w("dm-overlay.png", dm); // transparent DM marker layer (composited onto the finished map)
  w("flat.png", flat); // base + grid: the schematic, playable as-is without beautify
  return geo;
}

const args = parseArgs(process.argv.slice(2));
const cmd = args._[0];
const USAGE = "usage: map.mjs <preview|render|composite|compose> <input> [--ppi N] [--out dir] [--legend f]";
if (!cmd) fail(USAGE);

const manifest = loadManifest();

// ── preview / render — single room from a tile CSV ────────────────────────────
if (cmd === "preview" || cmd === "render") {
  const csvPath = args._[1];
  if (!csvPath) fail(USAGE);
  const grid = parseGrid(readFileSync(resolve(csvPath), "utf8"));
  const legend = loadLegendFile(args.legend);
  const report = validateGrid(grid, manifest, legend);
  const stem = basename(csvPath).replace(/\.csv$/i, "");

  if (cmd === "preview") {
    console.log(asciiPreview(grid, manifest));
    console.log("");
    for (const wn of report.warnings) console.log(`warning: ${wn}`);
    for (const e of report.errors) console.log(`error:   ${e}`);
    console.log(report.ok ? `valid — ${grid.width}x${grid.height} tiles` : `INVALID — ${report.errors.length} error(s)`);
    process.exit(report.ok ? 0 : 1);
  }

  if (!report.ok) {
    for (const e of report.errors) console.error(`error: ${e}`);
    fail("refusing to render an invalid map");
  }
  const geo = await writeRenderArtifacts(grid, manifest, legend, args.ppi, args.out, stem);
  console.log(`rendered ${stem} @ ${geo.widthPx}x${geo.heightPx}px (${args.ppi} ppi) → ${args.out}`);
  for (const wn of report.warnings) console.log(`warning: ${wn}`);
  process.exit(0);
}

// ── composite — finish a beautified base into player.png + dm.png ──────────────
if (cmd === "composite") {
  const [, imgPath, mapPath] = args._;
  if (!imgPath || !mapPath) fail("usage: map.mjs composite <beautified.png> <tiles.csv|dungeon.json> [--ppi N] [--out dir]");
  const { grid, stem } = gridFromInput(mapPath);
  const report = validateGrid(grid, manifest, loadLegendFile(args.legend));
  if (!report.ok) {
    for (const e of report.errors) console.error(`error: ${e}`);
    fail("refusing to composite onto an invalid map");
  }
  const beautified = readFileSync(resolve(imgPath));
  const { player, dm } = await finishMap(beautified, grid, manifest, geometry(grid, args.ppi).tilePx);
  mkdirSync(resolve(args.out), { recursive: true });
  writeFileSync(join(resolve(args.out), `${stem}.player.png`), player);
  writeFileSync(join(resolve(args.out), `${stem}.dm.png`), dm);
  console.log(`composited ${stem} @ ${grid.width * args.ppi}x${grid.height * args.ppi}px → ${stem}.player.png + ${stem}.dm.png`);
  process.exit(0);
}

// ── compose — assemble a multi-room dungeon, then render the master ────────────
if (cmd === "compose") {
  const jsonPath = args._[1];
  if (!jsonPath) fail("usage: map.mjs compose <dungeon.json> [--ppi N] [--out dir]");
  const spec = JSON.parse(readFileSync(resolve(jsonPath), "utf8"));
  const dir = dirname(resolve(jsonPath));
  const loadCsv = (name) => readFileSync(resolve(dir, name), "utf8");
  const { grid, collisions } = assembleDungeon(spec, loadCsv);

  console.log(asciiPreview(grid, manifest));
  console.log("");
  for (const c of collisions) console.error(`collision: (${c.x},${c.y}) ${c.existing} vs ${c.incoming} (room ${c.room})`);
  if (collisions.length) fail(`refusing to render a dungeon with ${collisions.length} collision(s)`);

  const legend = loadLegendFile(args.legend);
  const report = validateGrid(grid, manifest, legend);
  if (!report.ok) {
    for (const e of report.errors) console.error(`error: ${e}`);
    fail("refusing to render an invalid dungeon");
  }
  const stem = spec.name || basename(jsonPath).replace(/\.json$/i, "");
  const geo = await writeRenderArtifacts(grid, manifest, legend, args.ppi, args.out, stem);
  console.log(`composed ${stem} @ ${geo.widthPx}x${geo.heightPx}px (${args.ppi} ppi) → ${args.out}`);
  for (const wn of report.warnings) console.log(`warning: ${wn}`);
  process.exit(0);
}

fail(`unknown command: ${cmd}\n${USAGE}`);

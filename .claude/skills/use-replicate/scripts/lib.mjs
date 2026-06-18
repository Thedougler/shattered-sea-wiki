/**
 * Shared utilities for Replicate scripts.
 * Env loading is BUILT IN — reads .env and .env.local automatically.
 * Agents just run: node <script>.mjs "prompt" --save out.webp
 */

import Replicate from "replicate";
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

// Find project root by walking up to package.json
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
let ROOT = resolve(SCRIPT_DIR);
for (let i = 0; i < 10; i++) {
  if (existsSync(resolve(ROOT, "package.json"))) break;
  ROOT = dirname(ROOT);
}

// Load env files — try every candidate, don't stop on first hit
for (const name of [".env", ".env.local"]) {
  const p = resolve(ROOT, name);
  if (!existsSync(p)) continue;
  try {
    for (const line of readFileSync(p, "utf8").split("\n")) {
      const t = line.trim();
      if (!t || t.startsWith("#")) continue;
      const eq = t.indexOf("=");
      if (eq === -1) continue;
      const k = t.slice(0, eq).trim();
      const v = t.slice(eq + 1).trim().replace(/^["']|["']$/g, "");
      if (!process.env[k]) process.env[k] = v;
    }
  } catch {}
}

const token = process.env.REPLICATE_API_TOKEN;
if (!token) {
  console.error(`REPLICATE_API_TOKEN not found.
Checked .env and .env.local in ${ROOT}
Fix: add REPLICATE_API_TOKEN=r8_... to .env (uncommented)
Or: export REPLICATE_API_TOKEN=r8_... in shell
Get token: https://replicate.com/account/api-tokens`);
  process.exit(1);
}

export const replicate = new Replicate({ auth: token });

// Retry wrapper for rate limits
export async function runWithRetry(model, opts, maxRetries = 3) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await replicate.run(model, opts);
    } catch (e) {
      if (e?.response?.status === 429 && attempt < maxRetries) {
        const wait = Number(e.response?.headers?.get?.("retry-after") || 10);
        console.error(`Rate limited. Retrying in ${wait}s... (${attempt + 1}/${maxRetries})`);
        await new Promise(r => setTimeout(r, wait * 1000));
        continue;
      }
      // Clean error output — don't dump full request/response objects
      const msg = e?.message || String(e);
      const status = e?.response?.status;
      console.error(`Error${status ? ` (${status})` : ""}: ${msg.split("\n")[0]}`);
      process.exit(1);
    }
  }
}

function toUrl(item) {
  if (typeof item === "string") return item;
  if (item instanceof URL) return item.href;
  if (typeof item?.url === "function") return String(item.url());
  if (item?.url) return String(item.url);
  if (item?.href) return item.href;
  return null;
}

export async function saveOutput(output, savePath) {
  if (!savePath) return;
  const items = Array.isArray(output) ? output : [output];
  for (let i = 0; i < items.length; i++) {
    const url = toUrl(items[i]);
    if (!url) continue;
    const resp = await fetch(url);
    const buf = Buffer.from(await resp.arrayBuffer());
    const dest = items.length > 1
      ? savePath.replace(/(\.[^.]+)$/, `-${i}$1`)
      : savePath;
    const abs = resolve(dest);
    mkdirSync(dirname(abs), { recursive: true });
    writeFileSync(abs, buf);
    console.error(`Saved: ${dest} (${(buf.length / 1024).toFixed(1)}KB)`);
  }
}

export function printOutput(output) {
  const items = Array.isArray(output) ? output : [output];
  for (const item of items) {
    const url = toUrl(item);
    if (url) { console.log(url); continue; }
    console.log(typeof item === "string" ? item : JSON.stringify(item, null, 2));
  }
}

export function parseArgs(argv, flags = {}) {
  const args = argv.slice(2);
  const result = { _positional: [], ...flags };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--help" || args[i] === "-h") { result._help = true; continue; }
    if (args[i].startsWith("--")) {
      const key = args[i].replace(/^--/, "");
      if (key in result && typeof result[key] === "boolean") { result[key] = true; }
      else { i++; result[key] = args[i]; }
      continue;
    }
    if (args[i].startsWith("-") && args[i].length === 2) {
      const short = { s: "save", m: "model", d: "duration", a: "aspect", f: "format", v: "voice", l: "language" };
      const key = short[args[i][1]];
      if (key) { i++; result[key] = args[i]; continue; }
    }
    result._positional.push(args[i]);
  }
  return result;
}

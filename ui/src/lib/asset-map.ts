import fg from 'fast-glob';
import path from 'node:path';

let cached: Map<string, string> | null = null;

export async function buildAssetMap(): Promise<Map<string, string>> {
  if (cached) return cached;

  const assetsDir = path.resolve(import.meta.dirname, '../../../wiki/assets');
  const files = await fg('**/*.{png,jpg,jpeg,webp,gif,svg}', { cwd: assetsDir });

  const map = new Map<string, string>();
  for (const file of files) {
    const filename = path.basename(file);
    if (!map.has(filename)) {
      map.set(filename, `/assets/${file}`);
    }
  }

  cached = map;
  return map;
}

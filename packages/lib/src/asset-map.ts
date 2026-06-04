import path from 'node:path';
import fg from 'fast-glob';

export async function buildAssetMap(assetsDir: string): Promise<Map<string, string>> {
  const files = await fg('**/*.{png,jpg,jpeg,webp,gif,svg}', {
    cwd: assetsDir,
  });

  const map = new Map<string, string>();
  for (const file of files) {
    const filename = path.basename(file);
    if (!map.has(filename)) {
      map.set(filename, `/assets/${file}`);
    }
  }

  return map;
}

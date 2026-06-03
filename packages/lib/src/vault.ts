import fs from 'node:fs';
import path from 'node:path';
import fg from 'fast-glob';

export function resolveVaultRoot(from?: string): string {
  if (from) {
    const resolved = path.resolve(from);
    if (fs.existsSync(resolved)) return resolved;
    throw new Error(`Vault path does not exist: ${resolved}`);
  }
  let dir = process.cwd();
  while (dir !== path.dirname(dir)) {
    const candidate = path.join(dir, 'wiki');
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
      return candidate;
    }
    dir = path.dirname(dir);
  }
  throw new Error('Could not find wiki/ directory — pass --vault or run from within the repo');
}

export async function iterWikiFiles(vaultDir: string): Promise<string[]> {
  return fg('**/*.md', { cwd: vaultDir, absolute: false });
}

export function relPath(absolutePath: string, repoRoot: string): string {
  return path.relative(repoRoot, path.resolve(absolutePath)).replace(/\\/g, '/');
}

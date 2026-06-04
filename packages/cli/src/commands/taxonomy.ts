import fs from 'node:fs';
import path from 'node:path';
import { ALIASES, CANONICAL, resolveVaultRoot } from '@shattered-sea/lib';
import { Command } from 'commander';

export const taxonomyCommand = new Command('taxonomy')
  .description('Check taxonomy sync between TS module and wiki/system/taxonomy.md')
  .option('--check', 'verify sync (exit 1 on drift)')
  .option('--vault <path>', 'vault root directory')
  .action((opts: { check?: boolean; vault?: string }) => {
    const vaultDir = resolveVaultRoot(opts.vault);
    const taxonomyPath = path.join(vaultDir, 'system', 'taxonomy.md');

    if (!fs.existsSync(taxonomyPath)) {
      console.error(`taxonomy.md not found at ${taxonomyPath}`);
      process.exit(1);
    }

    const content = fs.readFileSync(taxonomyPath, 'utf-8');
    const mdTags = new Set<string>();
    for (const match of content.matchAll(/\| `([^`]+)` \|/g)) {
      mdTags.add(match[1]);
    }

    const inTsOnly = [...CANONICAL].filter((t) => !mdTags.has(t));
    const inMdOnly = [...mdTags].filter(
      (t) => !CANONICAL.has(t) && !ALIASES.has(t) && t.match(/^[a-z0-9-]+$/),
    );

    if (inTsOnly.length === 0 && inMdOnly.length === 0) {
      console.log('Taxonomy is in sync.');
      return;
    }

    if (inTsOnly.length) {
      console.log('In TypeScript but missing from taxonomy.md:');
      for (const t of inTsOnly.sort()) console.log(`  + ${t}`);
    }
    if (inMdOnly.length) {
      console.log('In taxonomy.md but missing from TypeScript:');
      for (const t of inMdOnly.sort()) console.log(`  - ${t}`);
    }

    if (opts.check) process.exit(1);
  });

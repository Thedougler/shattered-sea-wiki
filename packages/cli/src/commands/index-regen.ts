import { Command } from 'commander';
import fs from 'node:fs';
import path from 'node:path';
import { generateIndexFile, resolveVaultRoot } from '@shattered-sea/lib';

export const indexCommand = new Command('index')
  .description('Regenerate wiki/index.md from vault frontmatter')
  .option('--write', 'write to wiki/index.md (default: print to stdout)')
  .option('--vault <path>', 'vault root directory')
  .action((opts: { write?: boolean; vault?: string }) => {
    const vaultDir = resolveVaultRoot(opts.vault);
    const repoRoot = path.resolve(vaultDir, '..');
    const today = new Date().toISOString().slice(0, 10);

    const content = generateIndexFile(vaultDir, repoRoot, today);

    if (opts.write) {
      const indexPath = path.join(vaultDir, 'index.md');
      fs.writeFileSync(indexPath, content, 'utf-8');
      process.stderr.write('regen_index: wrote wiki/index.md\n');
    } else {
      process.stdout.write(content);
    }
  });

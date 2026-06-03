import { Command } from 'commander';
import path from 'node:path';
import { fixFrontmatter, resolveVaultRoot } from '@shattered-sea/lib';

export const fixCommand = new Command('fix')
  .description('Complete missing frontmatter fields on wiki files')
  .argument('<files...>', 'paths to wiki markdown files')
  .option('--vault <path>', 'vault root directory')
  .action((files: string[], opts: { vault?: string }) => {
    const vaultDir = resolveVaultRoot(opts.vault);
    const repoRoot = path.resolve(vaultDir, '..');

    for (const file of files) {
      try {
        const result = fixFrontmatter(path.resolve(file), repoRoot);
        if (result.changed.length) {
          process.stderr.write(
            `fixed: [${result.changed.join(', ')}] — ${file}\n`,
          );
        }
        if (result.summaryStale) {
          process.stderr.write(`FLAG: summary-stale — ${file}\n`);
        }
      } catch (err) {
        process.stderr.write(
          `fix_frontmatter error on ${file}: ${err}\n`,
        );
      }
    }
  });

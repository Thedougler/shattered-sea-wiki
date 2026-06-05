import fs from 'node:fs';
import path from 'node:path';
import {
  diffHealthSnapshots,
  formatDiff,
  formatHistory,
  loadSnapshots,
  resolveVaultRoot,
  saveSnapshot,
  takeSnapshot,
} from '@shattered-sea/lib';
import { Command } from 'commander';

export const healthCommand = new Command('health')
  .description('Capture an objective, machine-readable snapshot of wiki health')
  .option('--save', 'append snapshot to .claude/health-snapshots.jsonl')
  .option('--label <text>', 'label for the snapshot')
  .option('--diff [a] [b]', 'compare two snapshot files (or last 2 saved)')
  .option('--history', 'print trend table of saved snapshots')
  .option('--vault <path>', 'vault root directory')
  .action(
    (opts: {
      save?: boolean;
      label?: string;
      diff?: string | boolean;
      history?: boolean;
      vault?: string;
    }) => {
      const vaultDir = resolveVaultRoot(opts.vault);
      const repoRoot = path.resolve(vaultDir, '..');

      if (opts.history) {
        console.log(formatHistory(loadSnapshots(repoRoot)));
        return;
      }

      if (opts.diff !== undefined) {
        const args = process.argv.slice(process.argv.indexOf('--diff') + 1);
        const filePaths = args.filter(
          (a) => !a.startsWith('-') && fs.existsSync(a),
        );

        if (filePaths.length >= 2) {
          const a = JSON.parse(fs.readFileSync(filePaths[0], 'utf-8'));
          const b = JSON.parse(fs.readFileSync(filePaths[1], 'utf-8'));
          console.log(formatDiff(diffHealthSnapshots(a, b)));
        } else {
          const snapshots = loadSnapshots(repoRoot);
          if (snapshots.length < 2) {
            console.error(
              'Need at least 2 saved snapshots for --diff without arguments.',
            );
            process.exit(1);
          }
          const a = snapshots[snapshots.length - 2];
          const b = snapshots[snapshots.length - 1];
          console.log(formatDiff(diffHealthSnapshots(a, b)));
        }
        return;
      }

      const snapshot = takeSnapshot(vaultDir, repoRoot, opts.label ?? '');

      if (opts.save) {
        saveSnapshot(snapshot, repoRoot);
        console.log(
          `Snapshot saved (${snapshot.lint_total} lint issues, ${snapshot.file_count} files)`,
        );
      } else {
        console.log(JSON.stringify(snapshot, null, 2));
      }
    },
  );

import path from 'node:path';
import {
  type Issue,
  type LintOptions,
  type Severity,
  SEVERITIES,
  batchIssues,
  diffSnapshots,
  formatTopActions,
  lint,
  resolveVaultRoot,
  writeReport,
} from '@shattered-sea/lib';
import { Command } from 'commander';

export const lintCommand = new Command('lint')
  .description('Lint the wiki: report problems, auto-fix the safe ones')
  .argument('[paths...]', 'limit to these files/dirs (default: whole vault)')
  .option('--fix', 'standardize frontmatter in place')
  .option(
    '--fix-tags',
    'also fix safe tag issues (aliases, deprecated-fm/system tags)',
  )
  .option(
    '--since <ref>',
    "only lint files changed since this git ref or date (e.g. HEAD~5, 2026-06-01, '3 days ago')",
  )
  .option('--report', 'also write the DM review queue to wiki/dm/review-queue.md')
  .option('--summary', 'print only the count line')
  .option('--json', 'emit issues as JSON to stdout')
  .option('--top <n>', 'show the top N highest-leverage actions', parseInt)
  .option(
    '--diff <snapshot>',
    'compare against a previous --json snapshot file and show deltas',
  )
  .option(
    '--min-severity <level>',
    'suppress issues below this severity (default: quality = show all)',
    'quality',
  )
  .option('--vault <path>', 'vault root directory')
  .action(
    (
      paths: string[],
      opts: {
        fix?: boolean;
        fixTags?: boolean;
        since?: string;
        report?: boolean;
        summary?: boolean;
        json?: boolean;
        top?: number;
        diff?: string;
        minSeverity?: string;
        vault?: string;
      },
    ) => {
      const vaultDir = resolveVaultRoot(opts.vault);
      const repoRoot = path.resolve(vaultDir, '..');

      const options: LintOptions = {
        fix: opts.fix || opts.fixTags,
        fixTags: opts.fixTags,
        since: opts.since,
        minSeverity: (opts.minSeverity ?? 'quality') as Severity,
        paths: paths.length ? paths : undefined,
      };

      const result = lint(vaultDir, repoRoot, options);

      // Log fixed files
      for (const { file, changed } of result.fixed) {
        process.stderr.write(`fixed: [${changed.join(', ')}] — ${file}\n`);
      }

      // Summary line
      const summary =
        `WIKI LINT: ${result.counts.error} errors · ${result.counts.warning} warnings · ` +
        `${result.counts.quality} quality` +
        (result.fixed.length
          ? ` · ${result.fixed.length} files standardized`
          : '');

      // JSON output
      if (opts.json) {
        const byRule: Record<string, number> = {};
        for (const i of result.issues) {
          byRule[i.rule] = (byRule[i.rule] ?? 0) + 1;
        }
        console.log(
          JSON.stringify(
            {
              summary: result.counts,
              by_rule: byRule,
              fixed: result.fixed,
              issues: result.issues,
            },
            null,
            2,
          ),
        );
        process.exit(result.counts.error ? 1 : 0);
      }

      // Write report
      let reportPath: string | null = null;
      if (opts.report) {
        reportPath = writeReport(vaultDir, result.issues, result.counts);
      }

      process.stderr.write(summary + '\n');
      if (reportPath) {
        process.stderr.write(
          `wrote ${path.relative(repoRoot, reportPath)}\n`,
        );
      }

      // Diff mode
      if (opts.diff) {
        console.log(diffSnapshots(result.issues, opts.diff));
        console.log();
      }

      // Top N actions
      if (opts.top) {
        console.log(formatTopActions(result.issues, opts.top));
      } else if (!opts.summary) {
        for (const sev of SEVERITIES) {
          const sevIssues = result.issues
            .filter((i: Issue) => i.severity === sev)
            .sort((a: Issue, b: Issue) => {
              const pc = a.path.localeCompare(b.path);
              return pc !== 0 ? pc : a.rule.localeCompare(b.rule);
            });
          if (sevIssues.length === 0) continue;
          console.log(`${sev.toUpperCase()} (${sevIssues.length})`);
          for (const i of sevIssues) {
            const suffix = i.fix ? `  ·fix: ${i.fix}` : '';
            console.log(`  ${i.path}  ${i.rule}  ${i.detail}${suffix}`);
          }
        }
      }

      process.exit(result.counts.error ? 1 : 0);
    },
  );

import fs from 'node:fs';
import path from 'node:path';
import {
  detectDrift,
  getFields,
  iterWikiFiles,
  resolveVaultRoot,
  setField,
  syncField,
} from '@shattered-sea/lib';
import { Command } from 'commander';

function resolveRoots(opts: { vault?: string }): { vaultDir: string; repoRoot: string } {
  const vaultDir = resolveVaultRoot(opts.vault);
  const repoRoot = path.resolve(vaultDir, '..');
  return { vaultDir, repoRoot };
}

function expandFiles(
  patterns: string[],
  vaultDir: string,
  repoRoot: string,
  filterDir?: string,
  filterField?: string,
  filterValue?: string,
): string[] {
  if (patterns.length > 0) {
    return patterns.map((p) => path.resolve(p));
  }
  const results: string[] = [];
  function walk(dir: string) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) =>
      a.name.localeCompare(b.name),
    )) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith('.md') && entry.name !== 'index.md') results.push(full);
    }
  }

  const searchDir = filterDir ? path.resolve(vaultDir, filterDir) : vaultDir;
  if (!fs.existsSync(searchDir)) {
    process.stderr.write(`Directory not found: ${searchDir}\n`);
    return [];
  }
  walk(searchDir);

  if (filterField && filterValue !== undefined) {
    return results.filter((f) => {
      const fields = getFields(f);
      const raw = (fields[filterField] ?? '').replace(/^["']|["']$/g, '');
      return raw === filterValue;
    });
  }

  return results;
}

const getCmd = new Command('get')
  .description('Read a frontmatter field from wiki files')
  .argument('<field>', 'frontmatter field to read')
  .option('--dir <path>', 'subdirectory under wiki/ to scan')
  .option('--filter <field=value>', 'only show files where field equals value')
  .option('--vault <path>', 'vault root directory')
  .action((field: string, opts: { dir?: string; filter?: string; vault?: string }) => {
    const { vaultDir, repoRoot } = resolveRoots(opts);
    let filterField: string | undefined;
    let filterValue: string | undefined;
    if (opts.filter) {
      const [fk, ...fvParts] = opts.filter.split('=');
      filterField = fk;
      filterValue = fvParts.join('=');
    }
    const files = expandFiles([], vaultDir, repoRoot, opts.dir, filterField, filterValue);

    for (const f of files) {
      const fields = getFields(f);
      const val = fields[field] ?? '';
      const raw = val.replace(/^["']|["']$/g, '');
      const rel = path.relative(repoRoot, f);
      process.stdout.write(`${rel}\t${raw}\n`);
    }
  });

const setCmd = new Command('set')
  .description('Set a frontmatter field idempotently')
  .argument('<field>', 'frontmatter field to set')
  .argument('<value>', 'value to set')
  .argument('[files...]', 'files to update (or use --dir/--filter)')
  .option('--dir <path>', 'subdirectory under wiki/ to scan')
  .option('--filter <field=value>', 'only update files where field equals value')
  .option('--dry-run', 'show what would change without writing')
  .option('--vault <path>', 'vault root directory')
  .action(
    (
      field: string,
      value: string,
      files: string[],
      opts: { dir?: string; filter?: string; dryRun?: boolean; vault?: string },
    ) => {
      const { vaultDir, repoRoot } = resolveRoots(opts);
      let filterField: string | undefined;
      let filterValue: string | undefined;
      if (opts.filter) {
        const [fk, ...fvParts] = opts.filter.split('=');
        filterField = fk;
        filterValue = fvParts.join('=');
      }
      const targets = expandFiles(files, vaultDir, repoRoot, opts.dir, filterField, filterValue);

      let changed = 0;
      let skipped = 0;

      for (const f of targets) {
        if (opts.dryRun) {
          const fields = getFields(f);
          const cur = (fields[field] ?? '').replace(/^["']|["']$/g, '');
          const newRaw = value.replace(/^["']|["']$/g, '');
          const rel = path.relative(repoRoot, f);
          if (cur !== newRaw) {
            process.stdout.write(`would set: ${rel}\t${field}: ${cur} -> ${newRaw}\n`);
            changed++;
          } else {
            skipped++;
          }
        } else {
          const result = setField(f, field, value);
          const rel = path.relative(repoRoot, result.file);
          if (result.changed) {
            process.stdout.write(`set: ${rel}\t${field}: ${result.oldValue} -> ${result.newValue}\n`);
            changed++;
          } else {
            skipped++;
          }
        }
      }

      process.stderr.write(
        `${opts.dryRun ? '[dry-run] ' : ''}${changed} changed, ${skipped} already correct\n`,
      );
    },
  );

const driftCmd = new Command('drift')
  .description('Report files where type/subtype does not match path inference')
  .option('--type', 'check type field')
  .option('--subtype', 'check subtype field')
  .option('--dir <path>', 'subdirectory under wiki/ to scan')
  .option('--vault <path>', 'vault root directory')
  .action((opts: { type?: boolean; subtype?: boolean; dir?: string; vault?: string }) => {
    const { vaultDir, repoRoot } = resolveRoots(opts);
    const checkFields: ('type' | 'subtype')[] = [];
    if (opts.type) checkFields.push('type');
    if (opts.subtype) checkFields.push('subtype');
    if (checkFields.length === 0) checkFields.push('type', 'subtype');

    const files = expandFiles([], vaultDir, repoRoot, opts.dir);
    let count = 0;

    for (const f of files) {
      const entries = detectDrift(f, repoRoot, checkFields);
      for (const e of entries) {
        process.stdout.write(`${e.file}\t${e.field}: ${e.actual} -> ${e.expected}\n`);
        count++;
      }
    }

    process.stderr.write(`${count} drift${count === 1 ? '' : 's'} found\n`);
  });

const syncCmd = new Command('sync')
  .description('Sync type/subtype to match path inference (idempotent)')
  .option('--type', 'sync type field')
  .option('--subtype', 'sync subtype field')
  .option('--dir <path>', 'subdirectory under wiki/ to scan')
  .option('--dry-run', 'show what would change without writing')
  .option('--vault <path>', 'vault root directory')
  .action((opts: { type?: boolean; subtype?: boolean; dir?: string; dryRun?: boolean; vault?: string }) => {
    const { vaultDir, repoRoot } = resolveRoots(opts);
    const syncFields: ('type' | 'subtype')[] = [];
    if (opts.type) syncFields.push('type');
    if (opts.subtype) syncFields.push('subtype');
    if (syncFields.length === 0) syncFields.push('type', 'subtype');

    const files = expandFiles([], vaultDir, repoRoot, opts.dir);
    let changed = 0;
    let skipped = 0;

    for (const f of files) {
      for (const field of syncFields) {
        if (opts.dryRun) {
          const entries = detectDrift(f, repoRoot, [field]);
          for (const e of entries) {
            process.stdout.write(`would sync: ${e.file}\t${e.field}: ${e.actual} -> ${e.expected}\n`);
            changed++;
          }
          if (entries.length === 0) skipped++;
        } else {
          const result = syncField(f, repoRoot, field);
          if (result.changed) {
            const rel = path.relative(repoRoot, result.file);
            process.stdout.write(
              `synced: ${rel}\t${field}: ${result.oldValue} -> ${result.newValue}\n`,
            );
            changed++;
          } else {
            skipped++;
          }
        }
      }
    }

    process.stderr.write(
      `${opts.dryRun ? '[dry-run] ' : ''}${changed} synced, ${skipped} already correct\n`,
    );
  });

export const frontmatterCommand = new Command('fm')
  .description('Read, set, and sync frontmatter fields across wiki files')
  .addCommand(getCmd)
  .addCommand(setCmd)
  .addCommand(driftCmd)
  .addCommand(syncCmd);

import fs from 'node:fs';
import path from 'node:path';
import fg from 'fast-glob';
import { lint } from './lint.js';

// ─── Types ──────────────────────────────────────────────────────────────────

export interface HealthSnapshot {
  timestamp: string;
  label: string;
  file_count: number;
  total_tokens: number;
  mean_file_tokens: number;
  lint_errors: number;
  lint_warnings: number;
  lint_quality: number;
  lint_total: number;
  lint_by_category: Record<string, number>;
  orphan_count: number;
  deadend_count: number;
  stub_summaries: number;
  pending_ingest: number;
  hook_count: number;
  script_test_count: number;
  infra_tokens: number;
  skill_count: number;
  skill_tokens: number;
  claudemd_tokens: number;
  scripts_tested: string;
  scripts_without_tests: string[];
  daily_runs_total: number;
  daily_runs_zero_output: number;
  daily_ingest_total: number;
  daily_lint_fixes_total: number;
  daily_crosslinks_total: number;
  infra_inventory: InfraInventory;
}

export interface InfraInventory {
  scripts: Array<{ name: string; tokens: number; has_test: boolean }>;
  skills: Array<{ name: string; tokens: number; reference_files: number }>;
  hooks: Array<{ name: string; tokens: number }>;
  rules: Array<{ name: string; tokens: number }>;
}

export interface SnapshotDelta {
  [key: string]: { before: number; after: number; delta: number };
}

// ─── Constants ──────────────────────────────────────────────────────────────

const STUB_PATTERNS = [
  /^stub/i,
  /^no summary/i,
  /^tbd/i,
  /^placeholder/i,
  /^an?\s+(npc|location|faction|item|creature)\s+in\s+the\s+campaign/i,
];

// ─── Helpers ────────────────────────────────────────────────────────────────

function fileTokens(filePath: string): number {
  try {
    return Math.floor(fs.readFileSync(filePath, 'utf-8').length / 4);
  } catch {
    return 0;
  }
}

function extractSummary(text: string): string | null {
  let inFm = false;
  for (const line of text.split('\n')) {
    if (line.trim() === '---') {
      if (!inFm) {
        inFm = true;
        continue;
      }
      break;
    }
    if (inFm) {
      const m = line.match(/^summary:\s*["']?(.+?)["']?\s*$/);
      if (m) return m[1];
    }
  }
  return null;
}

// ─── Metric collectors ──────────────────────────────────────────────────────

export function countWikiFiles(vaultDir: string): {
  fileCount: number;
  totalChars: number;
  stubCount: number;
} {
  const files = fg.sync('**/*.md', { cwd: vaultDir });
  let totalChars = 0;
  let stubCount = 0;

  for (const file of files) {
    try {
      const text = fs.readFileSync(path.join(vaultDir, file), 'utf-8');
      totalChars += text.length;
      const summary = extractSummary(text);
      if (summary && STUB_PATTERNS.some((p) => p.test(summary))) {
        stubCount++;
      }
    } catch {
      /* skip */
    }
  }

  return { fileCount: files.length, totalChars, stubCount };
}

export function runLint(
  vaultDir: string,
  repoRoot: string,
): {
  errors: number;
  warnings: number;
  quality: number;
  byCategory: Record<string, number>;
} {
  const result = lint(vaultDir, repoRoot);
  const byCategory: Record<string, number> = {};
  for (const issue of result.issues) {
    byCategory[issue.rule] = (byCategory[issue.rule] ?? 0) + 1;
  }
  return {
    errors: result.counts.error,
    warnings: result.counts.warning,
    quality: result.counts.quality,
    byCategory,
  };
}

export function countPendingIngest(repoRoot: string): number {
  const inboxDir = path.join(repoRoot, 'Inbox');
  if (!fs.existsSync(inboxDir)) return 0;
  try {
    const files = fg.sync('**/*', { cwd: inboxDir });
    return files.length;
  } catch {
    return 0;
  }
}

export function countHooks(repoRoot: string): number {
  const settingsPath = path.join(repoRoot, '.claude', 'settings.json');
  try {
    const data = JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
    const hooks = data?.hooks?.PostToolUse ?? [];
    return hooks.reduce(
      (sum: number, entry: { hooks?: unknown[] }) =>
        sum + (entry.hooks?.length ?? 0),
      0,
    );
  } catch {
    return 0;
  }
}

export function countScriptTests(repoRoot: string): number {
  const scriptsDir = path.join(repoRoot, '.claude', 'scripts');
  if (!fs.existsSync(scriptsDir)) return 0;
  try {
    return fs
      .readdirSync(scriptsDir)
      .filter((n) => n.startsWith('test_') && n.endsWith('.py')).length;
  } catch {
    return 0;
  }
}

export function inventoryInfrastructure(repoRoot: string): {
  inventory: InfraInventory;
  infraTokens: number;
  skillTokens: number;
  claudemdTokens: number;
} {
  const claudeDir = path.join(repoRoot, '.claude');
  const scriptsDir = path.join(claudeDir, 'scripts');
  const skillsDir = path.join(claudeDir, 'skills');
  const hooksDir = path.join(claudeDir, 'hooks');
  const rulesDir = path.join(claudeDir, 'rules');

  let infraTokens = 0;
  let skillTokens = 0;

  const claudemdTokens = fileTokens(path.join(repoRoot, 'CLAUDE.md'));
  infraTokens += claudemdTokens;

  // Scripts
  const scripts: InfraInventory['scripts'] = [];
  const scriptsWithoutTests: string[] = [];
  if (fs.existsSync(scriptsDir)) {
    const allFiles = fs.readdirSync(scriptsDir).filter((n) => n.endsWith('.py'));
    const testFiles = new Set(allFiles.filter((n) => n.startsWith('test_')));
    const scriptFiles = allFiles.filter(
      (n) => !n.startsWith('test_') && n !== '__pycache__',
    );

    for (const name of scriptFiles.sort()) {
      const tokens = fileTokens(path.join(scriptsDir, name));
      const hasTest = testFiles.has(`test_${name}`);
      scripts.push({ name, tokens, has_test: hasTest });
      if (!hasTest && !name.startsWith('wiki_common')) {
        scriptsWithoutTests.push(name);
      }
      infraTokens += tokens;
    }
  }

  // Skills
  const skills: InfraInventory['skills'] = [];
  if (fs.existsSync(skillsDir)) {
    for (const name of fs.readdirSync(skillsDir).sort()) {
      const skillDir = path.join(skillsDir, name);
      if (!fs.statSync(skillDir).isDirectory()) continue;
      const tokens = fileTokens(path.join(skillDir, 'SKILL.md'));
      let refCount = 0;
      const refDir = path.join(skillDir, 'references');
      if (fs.existsSync(refDir)) {
        refCount = fs
          .readdirSync(refDir)
          .filter((f) => f.endsWith('.md')).length;
      }
      skills.push({ name, tokens, reference_files: refCount });
      skillTokens += tokens;
      infraTokens += tokens;
    }
  }

  // Hooks
  const hooks: InfraInventory['hooks'] = [];
  if (fs.existsSync(hooksDir)) {
    for (const name of fs.readdirSync(hooksDir).sort()) {
      if (name.endsWith('.sh')) {
        const tokens = fileTokens(path.join(hooksDir, name));
        hooks.push({ name, tokens });
        infraTokens += tokens;
      }
    }
  }

  // Rules
  const rules: InfraInventory['rules'] = [];
  if (fs.existsSync(rulesDir)) {
    for (const name of fs.readdirSync(rulesDir).sort()) {
      if (name.endsWith('.md')) {
        const tokens = fileTokens(path.join(rulesDir, name));
        rules.push({ name, tokens });
        infraTokens += tokens;
      }
    }
  }

  return {
    inventory: { scripts, skills, hooks, rules },
    infraTokens,
    skillTokens,
    claudemdTokens,
  };
}

export function parseDailyLog(repoRoot: string): {
  daily_runs_total: number;
  daily_runs_zero_output: number;
  daily_ingest_total: number;
  daily_lint_fixes_total: number;
  daily_crosslinks_total: number;
} {
  const logPath = path.join(repoRoot, 'wiki', 'dm', 'daily-log.md');
  const result = {
    daily_runs_total: 0,
    daily_runs_zero_output: 0,
    daily_ingest_total: 0,
    daily_lint_fixes_total: 0,
    daily_crosslinks_total: 0,
  };

  if (!fs.existsSync(logPath)) return result;

  let text: string;
  try {
    text = fs.readFileSync(logPath, 'utf-8');
  } catch {
    return result;
  }

  let inEntry = false;
  let entryHasOutput = false;

  for (const line of text.split('\n')) {
    if (/^## \d{4}-\d{2}-\d{2}/.test(line)) {
      if (inEntry && !entryHasOutput) result.daily_runs_zero_output++;
      inEntry = true;
      entryHasOutput = false;
      result.daily_runs_total++;
      continue;
    }
    if (!inEntry) continue;

    const ingestM = line.match(/(\d+)\s+sources?\s+processed/);
    if (ingestM) {
      result.daily_ingest_total += parseInt(ingestM[1], 10);
      entryHasOutput = true;
    }

    const lintM = line.match(/(\d+)\s+files?\s+auto-fixed/);
    if (lintM) {
      result.daily_lint_fixes_total += parseInt(lintM[1], 10);
      entryHasOutput = true;
    }

    const xlinkM = line.match(/(\d+)\s+links?\s+added/);
    if (xlinkM) {
      result.daily_crosslinks_total += parseInt(xlinkM[1], 10);
      entryHasOutput = true;
    }
  }

  if (inEntry && !entryHasOutput) result.daily_runs_zero_output++;

  return result;
}

// ─── Snapshot ───────────────────────────────────────────────────────────────

export function takeSnapshot(
  vaultDir: string,
  repoRoot: string,
  label = '',
): HealthSnapshot {
  const { fileCount, totalChars, stubCount } = countWikiFiles(vaultDir);
  const lintResult = runLint(vaultDir, repoRoot);
  const pending = countPendingIngest(repoRoot);
  const hookCount = countHooks(repoRoot);
  const testCount = countScriptTests(repoRoot);
  const { inventory, infraTokens, skillTokens, claudemdTokens } =
    inventoryInfrastructure(repoRoot);
  const daily = parseDailyLog(repoRoot);
  const totalTokens = Math.floor(totalChars / 4);

  const totalScripts = inventory.scripts.length;
  const scriptsWithTests = inventory.scripts.filter((s) => s.has_test).length;

  return {
    timestamp: new Date().toISOString(),
    label,
    file_count: fileCount,
    total_tokens: totalTokens,
    mean_file_tokens: fileCount ? Math.floor(totalTokens / fileCount) : 0,
    lint_errors: lintResult.errors,
    lint_warnings: lintResult.warnings,
    lint_quality: lintResult.quality,
    lint_total: lintResult.errors + lintResult.warnings + lintResult.quality,
    lint_by_category: lintResult.byCategory,
    orphan_count: lintResult.byCategory['orphan'] ?? 0,
    deadend_count: lintResult.byCategory['deadend'] ?? 0,
    stub_summaries: stubCount,
    pending_ingest: pending,
    hook_count: hookCount,
    script_test_count: testCount,
    infra_tokens: infraTokens,
    skill_count: inventory.skills.length,
    skill_tokens: skillTokens,
    claudemd_tokens: claudemdTokens,
    scripts_tested: `${scriptsWithTests}/${totalScripts}`,
    scripts_without_tests: inventory.scripts
      .filter((s) => !s.has_test && !s.name.startsWith('wiki_common'))
      .map((s) => s.name),
    ...daily,
    infra_inventory: inventory,
  };
}

// ─── Persistence ────────────────────────────────────────────────────────────

function snapshotLogPath(repoRoot: string): string {
  return path.join(repoRoot, '.claude', 'health-snapshots.jsonl');
}

export function saveSnapshot(
  snapshot: HealthSnapshot,
  repoRoot: string,
): void {
  const logPath = snapshotLogPath(repoRoot);
  fs.appendFileSync(logPath, JSON.stringify(snapshot) + '\n', 'utf-8');
}

export function loadSnapshots(repoRoot: string): HealthSnapshot[] {
  const logPath = snapshotLogPath(repoRoot);
  if (!fs.existsSync(logPath)) return [];
  const snapshots: HealthSnapshot[] = [];
  for (const line of fs.readFileSync(logPath, 'utf-8').split('\n')) {
    if (line.trim()) {
      try {
        snapshots.push(JSON.parse(line));
      } catch {
        /* skip malformed */
      }
    }
  }
  return snapshots;
}

// ─── Diff ───────────────────────────────────────────────────────────────────

const DIFF_KEYS = [
  'file_count',
  'total_tokens',
  'mean_file_tokens',
  'lint_errors',
  'lint_warnings',
  'lint_quality',
  'lint_total',
  'orphan_count',
  'deadend_count',
  'stub_summaries',
  'pending_ingest',
  'hook_count',
  'script_test_count',
  'infra_tokens',
  'skill_count',
  'skill_tokens',
  'claudemd_tokens',
  'daily_runs_total',
  'daily_runs_zero_output',
  'daily_ingest_total',
  'daily_lint_fixes_total',
  'daily_crosslinks_total',
] as const;

export function diffHealthSnapshots(
  a: HealthSnapshot,
  b: HealthSnapshot,
): SnapshotDelta {
  const deltas: SnapshotDelta = {};
  for (const k of DIFF_KEYS) {
    const va = (a as unknown as Record<string, unknown>)[k];
    const vb = (b as unknown as Record<string, unknown>)[k];
    if (typeof va === 'number' && typeof vb === 'number' && va !== vb) {
      deltas[k] = { before: va, after: vb, delta: vb - va };
    }
  }
  return deltas;
}

export function formatDiff(deltas: SnapshotDelta): string {
  if (Object.keys(deltas).length === 0) return 'No measurable change.';
  const lines: string[] = [];
  for (const [key, info] of Object.entries(deltas).sort(([a], [b]) =>
    a.localeCompare(b),
  )) {
    const d = info.delta;
    const dir = d > 0 ? '+' : '';
    lines.push(`  ${key}: ${info.before} -> ${info.after} (${dir}${d})`);
  }
  return lines.join('\n');
}

export function formatHistory(snapshots: HealthSnapshot[]): string {
  if (snapshots.length === 0) return 'No snapshots recorded yet.';
  const header =
    `${'Date'.padEnd(22)} ${'Label'.padEnd(25)} ${'Files'.padStart(5)} ${'Lint'.padStart(5)} ` +
    `${'Err'.padStart(4)} ${'Warn'.padStart(5)} ${'Orphn'.padStart(5)} ${'Stubs'.padStart(5)} ${'Infra'.padStart(6)}`;
  const lines = [header, '-'.repeat(header.length)];
  for (const s of snapshots.slice(-20)) {
    const ts = s.timestamp.slice(0, 19).replace('T', ' ');
    const label = (s.label || '').slice(0, 25);
    lines.push(
      `${ts.padEnd(22)} ${label.padEnd(25)} ${String(s.file_count).padStart(5)} ` +
        `${String(s.lint_total).padStart(5)} ${String(s.lint_errors).padStart(4)} ${String(s.lint_warnings).padStart(5)} ` +
        `${String(s.orphan_count).padStart(5)} ${String(s.stub_summaries).padStart(5)} ${String(s.infra_tokens).padStart(6)}`,
    );
  }
  return lines.join('\n');
}

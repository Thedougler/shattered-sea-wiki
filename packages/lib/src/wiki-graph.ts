import fg from 'fast-glob';
import matter from 'gray-matter';
import fs from 'node:fs';
import path from 'node:path';
import { deriveSlug, slugify, titleCase } from './slug.js';

export async function buildSlugSet(vaultDir: string): Promise<Set<string>> {
  const files = await fg('**/*.md', { cwd: vaultDir });
  const slugs = new Set<string>();

  for (const file of files) {
    slugs.add(deriveSlug(file));
    try {
      const raw = fs.readFileSync(path.join(vaultDir, file), 'utf-8');
      const { data } = matter(raw);
      if (Array.isArray(data.aliases)) {
        for (const alias of data.aliases) {
          slugs.add(slugify(alias));
        }
      }
    } catch {
      // skip unreadable files
    }
  }

  return slugs;
}

export interface BacklinkEntry {
  slug: string;
  title: string;
}

export async function buildBacklinks(
  vaultDir: string,
): Promise<Map<string, BacklinkEntry[]>> {
  const files = await fg('**/*.md', { cwd: vaultDir });
  const backlinks = new Map<string, BacklinkEntry[]>();
  const linkRegex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;

  for (const file of files) {
    const sourceSlug = deriveSlug(file);
    const sourceTitle = titleCase(sourceSlug);

    try {
      const raw = fs.readFileSync(path.join(vaultDir, file), 'utf-8');
      const body = raw.replace(/^---[\s\S]*?---/, '');
      let match;

      while ((match = linkRegex.exec(body)) !== null) {
        const targetSlug = match[1].toLowerCase().replace(/\s+/g, '-');
        if (targetSlug === sourceSlug) continue;

        if (!backlinks.has(targetSlug)) {
          backlinks.set(targetSlug, []);
        }
        const existing = backlinks.get(targetSlug)!;
        if (!existing.some((e) => e.slug === sourceSlug)) {
          existing.push({ slug: sourceSlug, title: sourceTitle });
        }
      }
    } catch {
      // skip
    }
  }

  return backlinks;
}

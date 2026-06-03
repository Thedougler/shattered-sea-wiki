export function deriveSlug(id: string): string {
  const clean = id.replace(/\.md$/, '');
  const filename = clean.split('/').pop()!;
  if (filename === 'index') {
    const parts = clean.split('/');
    return parts[parts.length - 2] || 'index';
  }
  return filename;
}

export function titleCase(slug: string): string {
  return slug
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

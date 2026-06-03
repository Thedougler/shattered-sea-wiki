import { describe, expect, it } from 'vitest';
import { deriveSlug, slugify, titleCase } from '../src/slug.js';

describe('deriveSlug', () => {
  it('strips .md and returns filename', () => {
    expect(deriveSlug('entities/characters/npcs/captain-voss.md')).toBe('captain-voss');
  });

  it('returns parent directory for index files', () => {
    expect(deriveSlug('entities/items/index.md')).toBe('items');
  });

  it('handles top-level files', () => {
    expect(deriveSlug('hot.md')).toBe('hot');
  });

  it('works without .md extension', () => {
    expect(deriveSlug('some/path/file')).toBe('file');
  });
});

describe('slugify', () => {
  it('lowercases and replaces non-alphanumeric with hyphens', () => {
    expect(slugify('Captain Voss')).toBe('captain-voss');
  });

  it('strips leading and trailing hyphens', () => {
    expect(slugify('--hello world--')).toBe('hello-world');
  });

  it('collapses multiple non-alphanumeric chars', () => {
    expect(slugify('the   great---whale')).toBe('the-great-whale');
  });
});

describe('titleCase', () => {
  it('replaces hyphens with spaces and capitalizes words', () => {
    expect(titleCase('captain-voss')).toBe('Captain Voss');
  });

  it('handles single word', () => {
    expect(titleCase('hot')).toBe('Hot');
  });
});

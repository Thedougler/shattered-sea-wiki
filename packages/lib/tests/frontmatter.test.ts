import { describe, expect, it } from 'vitest';
import { splitFrontmatter, parseFields, getSummary, firstH1 } from '../src/frontmatter.js';

describe('splitFrontmatter', () => {
  it('splits a file with frontmatter', () => {
    const text = '---\ntype: entity\nstatus: active\n---\n\n# Captain Voss\n\nA pirate.';
    const result = splitFrontmatter(text);
    expect(result.hadFrontmatter).toBe(true);
    expect(result.frontmatterLines).toEqual(['type: entity', 'status: active']);
    expect(result.body).toBe('\n# Captain Voss\n\nA pirate.');
  });

  it('returns no frontmatter for files without delimiters', () => {
    const text = '# Just a heading\n\nSome content.';
    const result = splitFrontmatter(text);
    expect(result.hadFrontmatter).toBe(false);
    expect(result.frontmatterLines).toEqual([]);
    expect(result.body).toBe(text);
  });

  it('handles unclosed frontmatter gracefully', () => {
    const text = '---\ntype: entity\nno closing delimiter';
    const result = splitFrontmatter(text);
    expect(result.hadFrontmatter).toBe(false);
  });

  it('handles empty frontmatter', () => {
    const text = '---\n---\n\nContent here.';
    const result = splitFrontmatter(text);
    expect(result.hadFrontmatter).toBe(true);
    expect(result.frontmatterLines).toEqual([]);
  });
});

describe('parseFields', () => {
  it('extracts key-value pairs', () => {
    const lines = ['type: entity', 'status: active', 'publish: false'];
    const fields = parseFields(lines);
    expect(fields).toEqual({ type: 'entity', status: 'active', publish: 'false' });
  });

  it('handles empty values', () => {
    const lines = ['summary:'];
    const fields = parseFields(lines);
    expect(fields).toEqual({ summary: '' });
  });

  it('ignores non-field lines', () => {
    const lines = ['  - item1', 'type: entity', '  - item2'];
    const fields = parseFields(lines);
    expect(fields).toEqual({ type: 'entity' });
  });
});

describe('getSummary', () => {
  it('strips quotes from summary', () => {
    expect(getSummary({ summary: '"A bold captain."' })).toBe('A bold captain.');
  });

  it('returns empty string when missing', () => {
    expect(getSummary({})).toBe('');
  });
});

describe('firstH1', () => {
  it('finds the first H1', () => {
    expect(firstH1('\n# Captain Voss\n\nSome text.')).toBe('Captain Voss');
  });

  it('strips stub suffix', () => {
    expect(firstH1('# The Warren — Stub')).toBe('The Warren');
  });

  it('returns null when no H1 exists', () => {
    expect(firstH1('## Not an H1\n\nSome text.')).toBeNull();
  });
});

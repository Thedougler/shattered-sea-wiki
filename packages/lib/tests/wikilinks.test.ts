import { describe, expect, it } from 'vitest';
import { parseWikilinks, resolveWikilink, escapeHtml } from '../src/wikilinks.js';

describe('parseWikilinks', () => {
  it('extracts simple wikilinks', () => {
    const result = parseWikilinks('See [[captain-voss]] for details.');
    expect(result).toHaveLength(1);
    expect(result[0].slug).toBe('captain-voss');
    expect(result[0].displayName).toBeNull();
  });

  it('extracts wikilinks with display names', () => {
    const result = parseWikilinks('Talk to [[captain-voss|the Captain]].');
    expect(result).toHaveLength(1);
    expect(result[0].slug).toBe('captain-voss');
    expect(result[0].displayName).toBe('the Captain');
  });

  it('normalizes slugs to lowercase with hyphens', () => {
    const result = parseWikilinks('See [[Captain Voss]].');
    expect(result[0].slug).toBe('captain-voss');
  });

  it('handles multiple wikilinks', () => {
    const result = parseWikilinks('[[foo]] and [[bar|Baz]] and [[qux]]');
    expect(result).toHaveLength(3);
    expect(result.map((w) => w.slug)).toEqual(['foo', 'bar', 'qux']);
  });

  it('returns empty array for text without wikilinks', () => {
    expect(parseWikilinks('Just plain text.')).toEqual([]);
  });
});

describe('resolveWikilink', () => {
  const slugSet = new Set(['captain-voss', 'the-warren', 'hot']);

  it('returns true for existing slugs', () => {
    expect(resolveWikilink('captain-voss', slugSet)).toBe(true);
  });

  it('returns false for missing slugs', () => {
    expect(resolveWikilink('nonexistent', slugSet)).toBe(false);
  });
});

describe('escapeHtml', () => {
  it('escapes HTML special characters', () => {
    expect(escapeHtml('<script>alert("xss")</script>')).toBe(
      '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;',
    );
  });
});

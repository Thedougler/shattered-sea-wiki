import { useState, useEffect, useRef } from 'preact/hooks';

interface SearchResult {
  url: string;
  meta: { title?: string };
  excerpt: string;
}

export default function SearchDialog() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [selected, setSelected] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const pagefindRef = useRef<any>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
      if (e.key === 'Escape') setOpen(false);
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, []);

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
      if (!pagefindRef.current) {
        const path = '/pagefind/pagefind.js';
        new Function('return import(' + JSON.stringify(path) + ')')()
          .then((pf: any) => {
            pf.init();
            pagefindRef.current = pf;
          })
          .catch(() => {});
      }
    } else {
      setQuery('');
      setResults([]);
      setSelected(0);
    }
  }, [open]);

  useEffect(() => {
    if (!query.trim() || !pagefindRef.current) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      try {
        const search = await pagefindRef.current.search(query);
        const items = await Promise.all(
          search.results.slice(0, 12).map((r: any) => r.data())
        );
        setResults(items);
        setSelected(0);
      } catch {
        setResults([]);
      }
    }, 150);

    return () => clearTimeout(timer);
  }, [query]);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelected((s) => Math.min(s + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelected((s) => Math.max(s - 1, 0));
    } else if (e.key === 'Enter' && results[selected]) {
      window.location.href = results[selected].url;
    }
  };

  if (!open) return null;

  return (
    <div
      class="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]"
      onClick={(e) => {
        if (e.target === e.currentTarget) setOpen(false);
      }}
    >
      <div
        class="fixed inset-0"
        style="background: rgba(0,0,0,0.6); backdrop-filter: blur(4px)"
      />
      <div
        class="relative w-full max-w-xl rounded-xl border shadow-2xl overflow-hidden"
        style="background: var(--color-bg-secondary); border-color: var(--color-border-highlight)"
      >
        <div class="flex items-center gap-3 px-4 py-3 border-b" style="border-color: var(--color-border)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--color-text-muted); flex-shrink: 0">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onInput={(e) => setQuery((e.target as HTMLInputElement).value)}
            onKeyDown={handleKeyDown}
            placeholder="Search the wiki..."
            class="flex-1 bg-transparent outline-none text-sm"
            style="color: var(--color-text-primary)"
          />
          <kbd
            class="text-xs px-1.5 py-0.5 rounded border"
            style="border-color: var(--color-border); color: var(--color-text-muted)"
          >
            esc
          </kbd>
        </div>

        {results.length > 0 && (
          <ul class="max-h-80 overflow-y-auto py-2">
            {results.map((r, i) => (
              <li key={r.url}>
                <a
                  href={r.url}
                  class="block px-4 py-2.5 text-sm transition-colors"
                  style={
                    i === selected
                      ? 'background: var(--color-bg-tertiary); color: var(--color-text-primary)'
                      : 'color: var(--color-text-secondary)'
                  }
                  onMouseEnter={() => setSelected(i)}
                >
                  <div class="font-medium" style="color: var(--color-text-primary)">
                    {r.meta?.title || r.url}
                  </div>
                  {r.excerpt && (
                    <div
                      class="text-xs mt-0.5 line-clamp-2"
                      style="color: var(--color-text-muted)"
                      dangerouslySetInnerHTML={{ __html: r.excerpt }}
                    />
                  )}
                </a>
              </li>
            ))}
          </ul>
        )}

        {query && results.length === 0 && pagefindRef.current && (
          <div class="px-4 py-6 text-center text-sm" style="color: var(--color-text-muted)">
            No results for "{query}"
          </div>
        )}

        {query && !pagefindRef.current && (
          <div class="px-4 py-6 text-center text-sm" style="color: var(--color-text-muted)">
            Search index not available. Run <code>pnpm build</code> first.
          </div>
        )}
      </div>
    </div>
  );
}

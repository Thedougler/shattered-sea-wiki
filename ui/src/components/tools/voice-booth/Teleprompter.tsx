import { useCallback, useEffect, useRef, useState } from 'preact/hooks';
import type { RecordingMode } from './types';

interface Props {
  character: string;
  summary: string;
  mode: RecordingMode;
  isRecording: boolean;
}

const SPEEDS = [
  { label: 'Slow', px: 0.4 },
  { label: 'Medium', px: 0.8 },
  { label: 'Fast', px: 1.4 },
] as const;

async function fetchScript(
  character: string,
  summary: string,
  mode: RecordingMode,
  previousContext?: string,
): Promise<string> {
  const res = await fetch('/api/voice-script', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, summary, mode, previousContext }),
  });
  if (!res.ok) return '';
  const data = await res.json();
  return data.script || '';
}

export default function Teleprompter({ character, summary, mode, isRecording }: Props) {
  const [blocks, setBlocks] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [speedIdx, setSpeedIdx] = useState(1);
  const [autoScroll, setAutoScroll] = useState(true);

  const containerRef = useRef<HTMLDivElement>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);
  const scrollFrame = useRef<number>(0);
  const manualScrollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const fetchingRef = useRef(false);

  const loadMore = useCallback(async () => {
    if (fetchingRef.current) return;
    fetchingRef.current = true;
    setLoading(true);
    const allText = blocks.join(' ');
    const context = allText.length > 200 ? allText.slice(-200) : allText || undefined;
    const script = await fetchScript(character, summary, mode, context);
    if (script) setBlocks((prev) => [...prev, script]);
    setLoading(false);
    fetchingRef.current = false;
  }, [blocks, character, summary, mode]);

  useEffect(() => {
    setBlocks([]);
    fetchingRef.current = false;
    setLoading(true);
    fetchScript(character, summary, mode).then((script) => {
      if (script) setBlocks([script]);
      setLoading(false);
    });
  }, [character, summary, mode]);

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !fetchingRef.current) loadMore();
      },
      { root: containerRef.current, rootMargin: '200px' },
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [loadMore]);

  useEffect(() => {
    const el = containerRef.current;
    if (!el || !isRecording || !autoScroll) {
      if (scrollFrame.current) cancelAnimationFrame(scrollFrame.current);
      return;
    }
    const speed = SPEEDS[speedIdx].px;
    let last = 0;
    const step = (ts: number) => {
      if (last) {
        const dt = ts - last;
        el.scrollTop += speed * (dt / 16);
      }
      last = ts;
      scrollFrame.current = requestAnimationFrame(step);
    };
    scrollFrame.current = requestAnimationFrame(step);
    return () => {
      if (scrollFrame.current) cancelAnimationFrame(scrollFrame.current);
    };
  }, [isRecording, autoScroll, speedIdx]);

  const handleWheel = useCallback(() => {
    setAutoScroll(false);
    if (manualScrollTimer.current) clearTimeout(manualScrollTimer.current);
    manualScrollTimer.current = setTimeout(() => setAutoScroll(true), 3000);
  }, []);

  return (
    <div class="vb-teleprompter">
      <div class="vb-teleprompter__speed">
        {SPEEDS.map((s, i) => (
          <button
            key={s.label}
            class={`vb-teleprompter__speed-btn ${i === speedIdx ? 'vb-teleprompter__speed-btn--active' : ''}`}
            onClick={() => setSpeedIdx(i)}
          >
            {s.label}
          </button>
        ))}
        {!autoScroll && (
          <button
            class="vb-teleprompter__speed-btn vb-teleprompter__speed-btn--resume"
            onClick={() => setAutoScroll(true)}
          >
            Resume scroll
          </button>
        )}
      </div>

      <div class="vb-teleprompter__scroll" ref={containerRef} onWheel={handleWheel}>
        {blocks.length === 0 && loading ? (
          <div class="vb-teleprompter__loading">Conjuring your script...</div>
        ) : (
          <>
            <div class="vb-teleprompter__text">
              {blocks.map((block, i) => (
                <p key={i}>{block}</p>
              ))}
            </div>
            <div ref={sentinelRef} class="vb-teleprompter__sentinel" />
            {loading && <div class="vb-teleprompter__loading">Loading more...</div>}
          </>
        )}
      </div>
    </div>
  );
}

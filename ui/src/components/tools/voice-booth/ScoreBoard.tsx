import { getTier, getNextTier, TIERS } from './types';

interface Props {
  seconds: number;
  label: string;
}

export default function ScoreBoard({ seconds, label }: Props) {
  const tier = getTier(seconds);
  const next = getNextTier(seconds);
  const progress = next
    ? ((seconds - tier.minSeconds) / (next.minSeconds - tier.minSeconds)) * 100
    : 100;

  return (
    <div class="vb-score">
      <div class="vb-score__label">{label}</div>
      <div class="vb-score__tier">{tier.title}</div>
      <div class="vb-score__stars">
        {Array.from({ length: TIERS[TIERS.length - 1].stars }, (_, i) => (
          <span
            key={i}
            class={`vb-score__star ${i < tier.stars ? 'vb-score__star--filled' : ''}`}
          >
            ★
          </span>
        ))}
      </div>
      {next && (
        <div class="vb-score__progress">
          <div class="vb-score__bar">
            <div class="vb-score__bar-fill" style={{ width: `${Math.min(100, progress)}%` }} />
          </div>
          <div class="vb-score__next">
            Next: {next.title} ({next.minSeconds}s)
          </div>
        </div>
      )}
    </div>
  );
}

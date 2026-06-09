"""Laughter highlight detector for session audio.

Experiment: scan one or more session audio files (the multi-part ``.m4a`` recordings
under ``.raw/sessions/session-NN/audio/parts/``) and rank the moments with the highest
concentration of laughter. Big group laughs are almost always the immediate aftermath of a session
highlight, so the top of this list is a shortlist of "find the funny bits" timestamps.

Approach (see ``compass_artifact_*.md`` for the research that motivated it): we use the
PANNs ``Cnn14_DecisionLevelMax`` sound-event-detection model, which does a single CNN
pass over the audio and returns a *framewise* probability (~10 ms resolution) for every
AudioSet class. We take the max over the laughter family (laughter / giggle / chuckle /
snicker / belly laugh / baby laughter), smooth it, merge contiguous above-threshold
frames into bursts, and rank bursts by integrated intensity (loud *and* sustained floats
to the top). This is ~60x faster than real time on CPU and needs no window tuning.

Multiple part files are stitched into one session-global timeline so the output reads
like "0:42:15 into the session, in part04 at 3:12". Decoding is via ffmpeg, so any format
ffmpeg can read works (m4a, wav, flac, mp3, ...).

Usage::

    python -m shattered_audio.laughs .raw/sessions/session-04/audio/parts/session-04-part-*.m4a --top 25
    python -m shattered_audio.laughs .raw/sessions/session-04/audio/parts/session-04-part-00.m4a --json out.json

First run downloads the PANNs checkpoint (~330 MB) to ``~/panns_data/`` (needs wget).
Also exposed as ``shattered-audio laughs`` via the Typer CLI.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import numpy as np  # noqa: E402

# PANNs models operate at 32 kHz.
SAMPLE_RATE = 32_000

# AudioSet classes that mean "people are laughing". Matched on substrings of the model's
# own label list so we don't hard-code indices.
LAUGH_KEYWORDS = ("laugh", "giggle", "chuckle", "snicker", "chortle", "guffaw")


@dataclass
class Burst:
    """A contiguous run of laughter, in session-global seconds."""

    start: float
    end: float
    peak: float  # max framewise probability in the burst
    integral: float  # area under the probability curve (loud AND sustained)
    part: str  # source file stem the burst falls in
    local_start: float  # offset within that source file (seconds)
    # Where the laughter decays back to the track's average (baseline) AFTER the peak.
    # This spans follow-on jokes that ride the same wave; -1 until computed.
    laugh_end_local: float = -1.0

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class Part:
    """One decoded source file placed on the session timeline."""

    path: Path
    offset: float  # session-global start, in seconds
    duration: float


def fmt_ts(seconds: float) -> str:
    """Seconds -> H:MM:SS (or M:SS under an hour)."""
    seconds = max(0, int(round(seconds)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def decode_audio(path: Path, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Decode any ffmpeg-readable file to mono float32 PCM at ``sample_rate``."""
    cmd = [
        "ffmpeg", "-v", "error", "-nostdin",
        "-i", str(path),
        "-f", "f32le", "-ac", "1", "-ar", str(sample_rate), "-",
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed to decode {path}:\n{proc.stderr.decode(errors='replace')}"
        )
    return np.frombuffer(proc.stdout, dtype=np.float32).copy()


@dataclass
class LaughterScorer:
    """Wraps PANNs sound-event-detection to produce a framewise laughter track."""

    device: str = "cpu"
    _sed: object = field(default=None, repr=False)
    _laugh_ids: list[int] = field(default_factory=list, repr=False)
    _labels: list[str] = field(default_factory=list, repr=False)

    def load(self) -> None:
        from panns_inference import SoundEventDetection, labels

        self._labels = list(labels)
        self._laugh_ids = [
            i for i, label in enumerate(self._labels)
            if any(k in label.lower() for k in LAUGH_KEYWORDS)
        ]
        if not self._laugh_ids:
            raise RuntimeError("No laughter classes found in PANNs labels")
        self._sed = SoundEventDetection(checkpoint_path=None, device=self.device)

    def labels(self) -> list[str]:
        return [self._labels[i] for i in self._laugh_ids]

    def score_track(
        self, audio: np.ndarray, chunk_seconds: float, log=None
    ) -> tuple[np.ndarray, np.ndarray, float]:
        """Return (frame_time_seconds, laughter_prob, frame_period) for one audio array.

        The model is run on ``chunk_seconds`` segments to bound memory; framewise outputs
        are concatenated onto a single local timeline.
        """
        chunk = int(chunk_seconds * SAMPLE_RATE)
        min_samples = int(0.5 * SAMPLE_RATE)  # too-short tails carry no useful signal
        times: list[np.ndarray] = []
        probs: list[np.ndarray] = []
        frame_period = 0.01
        offset = 0.0
        n_chunks = (len(audio) + chunk - 1) // chunk
        for ci, c0 in enumerate(range(0, len(audio), chunk)):
            seg = audio[c0 : c0 + chunk]
            real_dur = len(seg) / SAMPLE_RATE
            if len(seg) >= min_samples:
                framewise = self._sed.inference(seg[None, :].astype(np.float32))
                laugh = framewise[0][:, self._laugh_ids].max(axis=1)
                n = len(laugh)
                frame_period = real_dur / n
                t = offset + np.arange(n) * frame_period
                times.append(t)
                probs.append(laugh.astype(np.float64))
            offset += real_dur
            if log:
                log(f"    chunk {ci + 1}/{n_chunks}  ({fmt_ts(offset)})")

        if not probs:
            return np.array([]), np.array([]), frame_period
        return np.concatenate(times), np.concatenate(probs), frame_period


def _smooth(scores: np.ndarray, k: int) -> np.ndarray:
    """Centered moving average over k frames (k must be odd, >=1)."""
    if k <= 1 or len(scores) == 0:
        return scores
    kernel = np.ones(k) / k
    return np.convolve(scores, kernel, mode="same")


def _bursts_from_scores(
    times: np.ndarray,
    scores: np.ndarray,
    frame_period: float,
    threshold: float,
    min_len: float,
    merge_gap: float,
    part: Part,
) -> list[Burst]:
    """Group above-threshold frames into bursts on the session-global timeline."""
    if len(scores) == 0:
        return []
    above = scores >= threshold
    bursts: list[Burst] = []
    n = len(scores)
    i = 0
    while i < n:
        if not above[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and above[j + 1]:
            j += 1
        local_start = float(times[i])
        local_end = float(times[j]) + frame_period
        seg = scores[i : j + 1]
        bursts.append(
            Burst(
                start=part.offset + local_start,
                end=part.offset + local_end,
                peak=float(seg.max()),
                integral=float(seg.sum() * frame_period),
                part=part.path.stem,
                local_start=local_start,
            )
        )
        i = j + 1

    # Merge bursts separated by less than merge_gap, then drop the too-short ones.
    merged: list[Burst] = []
    for b in bursts:
        if merged and b.start - merged[-1].end <= merge_gap:
            prev = merged[-1]
            prev.end = b.end
            prev.peak = max(prev.peak, b.peak)
            prev.integral += b.integral
        else:
            merged.append(b)

    # Extend each burst forward to where the laughter decays back to the track's average
    # (baseline). The threshold end cuts on the first lull; this tail keeps following until
    # the room is genuinely quiet again, so follow-on jokes riding the same wave are included.
    avg = float(scores.mean())
    for b in merged:
        local_end = b.end - part.offset
        k = int(np.searchsorted(times, local_end))
        k = min(max(k, 0), n - 1)
        while k + 1 < n and scores[k + 1] > avg:
            k += 1
        b.laugh_end_local = max(local_end, float(times[k]) + frame_period)

    return [b for b in merged if b.duration >= min_len]


@dataclass
class ScanConfig:
    threshold: float = 0.10  # framewise laughter probability to count as "laughing"
    min_len: float = 0.5  # drop bursts shorter than this (s)
    merge_gap: float = 1.5  # merge bursts closer than this (s)
    smooth_seconds: float = 0.5  # moving-average smoothing of the prob track
    chunk_seconds: float = 240.0  # inference segment length (bounds memory)
    device: str = "cpu"


def scan(paths: list[Path], cfg: ScanConfig, log=print) -> list[Burst]:
    """Scan part files in order and return all laughter bursts, ranked by intensity."""
    scorer = LaughterScorer(device=cfg.device)
    log("Loading PANNs sound-event-detection model ...")
    scorer.load()
    log(f"  device={cfg.device}  laughter classes={scorer.labels()}")

    all_bursts: list[Burst] = []
    offset = 0.0
    for path in paths:
        log(f"Decoding {path.name} ...")
        audio = decode_audio(path)
        duration = len(audio) / SAMPLE_RATE
        part = Part(path=path, offset=offset, duration=duration)
        log(f"  {fmt_ts(duration)} -> scoring")
        times, scores, frame_period = scorer.score_track(audio, cfg.chunk_seconds, log=log)
        k = max(1, int(cfg.smooth_seconds / frame_period) | 1)  # force odd
        scores = _smooth(scores, k)
        bursts = _bursts_from_scores(
            times, scores, frame_period, cfg.threshold, cfg.min_len, cfg.merge_gap, part
        )
        log(f"  {len(bursts)} laughter burst(s)")
        all_bursts.extend(bursts)
        offset += duration

    all_bursts.sort(key=lambda b: b.integral, reverse=True)
    return all_bursts


def bursts_to_dicts(bursts: list[Burst]) -> list[dict]:
    return [
        {
            "rank": i + 1,
            "session_time": fmt_ts(b.start),
            "session_seconds": round(b.start, 2),
            "part": b.part,
            "part_time": fmt_ts(b.local_start),
            "duration": round(b.duration, 2),
            "peak": round(b.peak, 3),
            "intensity": round(b.integral, 3),
            # Where the laughter (incl. follow-on jokes) decays back to baseline — the
            # data-driven forward boundary for the clip/script. Local mm:ss + seconds.
            "laugh_end": fmt_ts(b.laugh_end_local),
            "laugh_end_seconds": round(b.laugh_end_local, 2),
        }
        for i, b in enumerate(bursts)
    ]


def render_table(bursts: list[Burst], top: int) -> str:
    rows = bursts_to_dicts(bursts[:top])
    lines = [
        f"# Laughter highlights ({len(bursts)} bursts, showing top {len(rows)})",
        "",
        "Ranked by intensity (area under the laughter-probability curve = loud + sustained).",
        "Seek to a moment in its part file; the laugh is usually the aftermath of the highlight.",
        "",
        "| # | Session | Part | In-part | Len | Peak | Intensity |",
        "|--:|--------:|------|--------:|----:|-----:|----------:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['rank']} | {r['session_time']} | {r['part']} | {r['part_time']} "
            f"| {r['duration']:.1f}s | {r['peak']:.2f} | {r['intensity']:.2f} |"
        )
    return "\n".join(lines)


def extract_clips(
    bursts: list[Burst], paths: list[Path], out_dir: Path, top: int, pad: float, log=print
) -> None:
    """Cut the top-N bursts to audio clips (with lead-in) so you can listen and verify.

    Lead-in matters: the laugh is the *aftermath* of the highlight, so we start the clip a
    few seconds before the laughter to capture the joke that caused it.
    """
    by_stem = {p.stem: p for p in paths}
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, b in enumerate(bursts[:top]):
        src = by_stem.get(b.part)
        if src is None:
            continue
        start = max(0.0, b.local_start - pad)
        # End at the laughter tail (where it decays to baseline) so follow-on jokes are kept,
        # plus a small pad. Falls back to the threshold end if the tail wasn't computed.
        tail = b.laugh_end_local if b.laugh_end_local >= 0 else (b.local_start + b.duration)
        dur = max(b.duration, tail - b.local_start) + 2 * pad
        name = f"{i + 1:02d}_{fmt_ts(b.start).replace(':', '-')}_{b.part}.m4a"
        out = out_dir / name
        cmd = [
            "ffmpeg", "-v", "error", "-nostdin", "-y",
            "-ss", f"{start:.2f}", "-i", str(src), "-t", f"{dur:.2f}",
            "-ac", "1", str(out),
        ]
        proc = subprocess.run(cmd, capture_output=True)
        if proc.returncode != 0:
            log(f"  clip {name} failed: {proc.stderr.decode(errors='replace')[:200]}")
        else:
            log(f"  wrote {out}")


def parse_ts(s: str) -> float:
    """Parse 'H:MM:SS' or 'MM:SS' (or plain seconds) to float seconds."""
    parts = [float(p) for p in str(s).strip().split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]


@dataclass
class TranscriptRow:
    start: float  # seconds, local to the part
    end: float
    speaker: str
    text: str


def load_transcript(csv_path: Path) -> list[TranscriptRow]:
    """Load a per-part transcript CSV (ID,Start,End,Speaker,Text)."""
    import csv

    rows: list[TranscriptRow] = []
    with open(csv_path, newline="") as f:
        for d in csv.DictReader(f):
            if not d.get("Start") or not d.get("End"):
                continue
            try:
                rows.append(
                    TranscriptRow(
                        start=parse_ts(d["Start"]),
                        end=parse_ts(d["End"]),
                        speaker=(d.get("Speaker") or "").strip(),
                        text=(d.get("Text") or "").strip(),
                    )
                )
            except (ValueError, KeyError):
                continue
    return rows


def _load_part_transcripts(paths: list[Path], log=print) -> dict[str, tuple[list[TranscriptRow], float]]:
    """Map part stem -> (rows, part_duration). Sibling CSV is '<audio>.csv'."""
    out: dict[str, tuple[list[TranscriptRow], float]] = {}
    for p in paths:
        csv_path = Path(str(p) + ".csv")
        if not csv_path.exists():
            log(f"  no transcript for {p.name} (looked for {csv_path.name})")
            continue
        rows = load_transcript(csv_path)
        duration = max((r.end for r in rows), default=0.0)
        out[p.stem] = (rows, duration)
    return out


def gather_context(
    burst: Burst,
    transcripts: dict[str, tuple[list[TranscriptRow], float]],
    order: list[str],
    seconds: float,
) -> list[tuple[str, TranscriptRow]]:
    """Return (part_stem, row) for transcript lines in the `seconds` before the laugh.

    Spills into the previous part's tail when the window crosses a part boundary.
    """
    out: list[tuple[str, TranscriptRow]] = []
    end = burst.local_start
    start = end - seconds

    if start < 0 and burst.part in order:
        idx = order.index(burst.part)
        if idx > 0:
            prev = order[idx - 1]
            prows, pdur = transcripts.get(prev, ([], 0.0))
            prev_window_start = pdur + start  # start is negative
            out.extend((prev, r) for r in prows if r.end >= prev_window_start)
        start = 0.0

    rows, _ = transcripts.get(burst.part, ([], 0.0))
    out.extend((burst.part, r) for r in rows if r.end >= start and r.start <= end)
    return out


def render_context_report(
    bursts: list[Burst],
    paths: list[Path],
    top: int,
    seconds: float,
    log=print,
) -> str:
    """Markdown: each top laugh with the `seconds` of transcript leading up to it."""
    transcripts = _load_part_transcripts(paths, log=log)
    order = [p.stem for p in sorted(paths, key=lambda p: p.name)]

    lines = [
        f"# Laughter highlights with transcript context (top {min(top, len(bursts))})",
        "",
        f"Each entry shows the {seconds:.0f}s of dialogue leading up to a detected laugh — "
        "the laugh is usually the payoff, so the setup is just above it.",
        "",
    ]
    for i, b in enumerate(bursts[:top]):
        lines.append(
            f"## {i + 1}. {fmt_ts(b.start)} "
            f"— peak {b.peak:.2f}, intensity {b.integral:.2f}, {b.duration:.1f}s"
        )
        tail = f" → laughter to {fmt_ts(b.laugh_end_local)}" if b.laugh_end_local >= 0 else ""
        lines.append(f"*{b.part} @ {fmt_ts(b.local_start)}{tail} (read forward to here for follow-on jokes)*")
        lines.append("")
        ctx = gather_context(b, transcripts, order, seconds)
        if not ctx:
            lines.append("> _(no transcript context found)_")
        else:
            for part_stem, row in ctx:
                tag = "" if part_stem == b.part else f" [{part_stem}]"
                speaker = row.speaker or "?"
                if row.text:
                    lines.append(f"> **{speaker}** ({fmt_ts(row.start)}{tag}): {row.text}")
        lines.append(">")
        lines.append("> 😂 **— laughter detected —**")
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="shattered-audio laughs",
        description="Rank the biggest laughs in session audio (highlight finder).",
    )
    p.add_argument("audio", nargs="+", type=Path, help="Audio part files (sorted by name)")
    p.add_argument("--top", type=int, default=25, help="How many bursts to print")
    p.add_argument("--json", type=Path, help="Write full ranked results as JSON here")
    p.add_argument("--threshold", type=float, default=0.10, help="Laughter prob threshold")
    p.add_argument("--min-len", type=float, default=0.5, help="Drop bursts shorter than this (s)")
    p.add_argument("--merge-gap", type=float, default=1.5, help="Merge bursts closer than this (s)")
    p.add_argument("--smooth", type=float, default=0.5, help="Smoothing window (s)")
    p.add_argument("--chunk", type=float, default=240.0, help="Inference chunk length (s)")
    p.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    p.add_argument("--clips", type=Path, help="Extract top-N bursts as audio clips into this dir")
    p.add_argument("--clip-pad", type=float, default=4.0, help="Lead-in/out around each clip (s)")
    p.add_argument(
        "--context-out", type=Path,
        help="Write a markdown report of the biggest laughs with preceding transcript (needs sibling .csv)",
    )
    p.add_argument(
        "--context-top", type=int, default=10,
        help="How many of the biggest laughs to include in the context report",
    )
    p.add_argument(
        "--context-seconds", type=float, default=60.0,
        help="Seconds of transcript to include before each laugh",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    missing = [p for p in args.audio if not p.exists()]
    if missing:
        print(f"Audio file(s) not found: {', '.join(str(m) for m in missing)}", file=sys.stderr)
        return 1

    cfg = ScanConfig(
        threshold=args.threshold,
        min_len=args.min_len,
        merge_gap=args.merge_gap,
        smooth_seconds=args.smooth,
        chunk_seconds=args.chunk,
        device=args.device,
    )
    paths = sorted(args.audio, key=lambda p: p.name)
    log = lambda m: print(m, file=sys.stderr)  # noqa: E731
    bursts = scan(paths, cfg, log=log)

    if args.json:
        args.json.write_text(json.dumps(bursts_to_dicts(bursts), indent=2))
        log(f"Wrote {len(bursts)} bursts to {args.json}")

    if args.clips:
        log(f"Extracting top {args.top} clips to {args.clips} ...")
        extract_clips(bursts, paths, args.clips, args.top, args.clip_pad, log=log)

    if args.context_out:
        log(f"Writing transcript-context report to {args.context_out} ...")
        report = render_context_report(
            bursts, paths, args.context_top, args.context_seconds, log=log
        )
        args.context_out.write_text(report)

    print(render_table(bursts, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

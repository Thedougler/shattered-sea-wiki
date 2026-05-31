# Batch Queue Protocol

## The Loop

```bash
python3 .claude/scripts/check_ingest.py --batch   # pull a token-aware wave
```

The script fills each batch to a 30k token budget (configurable via `--budget`), walking the
queue smallest-first and stopping when the next file would exceed the budget. stderr reports
the batch size, token total, and remaining count.

Process each source in the wave to completion, one at a time. Archive each as you finish it.
After the wave: regenerate index, commit once, then run the script again for the next wave.

```bash
# after the wave:
python3 .claude/scripts/regen_index.py --write
git add wiki .raw Inbox
git commit -m "ingest: <sources> — <summary>"

# next wave:
python3 .claude/scripts/check_ingest.py --batch
```

The sources you just finished should be gone. If one isn't, its archive didn't land — check
before continuing. If output is empty, you're done.

## Why Batching Matters

- **Quality does not degrade with queue depth.** A source gets the same full decomposition
  whether it is the only file waiting or the three-hundredth. A backlog is not permission
  to rush.
- **Interruptions cost nothing.** Re-running the script confirms the previous archive landed.
  A run that stops halfway resumes by running the script again.

Do not summarize the whole queue or plan all sources up front. Pull a wave, finish it, pull
the next.

## Ordering

The script outputs paths sorted smallest-first by file size. Process them in the order listed
— small files are quick wins that build cross-link density early, and large sources (session
transcripts, PDFs) get full context budget when they come up later.

Do not re-sort or cherry-pick within a wave. The script's ordering is deterministic and
optimized for throughput.

## Adjusting the Budget

The default 30k token budget works for typical wiki content. Override when needed:

```bash
python3 .claude/scripts/check_ingest.py --batch --budget 50000  # larger waves
python3 .claude/scripts/check_ingest.py --batch --budget 15000  # conservative
```

A single file that exceeds the budget is still included (batches are always ≥1 file).

## Shared Context Efficiency

Domain skills and references stay resident across the whole queue — load each once and reuse
for every source. The expensive setup (reading skill chain, loading hot.md) is paid once per
session, not per wave.

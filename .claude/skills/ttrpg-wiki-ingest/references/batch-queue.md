# Batch Queue Protocol (7+ Pending Sources)

When the queue has more than 6 sources, process in waves to keep context manageable.

## The Loop

```bash
python3 .claude/scripts/check_ingest.py --limit 6   # pull a wave
```

Process each source in the wave to completion, one at a time. Archive each as you finish it.
After the wave: regenerate index, commit once, then run the script again for the next wave.

```bash
# after the wave:
python3 .claude/scripts/regen_index.py --write
git add wiki .raw Inbox
git commit -m "ingest: <sources> — <summary>"

# next wave:
python3 .claude/scripts/check_ingest.py --limit 6
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

## Priority Within a Wave

The script lists paths alphabetically. When choosing which to process first within a wave:

1. Reviewed clean session transcripts (they set chronology others link to).
2. DM-declared canon updates.
3. Entity / location / faction / situation notes.
4. Rules and homebrew with table impact.
5. Player-facing handouts needing publish control.
6. Assets and research/guidance documents.

For a one-pass run this barely matters. It matters only when a session can't finish the whole
queue: do the spine first.

## Shared Context Efficiency

Domain skills and references stay resident across the whole queue — load each once and reuse
for every source. The expensive setup (reading skill chain, loading hot.md) is paid once per
session, not per wave.

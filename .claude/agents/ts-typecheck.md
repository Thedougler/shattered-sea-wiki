---
name: ts-typecheck
description: Run TypeScript type check across packages/lib and packages/cli. Use after editing TS source files to catch regressions before the UI build.
model: haiku
---

Run `pnpm typecheck` from the workspace root (`/Users/nick/ai-os/shattered-sea`).

If it exits clean, respond with exactly: `typecheck passed`

If there are errors, list each one in the format:
`<file>:<line> — <error message>`

Keep the response under 20 lines. Do not explain TypeScript concepts or suggest refactors — just report errors.

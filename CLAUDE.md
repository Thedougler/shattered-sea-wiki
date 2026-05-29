# CLAUDE.md — Shattered Sea Wiki Governance
# Under 200 lines. Agent reads this first, every session.

---

## Campaign

**Name:** Shattered Sea
**System:** D&D 5e 2024
**Status:** Active
**Philosophy:** {One sentence describing the campaign's core creative philosophy}
**Style:** Sandbox

---

## Party

| PC | Player | Notes |
|---|---|---|
| Crissdalynn Khinriss | {Player Name} | Crow aarakocra monk |
| Perrin Black-Jaw | {Player Name} | Rattkin sailor; bodhran, Minor Illusion |
| Jean-Claude Tabarnack | {Player Name} | Poison dart frog ranger; holds secret about Simone |
| Delmar Fisk | {Player Name} | Scarlet admiral coat; musket; party face |

**Home base:** *Uncertainty* (ex-HCS Surety) — `wiki/entities/vehicles/hcs-surety.md`
**Current arc:** Party in Calveno after Session 03; ship in dry dock at La Vasca (5-day repair); three new active situations (abyss vision, Umberlee's message, Nona's favor); Kyzil reunited with Crissdalynn.

---

## Active Factions (Clock Status)

Update this block after every session or faction-clock run.

| Faction | Clock | Next Trigger |
|---|---|---|
| Dravosi Crown | Moving — Rupert Knighton will send ships for Cap'n Gorgeous | Knighton's ships intercept or party enters Crown territory |
| The Passage | Nona met; attacks called off; favor owed (Perrin, unconditional); Anzolo status unknown | Nona uses sending stone; Anzolo surfaces |

---

## Doctrine & Automatic Behaviors

All cross-cutting rules — reading order, sandbox constraints, the PC-connection requirement,
the auto-correct protocol, frontmatter requirements, wikilink standards, and the ideal-state
definition — live in one place: **`wiki/system/doctrine.md`**. Load it on demand; don't expect
those rules to be restated in each skill.

Frontmatter completeness and the `updated` date are enforced automatically by a PostToolUse
hook (`.claude/scripts/fix_frontmatter.py`) — you do not maintain them by hand. `index.md` is
regenerated with `.claude/scripts/regen_index.py`, not hand-edited. Structural fixes are applied
without asking and committed; escalate to the DM only for genuine lore contradictions or
ambiguous entity identity (see doctrine).

Read order at a glance: `wiki/hot.md` first, then `wiki/system/task-routing.md`, then
`doctrine.md` and only the entity/situation files the task needs. Never read the full vault
before generating content.

---

## Change Log

See `wiki/log.md` for all structural changes.
See `wiki/discrepancy-log.md` for all lore contradictions (created on first conflict).

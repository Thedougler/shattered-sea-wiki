# Wikilink Standards

## Aliasing

Always alias: `[[npc-slug|NPC Display Name]]` — never bare slugs in body text.
First mention of a named entity in a section gets a link; later mentions in the same
section don't.

## Stub Creation

When a wikilink target doesn't exist, create a stub immediately:

1. Place at the correct path (infer from entity type)
2. Stub frontmatter: `status: stub`, `summary: "Stub — referenced in [[source]]. No page yet."`
3. Stub body: `# {Title} — Stub`
4. Add to `wiki/index.md` with `[stub]` marker
5. Let the write hook complete the remaining frontmatter
6. Log: `AUTO-CORRECT: stub-created — {path}`

## Bidirectional Rule

If A links B as a durable relationship, B gets the reciprocal link. Use the standardized
relationship labels in `frontmatter-defaults.md`.

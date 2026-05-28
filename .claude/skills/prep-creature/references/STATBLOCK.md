# Statblock — Fantasy Statblocks Plugin

Produce syntactically valid `statblock` codeblocks and bestiary-wired monster notes for the **Fantasy Statblocks** Obsidian plugin (Javalent / TTRPG Community).

Load this sub-document whenever:

- Creating a new creature or NPC note with a statblock
- Fixing a statblock that is not rendering correctly
- Wiring a creature to the bestiary
- Using `monster:` recall, `extends:`, or `+`/`-` field-append patterns
- Generating statblock YAML for any supported layout

## Reference Files

Load these on demand — do NOT preload all three. Load only what the task requires.

| Task | Load |
|---|---|
| Creating a 5e statblock from scratch | `references/5E-FIELDS.md` |
| Wiring to the bestiary or using `monster:` recall | `references/BESTIARY.md` |
| Using `columns:`, `dice:`, `extends:`, or any codeblock config key | `references/STATBLOCK-CONFIG.md` |
| Modifying an SRD creature (overrides/appends) | `references/5E-FIELDS.md` + `references/STATBLOCK-CONFIG.md` |

---

## Plugin Landmines — Things That Break Silently

These are Fantasy Statblocks failure modes that produce no error messages.

**`layout:` is case-and-space exact.** `"Basic 5e Layout"` ≠ `"basic 5e layout"` ≠ `"Basic 5E Layout"`. A wrong layout name causes the plugin to silently fall back to the default layout. Always verify the exact string against **Settings → Statblock Layouts** in Obsidian before committing to it.

**`monster:` recall silently returns nothing if the SRD bestiary source is disabled.** If the user's vault has the SRD source toggled off, or they're on a fresh install, `monster: Goblin` renders a blank block. Ask whether the SRD bestiary source is enabled if recall isn't working.

**`extends:` does NOT deep-merge nested lists.** Overriding `actions:` on an extended creature replaces the entire list — not appends to it. Use `actions+:` to add entries, `actions-:` (with `name:` only) to remove by name. Never mix `extends:` with a full `actions:` list expecting a merge.

**`statblock: inline` frontmatter registers the creature in the bestiary.** The frontmatter `name:` field must exactly match the codeblock `name:`. Mismatch causes silent registration failure.

**Dice expressions in `desc:` do NOT auto-link in all layouts.** Plain text `2d6+4` inside a description string is not interactive. Use `dice: true` at the codeblock config level to enable clickable dice rollers.

**`columns: 2` is a codeblock config key, not a separate layout.** There is no "two-column layout" — `Basic 5e Layout` supports columns via the `columns: 2` codeblock option. Never create a new layout for columns.

**Never auto-resolve stat contradictions.** If GM notes conflict with an existing statblock, flag it with a `> [!contradiction]` callout and present both values.

---

## Decision Trees

### Recall vs. write from scratch

| Situation | Approach |
|---|---|
| Creature exists in SRD and changes are <50% of fields | `monster: <SRD Name>` + override changed fields only |
| Homebrew with no SRD analog | Write full statblock from scratch |
| SRD base but >50% of fields differ | Write from scratch — recall noise outweighs value |
| SRD bestiary source is disabled in vault | Write from scratch |

### `extends:` vs `monster:`

- Need to recall a creature from the bestiary (cross-note) → use `monster:`
- Need to inherit from another note in the same vault → use `extends:`
- If both are defined: `monster:` takes precedence; do not mix them

### Layout selection

- Standard 5e → `Basic 5e Layout`
- Two-column → `Basic 5e Layout` + `columns: 2` codeblock key
- Other system → see `references/STATBLOCK-CONFIG.md` for built-in layout names
- Custom layout → must be defined in **Settings → Statblock Layouts** first; name must match exactly

---

## Workflows

### Creating a new creature note

Load `references/5E-FIELDS.md` completely before generating any fields.

1. Establish: name, size, type, CR, and layout string.
2. Fill all required fields (`name`, `size`, `type`, `alignment`, `ac`, `hp`, `hit_dice`, `speed`, `stats`, `cr`) plus any optional fields relevant to the creature.
3. Add `statblock: inline` to frontmatter so it registers in the bestiary.
4. Ensure the frontmatter `name:` exactly matches the codeblock `name:`.
5. Attach wiki frontmatter (`domain`, `type: monster`, `summary`, `status`, `visibility`, `tags`, `related`, `created`, `updated`).
6. Keep the statblock inline in the creature note — do not split to a separate file unless explicitly asked.

### Modifying an existing SRD creature

Load `references/STATBLOCK-CONFIG.md` for `+`/`-` field-append syntax before writing any overrides.

1. Use `monster: <SRD Name>` to establish the baseline.
2. Override only the fields that differ from SRD.
3. Use `actions+:` / `reactions+:` / `traits+:` to append — never overwrite a full section to add one entry.
4. Use `actions-:` with `name:` only to remove a specific action by name.

### Debugging a broken statblock

Check in this order:

1. **Layout name** — copy the exact string from Settings → Statblock Layouts. This is the #1 silent failure.
2. **Bestiary source** — if using `monster:` recall, confirm the SRD source is enabled.
3. **Frontmatter `name:` vs codeblock `name:`** — must match exactly for bestiary registration.
4. **List-override vs list-append** — if inherited actions disappeared, check for `actions:` vs `actions+:`.
5. **Unquoted colons in strings** — `desc: Melee Attack: +4` will break YAML parsing. Quote the value.
6. Validate standalone YAML at https://www.yamllint.com if root cause is still unclear.

---

## Key Patterns

### Minimal viable 5e statblock

````yaml
```statblock
layout: Basic 5e Layout
name: Goblin Scout
size: Small
type: humanoid
alignment: neutral evil
ac: 15
hp: 7
hit_dice: 2d6
speed: "30 ft."
stats: [8, 14, 10, 10, 8, 8]
cr: 1/4
actions:
  - name: Scimitar
    desc: "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 5 (1d6 + 2) slashing damage."
```
````

### Bestiary wire-up (recommended for all new creatures)

````yaml
---
statblock: inline
name: Goblin Shaman
domain: shattered-sea
type: monster
summary: "A goblin touched by dark swamp magic."
status: active
visibility: private
tags: [monster, goblinoid]
related: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

```statblock
layout: Basic 5e Layout
name: Goblin Shaman
...
```
````

`name:` in frontmatter MUST match `name:` in codeblock exactly.

### Override a bestiary creature (append, not replace)

````yaml
```statblock
layout: Basic 5e Layout
monster: Goblin
name: "Goblin Shaman"
cr: 1
traits+:
  - name: "Spellcasting"
    desc: "The shaman is a 3rd-level spellcaster (Wisdom, DC 11)."
actions-:
  - name: Scimitar
```
````

### Extends / inheritance

````yaml
```statblock
layout: Basic 5e Layout
name: Elder Goblin
extends: Goblin
hp: 21
cr: 1
actions+:
  - name: Multiattack
    desc: "The elder goblin makes two scimitar attacks."
```
````

Use `actions+:` not `actions:` — `extends:` does not merge lists; a bare `actions:` replaces the parent's entire list.

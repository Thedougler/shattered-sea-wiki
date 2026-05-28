# Wiki DnD — Reference Page Authoring

Reference pages are mechanical condensations — not narrative entities. Precision and scannability over prose.

> **Prerequisite:** SKILL.md bootstrap complete — `wiki/index.md` and `CLAUDE.md` already read. Check `wiki/index.md` before creating any page.

---

## Condition Pages

Condition pages are mechanical references only.

**Interview (if needed):** Ruleset version, exact condition name, strict SRD mirror or campaign-adjusted wording?

### Frontmatter

```yaml
type: entity
subtype: condition
status: active
tags: [rule, condition]
sources: []
source_count: 0
confidence_level: canon
```

### Body Pattern

- H1 with condition name
- `## Rule Text`
- Lead sentence: `While you have the <Condition> condition, you experience the following effects.`
- Effect lines: `***Header.*** Rule sentence.`
- Optional `## Context` for table-specific clarifications

**Rule Fidelity:** Preserve mechanical intent and key thresholds exactly. Compact, scan-friendly. No lore language. One condition per page.

---

## Class Pages

Class pages are reference condensations of published mechanics.

**Interview (if needed):** Rules edition/source, class name, resource progression or spell-slot table emphasis?

### Frontmatter

```yaml
type: concept
subtype: class
status: active
tags: [reference, class, <class-identifier>]
sources: []
source_count: 0
confidence_level: canon
cssclasses: [wiki-reference]
```

### Body Pattern

- H1 with class name
- Italic source line: `*Class — Source*`
- One-line mechanical profile using bold labels: Primary Ability, Hit Die, Saves, Armor, Weapons, Spellcasting
- `---`
- Progression section: resource progression text OR `Spell Slots by Level` table
- `## Core Features` level table
- `## Subclasses`
- `## Connections`

**Rule Fidelity:** Mechanical thresholds and progression breakpoints exact to source. Table-first, no narrative prose. One class per page.

---

## Rule Pages

Rule pages are reference digests for mechanics and campaign implementation notes.

**Interview (if needed):** Source book/version, rule scope, strict summary or campaign adaptation?

### Frontmatter

```yaml
type: concept
subtype: rule
status: active
tags: [rule, reference]
sources: []
source_count: 0
confidence_level: canon
```

### Body Pattern

- H1 with rule name
- `## Rule Text` as primary section
- `###` subsections for components/mechanics
- Markdown tables for enumerations and progression
- Optional `## Context` for campaign-specific adaptation notes
- `## Connections` to related rules/entities

**Rule Fidelity:** Preserve mechanical intent and thresholds. Implementation-first wording. One rule system/topic per page; split by subsystem when oversized.

---

## Filing

File to the appropriate reference directory per `wiki-core/SKILL.md` vault structure. Run vault filing sequence from `../PREP.md` § Vault Filing after writing.

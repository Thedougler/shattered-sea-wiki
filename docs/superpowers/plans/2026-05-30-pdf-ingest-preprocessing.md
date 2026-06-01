# PDF Ingest Preprocessing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically preprocess PDF character sheets into agent-readable markdown before ingestion, so agents process structured text instead of raw binary.

**Architecture:** A new `preprocess_pdf.py` script extracts form fields and text from PDFs using pymupdf, maps D&D 5e character sheet fields to a structured markdown template, and writes a `.md` sidecar file alongside the original. The `check_ingest.py --batch` pipeline calls this preprocessor before batch assembly, so by the time the agent sees a PDF source, it reads the markdown and archives both files together.

**Tech Stack:** pymupdf (already installed), Python stdlib. No new system dependencies.

---

### Task 1: Create `preprocess_pdf.py` — form field extraction

**Files:**
- Create: `.claude/scripts/preprocess_pdf.py`

The core challenge with D&D character sheet PDFs: the real data lives in **form fields** (widgets), not in the page text. Standard text extraction returns just field labels ("STR", "DEX") without values. The script must extract widgets and map them to a structured markdown document.

Field names in the standard 5e PDF follow a known convention (e.g. `CharacterName`, `STR`, `DEXmod`, `ClassLevel`, `Wpn Name`, `AttacksSpellcasting`, `Features and Traits`). The script should handle these gracefully, but also work for non-standard PDFs by falling back to raw text extraction.

- [ ] **Step 1: Create the script with form field extraction**

```python
#!/usr/bin/env python3
"""Preprocess a PDF into an agent-readable markdown sidecar.

Extracts form fields (for D&D character sheets) and page text, producing a
structured .md file that contains all information from the PDF in a format
agents can search, decompose, and cross-link. The PDF becomes a sidecar
archived alongside the markdown.

Auto-installs pymupdf if missing.

Usage:
    preprocess_pdf.py Inbox/path/to/Character.pdf [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

try:
    import fitz
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "pymupdf"],
        stdout=subprocess.DEVNULL,
    )
    import fitz


# Standard 5e character sheet field names grouped by section.
# Maps field_name -> display label. Ordering within each group matters for output.
ABILITY_FIELDS = [
    ("STR", "Strength"), ("STRmod", "STR Modifier"),
    ("DEX", "Dexterity"), ("DEXmod", "DEX Modifier"),
    ("CON", "Constitution"), ("CONmod", "CON Modifier"),
    ("INT", "Intelligence"), ("INTmod", "INT Modifier"),
    ("WIS", "Wisdom"), ("WISmod", "WIS Modifier"),
    ("CHA", "Charisma"), ("CHamod", "CHA Modifier"),
]

SAVE_FIELDS = [
    ("ST Strength", "Strength Save"),
    ("ST Dexterity", "Dexterity Save"),
    ("ST Constitution", "Constitution Save"),
    ("ST Intelligence", "Intelligence Save"),
    ("ST Wisdom", "Wisdom Save"),
    ("ST Charisma", "Charisma Save"),
]

SKILL_FIELDS = [
    ("Acrobatics", "Acrobatics (Dex)"),
    ("Animal", "Animal Handling (Wis)"),
    ("Arcana", "Arcana (Int)"),
    ("Athletics", "Athletics (Str)"),
    ("Deception", "Deception (Cha)"),
    ("History", "History (Int)"),
    ("Insight", "Insight (Wis)"),
    ("Intimidation", "Intimidation (Cha)"),
    ("Investigation", "Investigation (Int)"),
    ("Medicine", "Medicine (Wis)"),
    ("Nature", "Nature (Int)"),
    ("Perception", "Perception (Wis)"),
    ("Performance", "Performance (Cha)"),
    ("Persuasion", "Persuasion (Cha)"),
    ("Religion", "Religion (Int)"),
    ("SleightofHand", "Sleight of Hand (Dex)"),
    ("Stealth", "Stealth (Dex)"),
    ("Survival", "Survival (Wis)"),
]

COMBAT_FIELDS = [
    ("AC", "Armor Class"),
    ("Initiative", "Initiative"),
    ("Speed", "Speed"),
    ("HPMax", "HP Maximum"),
    ("HPCurrent", "HP Current"),
    ("HDTotal", "Hit Dice Total"),
    ("HD", "Hit Dice"),
]

WEAPON_FIELD_SETS = [
    [("Wpn Name", "Name"), ("Wpn1 AtkBonus", "Attack Bonus"), ("Wpn1 Damage", "Damage")],
    [("Wpn Name 2", "Name"), ("Wpn2 AtkBonus", "Attack Bonus"), ("Wpn2 Damage", "Damage")],
    [("Wpn Name 3", "Name"), ("Wpn3 AtkBonus", "Attack Bonus"), ("Wpn3 Damage", "Damage")],
]

IDENTITY_FIELDS = [
    ("CharacterName", "Character Name"),
    ("ClassLevel", "Class & Level"),
    ("Race", "Race"),
    ("Background", "Background"),
    ("Alignment", "Alignment"),
    ("PlayerName", "Player Name"),
    ("XP", "Experience Points"),
]

PERSONALITY_FIELDS = [
    ("PersonalityTraits", "Personality Traits"),
    ("Ideals", "Ideals"),
    ("Bonds", "Bonds"),
    ("Flaws", "Flaws"),
]

PROSE_FIELDS = [
    ("Features and Traits", "Features & Traits"),
    ("Feat+Traits", "Additional Features & Traits"),
    ("AttacksSpellcasting", "Attacks & Spellcasting Notes"),
    ("ProficienciesLang", "Proficiencies & Languages"),
    ("Equipment", "Equipment"),
    ("Backstory", "Backstory"),
    ("Allies", "Allies & Organizations"),
    ("Treasure", "Treasure"),
]


def extract_fields(doc: fitz.Document) -> dict[str, str]:
    """Extract all form field values from every page."""
    fields: dict[str, str] = {}
    for page in doc:
        for widget in page.widgets():
            name = widget.field_name or ""
            value = (widget.field_value or "").strip()
            if name and value and value.lower() != "off":
                fields[name] = value
    return fields


def extract_text(doc: fitz.Document) -> str:
    """Extract raw page text as fallback for non-form PDFs."""
    parts = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            parts.append(f"## Page {i + 1}\n\n{text}")
    return "\n\n".join(parts)


def format_field_group(
    fields: dict[str, str],
    mapping: list[tuple[str, str]],
    used: set[str],
) -> list[str]:
    """Format a group of fields as `| Label | Value |` rows, tracking used keys."""
    rows = []
    for key, label in mapping:
        val = fields.get(key, "")
        if val:
            rows.append(f"| {label} | {val} |")
            used.add(key)
    return rows


def format_prose_field(
    fields: dict[str, str],
    key: str,
    heading: str,
    used: set[str],
) -> str | None:
    """Format a long-text field as a heading + body paragraph."""
    val = fields.get(key, "").strip()
    if not val:
        return None
    used.add(key)
    return f"### {heading}\n\n{val}"


def render_character_sheet(fields: dict[str, str], pdf_basename: str) -> str:
    """Render extracted fields into structured markdown."""
    used: set[str] = set()
    sections: list[str] = []

    # Identity / header
    char_name = fields.get("CharacterName", "Unknown Character")
    used.add("CharacterName")

    fm_lines = [
        "---",
        f"title: \"{char_name}\"",
        "category: character-sheet",
        "type: entity-source",
        "audience: dm",
        "publish: false",
        f"pdf_sidecar: \"{pdf_basename}\"",
        "---",
    ]
    sections.append("\n".join(fm_lines))
    sections.append(f"# {char_name}\n")

    # Identity table
    id_rows = format_field_group(fields, IDENTITY_FIELDS, used)
    if id_rows:
        sections.append("## Identity\n")
        sections.append("| Field | Value |\n|---|---|")
        sections.append("\n".join(id_rows))

    # Ability scores
    ab_rows = format_field_group(fields, ABILITY_FIELDS, used)
    if ab_rows:
        sections.append("\n## Ability Scores\n")
        sections.append("| Ability | Value |\n|---|---|")
        sections.append("\n".join(ab_rows))

    # Saves
    save_rows = format_field_group(fields, SAVE_FIELDS, used)
    if save_rows:
        sections.append("\n## Saving Throws\n")
        sections.append("| Save | Modifier |\n|---|---|")
        sections.append("\n".join(save_rows))

    # Skills
    skill_rows = format_field_group(fields, SKILL_FIELDS, used)
    if skill_rows:
        sections.append("\n## Skills\n")
        sections.append("| Skill | Modifier |\n|---|---|")
        sections.append("\n".join(skill_rows))

    # Proficiency bonus and passive perception
    misc_rows = []
    for key, label in [("ProfBonus", "Proficiency Bonus"), ("Passive", "Passive Perception")]:
        val = fields.get(key, "")
        if val:
            misc_rows.append(f"| {label} | {val} |")
            used.add(key)
    if misc_rows:
        sections.append("\n## Miscellaneous\n")
        sections.append("| Field | Value |\n|---|---|")
        sections.append("\n".join(misc_rows))

    # Combat
    combat_rows = format_field_group(fields, COMBAT_FIELDS, used)
    if combat_rows:
        sections.append("\n## Combat\n")
        sections.append("| Stat | Value |\n|---|---|")
        sections.append("\n".join(combat_rows))

    # Weapons
    for weapon_set in WEAPON_FIELD_SETS:
        w_rows = format_field_group(fields, weapon_set, used)
        if w_rows:
            weapon_name = fields.get(weapon_set[0][0], "Weapon")
            sections.append(f"\n### {weapon_name}\n")
            sections.append("| Field | Value |\n|---|---|")
            sections.append("\n".join(w_rows))

    # Personality
    for key, heading in PERSONALITY_FIELDS:
        block = format_prose_field(fields, key, heading, used)
        if block:
            sections.append(f"\n{block}")

    # Prose sections
    sections.append("\n## Character Details\n")
    for key, heading in PROSE_FIELDS:
        block = format_prose_field(fields, key, heading, used)
        if block:
            sections.append(block)

    # Remaining fields not covered by the template
    remaining = {k: v for k, v in fields.items() if k not in used and not k.startswith("Check Box")}
    if remaining:
        sections.append("\n## Other Fields\n")
        sections.append("| Field | Value |\n|---|---|")
        for k in sorted(remaining):
            sections.append(f"| {k} | {remaining[k]} |")

    return "\n".join(sections)


def preprocess_pdf(pdf_path: str, dry_run: bool = False) -> str | None:
    """Convert a PDF to a markdown sidecar. Returns the .md path, or None."""
    doc = fitz.open(pdf_path)

    fields = extract_fields(doc)
    pdf_basename = os.path.basename(pdf_path)

    if fields:
        content = render_character_sheet(fields, pdf_basename)
    else:
        raw_text = extract_text(doc)
        if not raw_text.strip():
            return None
        fm = "\n".join([
            "---",
            f"title: \"{os.path.splitext(pdf_basename)[0]}\"",
            "category: pdf-extract",
            "type: entity-source",
            "audience: dm",
            "publish: false",
            f"pdf_sidecar: \"{pdf_basename}\"",
            "---",
        ])
        content = f"{fm}\n\n# {os.path.splitext(pdf_basename)[0]}\n\n{raw_text}"

    doc.close()

    md_path = os.path.splitext(pdf_path)[0] + ".md"
    if dry_run:
        print(f"would write: {md_path} ({len(content)} chars)")
        return md_path

    with open(md_path, "w") as fh:
        fh.write(content)
    return md_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Preprocess a PDF into agent-readable markdown."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.pdf):
        sys.stderr.write(f"preprocess_pdf: not found — {args.pdf}\n")
        return 1

    result = preprocess_pdf(args.pdf, dry_run=args.dry_run)
    if result:
        print(result)
        return 0
    else:
        sys.stderr.write(f"preprocess_pdf: no extractable content — {args.pdf}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 2: Test against both PDFs**

Run:
```bash
python3 .claude/scripts/preprocess_pdf.py "Inbox/private/players/perrin/Perrin Black-Jaw.pdf" --dry-run
python3 .claude/scripts/preprocess_pdf.py "Inbox/private/players/delmar/Admiral Delmar Fisk.pdf" --dry-run
```

Expected: prints the .md path and character count for each.

- [ ] **Step 3: Run for real and inspect output**

```bash
python3 .claude/scripts/preprocess_pdf.py "Inbox/private/players/perrin/Perrin Black-Jaw.pdf"
head -60 "Inbox/private/players/perrin/Perrin Black-Jaw.md"
```

Expected: structured markdown with frontmatter, ability scores table, skills, equipment, backstory.

- [ ] **Step 4: Commit**

```bash
git add .claude/scripts/preprocess_pdf.py
git commit -m "feat: add preprocess_pdf.py for character sheet extraction"
```

---

### Task 2: Integrate preprocessing into `check_ingest.py --batch`

**Files:**
- Modify: `.claude/scripts/check_ingest.py`

PDFs should be preprocessed automatically when `--batch` runs. Before batch assembly, the script finds any `.pdf` files in the pending list that don't already have a `.md` sidecar, runs `preprocess_pdf.py` on them, and replaces the PDF path with the `.md` path in the queue. The PDF stays in Inbox/ as a sidecar — it's not in the queue itself.

- [ ] **Step 1: Add PDF preprocessing to the batch path**

In `check_ingest.py`, after the `expanded` list is built (where oversized markdown chunking happens), add a PDF preprocessing pass:

```python
# In the --batch block, after the chunking loop and before the sort:

preprocessed_pdfs: list[tuple[str, str]] = []  # (md_path, pdf_path)
final: list[str] = []
for path in expanded:
    if path.lower().endswith(".pdf"):
        md_path = os.path.splitext(path)[0] + ".md"
        if not os.path.exists(md_path):
            from preprocess_pdf import preprocess_pdf as _preprocess
            result = _preprocess(path)
            if result:
                sys.stderr.write(
                    f"check_ingest: preprocessed {display_path(path)} -> "
                    f"{display_path(result)}\n"
                )
                preprocessed_pdfs.append((result, path))
                final.append(result)
                continue
        else:
            final.append(md_path)
            continue
    final.append(path)

expanded = final
```

- [ ] **Step 2: Test the integration**

```bash
# Remove any previous .md sidecar to test fresh preprocessing
rm -f "Inbox/private/players/perrin/Perrin Black-Jaw.md"
python3 .claude/scripts/check_ingest.py --batch --no-dedupe 2>&1
```

Expected stderr: `check_ingest: preprocessed Inbox/private/players/perrin/Perrin Black-Jaw.pdf -> Inbox/private/players/perrin/Perrin Black-Jaw.md`
Expected stdout: the `.md` path appears in the batch, not the `.pdf`.

- [ ] **Step 3: Commit**

```bash
git add .claude/scripts/check_ingest.py
git commit -m "feat: auto-preprocess PDFs to markdown during --batch"
```

---

### Task 3: Update `archive_source.py` to handle PDF sidecars

**Files:**
- Modify: `.claude/scripts/archive_source.py`

When archiving a `.md` file that has a `pdf_sidecar:` field in its frontmatter, the script should also archive the PDF alongside it. Both files move to `.raw/<type>/` together.

- [ ] **Step 1: Add sidecar detection to `archive_source.py`**

After the existing `src_abs` resolution, add:

```python
def find_pdf_sidecar(md_path: str) -> str | None:
    """If the markdown has a pdf_sidecar frontmatter field, return the PDF path."""
    if not md_path.endswith(".md"):
        return None
    try:
        with open(md_path) as fh:
            in_fm = False
            for line in fh:
                if line.strip() == "---":
                    if in_fm:
                        break
                    in_fm = True
                    continue
                if in_fm and line.startswith("pdf_sidecar:"):
                    pdf_name = line.split(":", 1)[1].strip().strip('"').strip("'")
                    pdf_path = os.path.join(os.path.dirname(md_path), pdf_name)
                    if os.path.isfile(pdf_path):
                        return pdf_path
    except Exception:
        pass
    return None
```

Then in `main()`, after archiving the primary source, check for and archive the sidecar:

```python
# After the primary git mv succeeds:
sidecar = find_pdf_sidecar(src_abs)
if sidecar:
    sidecar_rel = rel(sidecar)
    sidecar_dest_rel = f".raw/{subdir}/{os.path.basename(sidecar)}"
    sidecar_dest_abs = os.path.join(REPO_ROOT, sidecar_dest_rel)
    if not os.path.exists(sidecar_dest_abs):
        os.makedirs(os.path.dirname(sidecar_dest_abs), exist_ok=True)
        r = git("mv", sidecar_rel, sidecar_dest_rel, check=False)
        if r.returncode != 0:
            os.rename(sidecar, sidecar_dest_abs)
            git("add", sidecar_rel, sidecar_dest_rel, check=False)
        print(f"archived sidecar {sidecar_rel} -> {sidecar_dest_rel}")
```

- [ ] **Step 2: Test sidecar archival**

```bash
python3 .claude/scripts/archive_source.py "Inbox/private/players/perrin/Perrin Black-Jaw.md" --type entity-source --dry-run
```

Expected: reports both the `.md` and `.pdf` moves.

- [ ] **Step 3: Commit**

```bash
git add .claude/scripts/archive_source.py
git commit -m "feat: archive PDF sidecars alongside preprocessed markdown"
```

---

### Task 4: Update `check_ingest.py` to exclude PDF sidecars from the queue

**Files:**
- Modify: `.claude/scripts/check_ingest.py`

After preprocessing, the PDF has a `.md` sibling. The `.md` file is the queue entry; the PDF should not appear independently. In `classify_inbox`, skip any `.pdf` file that has a corresponding `.md` sibling already present.

- [ ] **Step 1: Filter PDFs with existing markdown sidecars from pending**

In `classify_inbox`, after building the `pending` list (after the dedup loop), add:

```python
# Filter out PDFs that have a preprocessed .md sidecar
pending = [
    p for p in pending
    if not (
        p.lower().endswith(".pdf")
        and os.path.isfile(os.path.splitext(p)[0] + ".md")
    )
]
```

- [ ] **Step 2: Test that PDFs with sidecars don't appear in queue**

```bash
# Ensure both .pdf and .md exist
ls "Inbox/private/players/perrin/Perrin Black-Jaw".*
python3 .claude/scripts/check_ingest.py --no-dedupe 2>&1 | grep -i perrin
```

Expected: only the `.md` path appears, not the `.pdf`.

- [ ] **Step 3: Commit**

```bash
git add .claude/scripts/check_ingest.py
git commit -m "fix: exclude PDFs from queue when markdown sidecar exists"
```

---

### Task 5: Add `character-sheet` source type to triage and archive

**Files:**
- Modify: `.claude/skills/ttrpg-wiki-ingest/references/source-triage.md`
- Modify: `.claude/scripts/archive_source.py`

- [ ] **Step 1: Add character-sheet type to source-triage.md**

Add to the Source Types table:

```markdown
| `character-sheet` | PDF form fields, ability scores, class/level, equipment | PC sheet page, combat reference, entity links |
```

- [ ] **Step 2: Add character-sheet mapping to archive_source.py**

In `TYPE_TO_SUBDIR`, add:

```python
("character-sheet", "characters"),
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ttrpg-wiki-ingest/references/source-triage.md .claude/scripts/archive_source.py
git commit -m "feat: add character-sheet source type for PDF character sheets"
```

---

### Task 6: Update the ingest skill documentation

**Files:**
- Modify: `.claude/skills/ttrpg-wiki-ingest/SKILL.md`

- [ ] **Step 1: Update the batch description to mention PDF preprocessing**

Replace the paragraph about binary files in the "1+ pending" section:

```markdown
Oversized markdown files (over the budget) are automatically chunked by `##` headings into
parts that fit. Each chunk keeps the original frontmatter and is processed as a separate
source. The original is hidden until all chunks are handled.

PDF files are automatically preprocessed into agent-readable markdown before batch assembly.
The script extracts form fields (for D&D character sheets) or page text, writes a structured
`.md` sidecar, and queues the markdown instead of the PDF. The PDF travels alongside the
markdown as a sidecar — it is the player-facing view; the markdown is the agent-optimized
translation. Both are archived together.
```

- [ ] **Step 2: Add character-sheet to the domain skill chain table**

```markdown
| PC character sheet (PDF) | `prep-npc` (for the wiki entity page) |
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ttrpg-wiki-ingest/SKILL.md
git commit -m "docs: update ingest skill for PDF preprocessing and sidecar archival"
```

---

### Task 7: End-to-end verification

- [ ] **Step 1: Clean slate test**

```bash
# Remove any previous preprocessing artifacts
rm -f "Inbox/private/players/perrin/Perrin Black-Jaw.md"
rm -f "Inbox/private/players/delmar/Admiral Delmar Fisk.md"

# Run the full pipeline
python3 .claude/scripts/check_ingest.py --count
python3 .claude/scripts/check_ingest.py --batch 2>&1
```

Expected stderr: preprocessing messages for both PDFs. Expected stdout: `.md` paths, not `.pdf` paths.

- [ ] **Step 2: Verify markdown quality**

```bash
head -80 "Inbox/private/players/perrin/Perrin Black-Jaw.md"
```

Expected: frontmatter with `pdf_sidecar`, ability scores table, skills, equipment, backstory.

- [ ] **Step 3: Verify archive handles sidecar**

```bash
python3 .claude/scripts/archive_source.py "Inbox/private/players/perrin/Perrin Black-Jaw.md" --type character-sheet --dry-run
```

Expected: reports both `.md` and `.pdf` would be moved to `.raw/characters/`.

- [ ] **Step 4: Verify PDF excluded from queue after preprocessing**

```bash
python3 .claude/scripts/check_ingest.py --no-dedupe 2>&1 | grep -c "\.pdf"
```

Expected: `0` (no raw PDFs in queue).

#!/usr/bin/env python3
"""Extract D&D 5e character sheet form fields from a PDF into structured markdown.

Reads PDF widget (form-field) data — the actual filled-in values, not just
printed labels — and writes a .md sidecar file in the same directory.

Falls back to raw page-text extraction for PDFs without form fields.

Usage:
    preprocess_pdf.py <path.pdf> [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
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


# ---------------------------------------------------------------------------
# Field extraction
# ---------------------------------------------------------------------------


def extract_fields(pdf_path: str) -> dict[str, str]:
    """Return {field_name: field_value} for all populated widgets in the PDF."""
    doc = fitz.open(pdf_path)
    fields: dict[str, str] = {}
    for page in doc:
        for widget in page.widgets():
            name = (widget.field_name or "").strip()
            value = (widget.field_value or "").strip()
            if not name or not value or value == "Off":
                continue
            if name not in fields:
                fields[name] = value
    doc.close()
    return fields


def extract_raw_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append(f"## Page {i + 1}\n\n{text}")
    doc.close()
    return "\n\n".join(pages)


# ---------------------------------------------------------------------------
# Field lookup helpers — handles the naming inconsistencies across PDF sources
# ---------------------------------------------------------------------------


def _get(fields: dict[str, str], *candidates: str) -> str:
    """Return the first non-empty match from candidate field names."""
    for key in candidates:
        val = fields.get(key, "").strip()
        if val:
            return val
    return ""


def _pop(fields: dict[str, str], *candidates: str) -> str:
    """Like _get but also removes matched keys from the dict."""
    for key in candidates:
        val = fields.pop(key, "").strip()
        if val:
            for other in candidates:
                fields.pop(other, None)
            return val
    return ""


def _pop_pattern(fields: dict[str, str], pattern: str) -> dict[str, str]:
    """Pop and return all keys matching a regex pattern."""
    regex = re.compile(pattern, re.IGNORECASE)
    matched = {}
    for key in list(fields):
        if regex.search(key):
            matched[key] = fields.pop(key)
    return matched


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

SKILL_NAMES = [
    "Acrobatics",
    "Animal",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Performance",
    "Persuasion",
    "Religion",
    "SleightofHand",
    "Stealth",
    "Survival",
]

SKILL_DISPLAY = {
    "Animal": "Animal Handling",
    "SleightofHand": "Sleight of Hand",
}

ABILITY_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_MOD_KEYS = {
    "STR": ["STRmod"],
    "DEX": ["DEXmod", "DEXmod "],
    "CON": ["CONmod"],
    "INT": ["INTmod"],
    "WIS": ["WISmod"],
    "CHA": ["CHamod", "CHAmod"],
}

SAVE_KEYS = {
    "STR": "ST Strength",
    "DEX": "ST Dexterity",
    "CON": "ST Constitution",
    "INT": "ST Intelligence",
    "WIS": "ST Wisdom",
    "CHA": "ST Charisma",
}


def _multiline_block(text: str) -> str:
    """Format a multi-line field value as a readable block."""
    return text.strip()


def build_character_markdown(fields: dict[str, str], pdf_filename: str) -> str:
    # Work on a copy so we can track consumed fields
    f = dict(fields)
    sections: list[str] = []

    char_name = _pop(f, "CharacterName")
    class_level = _pop(f, "ClassLevel", "CLASS  LEVEL")
    background = _pop(f, "Background", "BACKGROUND")
    player_name = _pop(f, "PlayerName", "PLAYER NAME")
    race = _pop(f, "Race ", "Race", "RACE")
    alignment = _pop(f, "Alignment", "ALIGNMENT")
    xp = _pop(f, "XP", "EXPERIENCE POINTS")

    # -- Frontmatter --
    safe_title = char_name or os.path.splitext(pdf_filename)[0]
    fm_lines = [
        "---",
        f'title: "{safe_title}"',
        "category: character-sheet",
        "type: entity-source",
        "audience: dm",
        "publish: false",
        f'pdf_sidecar: "{pdf_filename}"',
        "---",
    ]
    sections.append("\n".join(fm_lines))

    # -- Identity --
    identity_lines = [f"# {safe_title}", "", "## Identity", ""]
    identity_table = [
        ("Character", char_name),
        ("Class / Level", class_level),
        ("Background", background),
        ("Race", race),
        ("Alignment", alignment),
        ("Player", player_name),
        ("XP", xp),
    ]
    # Page-2+ duplicates of identity fields
    for key in list(f):
        if re.match(
            r"(CharacterName|CLASS  LEVEL|PLAYER NAME|RACE|BACKGROUND|EXPERIENCE POINTS)\d+$",
            key,
        ):
            f.pop(key)

    gender = _pop(f, "GENDER")
    age = _pop(f, "AGE")
    size = _pop(f, "SIZE")
    height = _pop(f, "HEIGHT")
    weight = _pop(f, "WEIGHT")
    faith = _pop(f, "FAITH")
    skin = _pop(f, "SKIN")
    eyes = _pop(f, "EYES")
    hair = _pop(f, "HAIR")

    appearance_fields = [
        ("Gender", gender),
        ("Age", age),
        ("Size", size),
        ("Height", height),
        ("Weight", weight),
        ("Faith", faith),
        ("Skin", skin),
        ("Eyes", eyes),
        ("Hair", hair),
    ]
    identity_table.extend((k, v) for k, v in appearance_fields if v)

    for label, val in identity_table:
        if val:
            identity_lines.append(f"- **{label}:** {val}")
    sections.append("\n".join(identity_lines))

    # -- Ability Scores --
    ability_rows = []
    for ab in ABILITY_NAMES:
        score = _pop(f, ab)
        mod = _pop(f, *ABILITY_MOD_KEYS[ab])
        if score or mod:
            ability_rows.append(f"| {ab} | {score} | {mod} |")
    if ability_rows:
        header = "## Ability Scores\n\n| Ability | Score | Mod |\n|---|---|---|"
        sections.append(header + "\n" + "\n".join(ability_rows))

    # -- Saving Throws --
    save_rows = []
    for ab in ABILITY_NAMES:
        key = SAVE_KEYS[ab]
        ab_title = ab.capitalize()
        prof = _pop(f, f"{ab_title}Prof", f"{ab}Prof", f"{ab.lower()}Prof")
        val = _pop(f, key)
        if val:
            prof_mark = "Yes" if prof else ""
            save_rows.append(f"| {ab} | {val} | {prof_mark} |")
    if save_rows:
        header = "## Saving Throws\n\n| Save | Bonus | Prof |\n|---|---|---|"
        sections.append(header + "\n" + "\n".join(save_rows))

    # -- Skills --
    skill_rows = []
    for sk in SKILL_NAMES:
        display = SKILL_DISPLAY.get(sk, sk)
        # Try with and without trailing space (Perrin's PDF has trailing spaces)
        val = _pop(f, sk, f"{sk} ", f"{sk}  ")
        # Handle casing variants: SleightofHand vs SleightOfHand
        prof = _pop(f, f"{sk}Prof", f"{sk.replace('of', 'Of')}Prof")
        mod_src = _pop(f, f"{sk}Mod", f"{sk.replace('of', 'Of')}Mod")
        if val:
            extras = []
            if prof:
                extras.append(f"Prof: {prof}")
            if mod_src:
                extras.append(f"({mod_src})")
            suffix = " " + " ".join(extras) if extras else ""
            skill_rows.append(f"| {display} | {val}{suffix} |")
    if skill_rows:
        header = "## Skills\n\n| Skill | Bonus |\n|---|---|"
        sections.append(header + "\n" + "\n".join(skill_rows))

    # -- Combat --
    prof_bonus = _pop(f, "ProfBonus")
    ac = _pop(f, "AC")
    init = _pop(f, "Initiative", "Init")
    speed = _pop(f, "Speed")
    hp = _pop(f, "HPCurrent", "MaxHP")
    temp_hp = _pop(f, "TempHP")
    hd = _pop(f, "HD", "Total")
    passive = _pop(f, "Passive", "Passive1")
    _pop(f, "Passive2", "Passive3")

    combat_stats = [
        ("Proficiency Bonus", prof_bonus),
        ("AC", ac),
        ("Initiative", init),
        ("Speed", speed),
        ("HP", hp),
        ("Temp HP", temp_hp),
        ("Hit Dice", hd),
        ("Passive Perception", passive),
    ]
    combat_lines = [f"- **{k}:** {v}" for k, v in combat_stats if v]
    if combat_lines:
        sections.append("## Combat\n\n" + "\n".join(combat_lines))

    # -- Weapons --
    weapon_blocks = []
    # Pattern 1: "Wpn Name", "Wpn1 AtkBonus", "Wpn1 Damage" (Perrin-style)
    # Pattern 2: "Wpn Name 2", "Wpn2 AtkBonus", "Wpn2 Damage" (Delmar-style)
    for i in range(1, 10):
        suffix = "" if i == 1 else f" {i}"
        num = str(i) if i > 1 else "1"
        name = _pop(f, f"Wpn Name{suffix}", f"Wpn Name{i}" if i > 1 else "Wpn Name")
        atk = _pop(
            f,
            f"Wpn{num} AtkBonus",
            f"Wpn{num} AtkBonus ",
            f"Wpn{num} AtkBonus  ",
            f"Wpn{num} AtkBonus   ",
        )
        dmg = _pop(f, f"Wpn{num} Damage", f"Wpn{num} Damage ")
        notes = _pop(f, f"Wpn Notes {i}", f"Wpn Notes{i}")
        if name:
            line = f"- **{name}:** Atk {atk}, Dmg {dmg}"
            if notes:
                line += f" ({notes})"
            weapon_blocks.append(line)
    if weapon_blocks:
        sections.append("## Weapons\n\n" + "\n".join(weapon_blocks))

    # -- Actions --
    actions = []
    for key in ["Actions1", "Actions2", "Actions3"]:
        val = _pop(f, key)
        if val:
            actions.append(val)
    if actions:
        sections.append(
            "## Actions\n\n" + "\n\n".join(_multiline_block(a) for a in actions)
        )

    # -- Personality --
    traits = _pop(f, "PersonalityTraits ", "PersonalityTraits")
    ideals = _pop(f, "Ideals", "Ideals ")
    bonds = _pop(f, "Bonds", "Bonds ")
    flaws = _pop(f, "Flaws", "Flaws ")
    personality_parts = []
    if traits:
        personality_parts.append(
            f"### Personality Traits\n\n{_multiline_block(traits)}"
        )
    if ideals:
        personality_parts.append(f"### Ideals\n\n{_multiline_block(ideals)}")
    if bonds:
        personality_parts.append(f"### Bonds\n\n{_multiline_block(bonds)}")
    if flaws:
        personality_parts.append(f"### Flaws\n\n{_multiline_block(flaws)}")
    if personality_parts:
        sections.append("## Personality\n\n" + "\n\n".join(personality_parts))

    # -- Features & Traits --
    feat_parts = []
    for key in [
        "Features and Traits",
        "Feat+Traits",
        "FeaturesTraits1",
        "FeaturesTraits2",
        "FeaturesTraits3",
        "FeaturesTraits4",
    ]:
        val = _pop(f, key)
        if val:
            feat_parts.append(_multiline_block(val))
    if feat_parts:
        sections.append("## Features and Traits\n\n" + "\n\n".join(feat_parts))

    # -- Proficiencies & Languages --
    prof_lang = _pop(f, "ProficienciesLang")
    if prof_lang:
        sections.append(
            f"## Proficiencies and Languages\n\n{_multiline_block(prof_lang)}"
        )

    # -- Equipment --
    equip_text = _pop(f, "Equipment")
    equip_items = _pop_pattern(f, r"^Eq (Name|Qty|Weight)\d+$")
    equip_parts = []
    if equip_text:
        equip_parts.append(_multiline_block(equip_text))
    if equip_items:
        # Group by index
        indexed: dict[int, dict[str, str]] = {}
        for key, val in equip_items.items():
            m = re.match(r"Eq (Name|Qty|Weight)(\d+)$", key)
            if m:
                idx = int(m.group(2))
                indexed.setdefault(idx, {})[m.group(1)] = val
        if indexed:
            table_lines = ["| Item | Qty | Weight |", "|---|---|---|"]
            for idx in sorted(indexed):
                row = indexed[idx]
                name = row.get("Name", "")
                qty = row.get("Qty", "")
                weight = row.get("Weight", "")
                if name:
                    table_lines.append(f"| {name} | {qty} | {weight} |")
            equip_parts.append("\n".join(table_lines))

    # Currency
    currency_keys = ["CP", "SP", "EP", "GP", "PP"]
    currency_vals = {k: _pop(f, k) for k in currency_keys}
    currency_vals = {k: v for k, v in currency_vals.items() if v}
    if currency_vals:
        equip_parts.append(
            "**Currency:** "
            + ", ".join(f"{v} {k.lower()}" for k, v in currency_vals.items())
        )

    carry_fields = []
    for key in ["Weight Carried", "Encumbered", "PushDragLift"]:
        val = _pop(f, key)
        if val:
            carry_fields.append(f"{key}: {val}")
    if carry_fields:
        equip_parts.append(" | ".join(carry_fields))

    if equip_parts:
        sections.append("## Equipment\n\n" + "\n\n".join(equip_parts))

    # -- Spellcasting / Attacks --
    atk_spell = _pop(f, "AttacksSpellcasting")
    if atk_spell:
        sections.append(f"## Attacks and Spellcasting\n\n{_multiline_block(atk_spell)}")

    # -- Backstory & Allies --
    backstory = _pop(f, "Backstory")
    allies = _pop(f, "Allies")
    treasure = _pop(f, "Treasure")
    if backstory:
        sections.append(f"## Backstory\n\n{_multiline_block(backstory)}")
    if allies:
        sections.append(f"## Allies\n\n{_multiline_block(allies)}")
    if treasure:
        sections.append(f"## Treasure\n\n{_multiline_block(treasure)}")

    # -- Cleanup: drop checkbox fields and page-N duplicates --
    for key in list(f):
        if re.match(r"Check Box \d+", key):
            f.pop(key)

    # -- Other Fields (catch-all) --
    if f:
        other_lines = ["## Other Fields", ""]
        for key in sorted(f):
            val = f[key]
            if "\n" in val:
                other_lines.append(f"### {key}\n\n{_multiline_block(val)}")
            else:
                other_lines.append(f"- **{key}:** {val}")
        sections.append("\n".join(other_lines))

    return "\n\n".join(sections) + "\n"


def build_raw_markdown(text: str, pdf_filename: str) -> str:
    stem = os.path.splitext(pdf_filename)[0]
    fm = "\n".join(
        [
            "---",
            f'title: "{stem}"',
            "category: pdf-extract",
            "type: entity-source",
            "audience: dm",
            "publish: false",
            f'pdf_sidecar: "{pdf_filename}"',
            "---",
        ]
    )
    return f"{fm}\n\n# {stem}\n\n{text}\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract D&D character sheet form fields from a PDF into markdown."
    )
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the markdown to stdout instead of writing a file",
    )
    args = parser.parse_args(argv)

    pdf_path = os.path.abspath(args.pdf)
    if not os.path.isfile(pdf_path):
        sys.stderr.write(f"preprocess_pdf: file not found: {pdf_path}\n")
        return 1

    pdf_filename = os.path.basename(pdf_path)
    fields = extract_fields(pdf_path)

    if fields:
        markdown = build_character_markdown(fields, pdf_filename)
        mode = "character-sheet"
    else:
        text = extract_raw_text(pdf_path)
        if not text:
            sys.stderr.write(
                f"preprocess_pdf: no form fields or text found in {pdf_filename}\n"
            )
            return 1
        markdown = build_raw_markdown(text, pdf_filename)
        mode = "raw-text"

    if args.dry_run:
        print(markdown)
        sys.stderr.write(f"preprocess_pdf: [{mode}] {pdf_filename} (dry run)\n")
        return 0

    stem = os.path.splitext(pdf_path)[0]
    out_path = stem + ".md"
    with open(out_path, "w") as fh:
        fh.write(markdown)
    sys.stderr.write(f"preprocess_pdf: [{mode}] wrote {out_path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

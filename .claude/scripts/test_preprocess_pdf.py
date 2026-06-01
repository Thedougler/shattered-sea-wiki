#!/usr/bin/env python3
"""Tests for preprocess_pdf.py — pure helper functions only (no real PDFs needed)."""

from __future__ import annotations

import unittest

import preprocess_pdf

# ---------------------------------------------------------------------------
# _get / _pop / _pop_pattern
# ---------------------------------------------------------------------------


class GetTests(unittest.TestCase):
    def test_returns_first_match(self):
        fields = {"STR": "18", "DEX": "14"}
        self.assertEqual(preprocess_pdf._get(fields, "STR", "DEX"), "18")

    def test_returns_second_when_first_empty(self):
        fields = {"STR": "", "DEX": "14"}
        self.assertEqual(preprocess_pdf._get(fields, "STR", "DEX"), "14")

    def test_returns_empty_when_none_match(self):
        fields = {"STR": "", "DEX": ""}
        self.assertEqual(preprocess_pdf._get(fields, "STR", "DEX"), "")

    def test_missing_key_returns_empty(self):
        fields = {}
        self.assertEqual(preprocess_pdf._get(fields, "MISSING"), "")

    def test_strips_whitespace(self):
        fields = {"key": "  value  "}
        self.assertEqual(preprocess_pdf._get(fields, "key"), "value")


class PopTests(unittest.TestCase):
    def test_pops_and_returns_first_match(self):
        fields = {"STR": "18", "DEX": "14"}
        result = preprocess_pdf._pop(fields, "STR", "DEX")
        self.assertEqual(result, "18")
        self.assertNotIn("STR", fields)
        self.assertNotIn("DEX", fields)  # other candidates removed too

    def test_pops_second_when_first_empty(self):
        fields = {"STR": "", "DEX": "14"}
        result = preprocess_pdf._pop(fields, "STR", "DEX")
        self.assertEqual(result, "14")
        self.assertNotIn("DEX", fields)

    def test_returns_empty_when_none(self):
        fields = {}
        result = preprocess_pdf._pop(fields, "MISSING")
        self.assertEqual(result, "")

    def test_strips_whitespace(self):
        fields = {"key": "  val  "}
        result = preprocess_pdf._pop(fields, "key")
        self.assertEqual(result, "val")


class PopPatternTests(unittest.TestCase):
    def test_pops_matching_keys(self):
        fields = {"Skill Acrobatics": "5", "Skill Athletics": "3", "Other": "x"}
        matched = preprocess_pdf._pop_pattern(fields, r"Skill\s+\w+")
        self.assertIn("Skill Acrobatics", matched)
        self.assertIn("Skill Athletics", matched)
        self.assertNotIn("Skill Acrobatics", fields)
        self.assertNotIn("Skill Athletics", fields)
        self.assertIn("Other", fields)

    def test_returns_empty_dict_when_no_match(self):
        fields = {"A": "1", "B": "2"}
        matched = preprocess_pdf._pop_pattern(fields, r"^ZZZNOMATCH")
        self.assertEqual(matched, {})

    def test_case_insensitive(self):
        fields = {"skill_str": "5"}
        matched = preprocess_pdf._pop_pattern(fields, r"SKILL")
        self.assertIn("skill_str", matched)


# ---------------------------------------------------------------------------
# _multiline_block
# ---------------------------------------------------------------------------


class MultilineBlockTests(unittest.TestCase):
    def test_strips_surrounding_whitespace(self):
        result = preprocess_pdf._multiline_block("  hello world  ")
        self.assertEqual(result, "hello world")

    def test_preserves_internal_newlines(self):
        text = "line one\nline two"
        result = preprocess_pdf._multiline_block(text)
        self.assertIn("line one", result)
        self.assertIn("line two", result)

    def test_empty_string(self):
        self.assertEqual(preprocess_pdf._multiline_block(""), "")


# ---------------------------------------------------------------------------
# SKILL_NAMES / ABILITY_NAMES constants
# ---------------------------------------------------------------------------


class ConstantsTests(unittest.TestCase):
    def test_skill_names_populated(self):
        self.assertGreater(len(preprocess_pdf.SKILL_NAMES), 10)
        self.assertIn("Acrobatics", preprocess_pdf.SKILL_NAMES)
        self.assertIn("Perception", preprocess_pdf.SKILL_NAMES)

    def test_ability_names(self):
        self.assertEqual(
            preprocess_pdf.ABILITY_NAMES, ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        )

    def test_skill_display_has_animal_handling(self):
        self.assertEqual(preprocess_pdf.SKILL_DISPLAY.get("Animal"), "Animal Handling")

    def test_save_keys_has_all_abilities(self):
        for ability in preprocess_pdf.ABILITY_NAMES:
            self.assertIn(ability, preprocess_pdf.SAVE_KEYS)


# ---------------------------------------------------------------------------
# main — file-not-found path
# ---------------------------------------------------------------------------


class MainTests(unittest.TestCase):
    def test_main_missing_file(self):
        import contextlib
        import io

        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                code = preprocess_pdf.main(["/nonexistent/path/sheet.pdf"])
            except SystemExit as e:
                code = e.code
        self.assertNotEqual(code, 0)

    def test_main_dry_run_missing_file(self):
        import contextlib
        import io

        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            try:
                code = preprocess_pdf.main(["/nonexistent/path/sheet.pdf", "--dry-run"])
            except SystemExit as e:
                code = e.code
        self.assertNotEqual(code, 0)

    def test_main_no_args(self):
        try:
            code = preprocess_pdf.main([])
        except SystemExit as e:
            code = e.code
        self.assertNotEqual(code, 0)


# ---------------------------------------------------------------------------
# build_raw_markdown
# ---------------------------------------------------------------------------


class BuildRawMarkdownTests(unittest.TestCase):
    def test_returns_string_with_frontmatter(self):
        result = preprocess_pdf.build_raw_markdown("Page text here.", "sheet.pdf")
        self.assertIn("---", result)
        self.assertIn("pdf_sidecar", result)
        self.assertIn("sheet.pdf", result)

    def test_includes_pdf_extract_category(self):
        result = preprocess_pdf.build_raw_markdown("Content", "my-sheet.pdf")
        self.assertIn("category: pdf-extract", result)

    def test_includes_page_text(self):
        result = preprocess_pdf.build_raw_markdown("Some page content", "sheet.pdf")
        self.assertIn("Some page content", result)

    def test_uses_stem_as_title(self):
        result = preprocess_pdf.build_raw_markdown("Content", "my-sheet.pdf")
        self.assertIn("# my-sheet", result)


# ---------------------------------------------------------------------------
# build_character_markdown
# ---------------------------------------------------------------------------


class BuildCharacterMarkdownTests(unittest.TestCase):
    def test_minimal_fields_produces_markdown(self):
        fields = {"CharacterName": "Bob"}
        result = preprocess_pdf.build_character_markdown(fields, "bob.pdf")
        self.assertIn("Bob", result)
        self.assertIn("---", result)

    def test_empty_fields_uses_filename(self):
        result = preprocess_pdf.build_character_markdown({}, "bob.pdf")
        self.assertIn("bob", result)

    def test_ability_scores_section(self):
        fields = {
            "STR": "18",
            "STRmod": "+4",
            "DEX": "14",
            "DEXmod": "+2",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Ability Scores", result)
        self.assertIn("18", result)

    def test_saving_throws_section(self):
        fields = {
            "ST Strength": "+5",
            "ST Dexterity": "+3",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Saving Throws", result)

    def test_skills_section(self):
        fields = {"Acrobatics": "+4"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Skills", result)
        self.assertIn("Acrobatics", result)

    def test_combat_section(self):
        fields = {"AC": "16", "HPCurrent": "45", "Speed": "30"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Combat", result)
        self.assertIn("AC", result)
        self.assertIn("16", result)

    def test_weapons_section(self):
        fields = {
            "Wpn Name": "Longsword",
            "Wpn1 AtkBonus": "+5",
            "Wpn1 Damage": "1d8+3",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Weapons", result)
        self.assertIn("Longsword", result)

    def test_personality_section(self):
        fields = {"PersonalityTraits": "Brave and bold.", "Ideals": "Honor above all."}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Personality", result)

    def test_actions_section(self):
        fields = {"Actions1": "Multiattack: two melee attacks."}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Actions", result)

    def test_proficiencies_section(self):
        fields = {"ProficienciesLang": "Common, Elvish"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Common, Elvish", result)

    def test_strips_duplicate_identity_fields(self):
        fields = {
            "CharacterName": "Bob",
            "CharacterName2": "Bob",  # duplicate page field
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Bob", result)

    def test_appearance_fields_included(self):
        fields = {
            "CharacterName": "Bob",
            "GENDER": "Male",
            "AGE": "25",
            "HEIGHT": "5'10\"",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Gender", result)
        self.assertIn("Age", result)

    def test_remaining_fields_dumped(self):
        fields = {
            "SomeUnknownField": "mystery value",
            "AnotherField": "another value",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        # Unknown fields go to a catch-all section
        self.assertIn("mystery value", result)

    def test_skill_display_name(self):
        fields = {"Animal": "+3"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Animal Handling", result)

    def test_sleight_of_hand_display(self):
        fields = {"SleightofHand": "+4"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Sleight of Hand", result)

    def test_skill_with_proficiency(self):
        fields = {"Acrobatics": "+4", "AcrobaticsProf": "Yes"}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Prof", result)

    def test_weapon_with_notes(self):
        fields = {
            "Wpn Name": "Bow",
            "Wpn1 AtkBonus": "+4",
            "Wpn1 Damage": "1d6",
            "Wpn Notes 1": "Ranged",
        }
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Ranged", result)

    def test_flaws_section(self):
        fields = {"Flaws": "Too proud."}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Flaws", result)
        self.assertIn("Too proud", result)

    def test_bonds_section(self):
        fields = {"Bonds": "My hometown."}
        result = preprocess_pdf.build_character_markdown(fields, "char.pdf")
        self.assertIn("Bonds", result)

    def test_full_character_sheet(self):
        fields = {
            "CharacterName": "Perrin Black-Jaw",
            "ClassLevel": "Rogue 5",
            "Background": "Sailor",
            "Race ": "Rattkin",
            "Alignment": "Chaotic Good",
            "STR": "10",
            "STRmod": "+0",
            "DEX": "18",
            "DEXmod": "+4",
            "CON": "14",
            "CONmod": "+2",
            "INT": "12",
            "INTmod": "+1",
            "WIS": "10",
            "WISmod": "+0",
            "CHA": "16",
            "CHamod": "+3",
            "ST Strength": "+0",
            "ST Dexterity": "+7",
            "AC": "15",
            "HPCurrent": "38",
            "Speed": "30",
            "Acrobatics": "+7",
            "PersonalityTraits": "Never pays full price.",
            "Ideals": "Freedom.",
        }
        result = preprocess_pdf.build_character_markdown(fields, "perrin.pdf")
        self.assertIn("Perrin Black-Jaw", result)
        self.assertIn("DEX", result)
        self.assertIn("Rogue", result)


if __name__ == "__main__":
    unittest.main()

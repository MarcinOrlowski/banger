"""
##################################################################################
#
# Bänger by Marcin Orlowski
# Because your `banner` deserves to be a `bänger`!
#
# @author    Marcin Orlowski <mail@marcinOrlowski.com>
# Copyright  ©2025 Marcin Orlowski <MarcinOrlowski.com>
# @link      https://github.com/MarcinOrlowski/banger
#
##################################################################################
"""

import unittest

from banger.fonts import (
    get_available_fonts,
    validate_font_character_coverage,
    get_all_fonts_validation_report,
    MANDATORY_CHARACTERS,
)

"""Tests for font character validation and mandatory character coverage."""


class TestFontCharacterValidation(unittest.TestCase):
    """Test font character validation functionality."""

    def test_mandatory_characters_set_is_comprehensive(self):
        """Test that MANDATORY_CHARACTERS contains expected character types."""
        # Check that mandatory characters include all expected categories
        digits = set("0123456789")
        uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        lowercase = set("abcdefghijklmnopqrstuvwxyz")
        space = {" "}

        # Verify all categories are present
        self.assertTrue(
            digits.issubset(MANDATORY_CHARACTERS),
            "Missing digits in mandatory characters",
        )
        self.assertTrue(
            uppercase.issubset(MANDATORY_CHARACTERS),
            "Missing uppercase letters in mandatory characters",
        )
        self.assertTrue(
            lowercase.issubset(MANDATORY_CHARACTERS),
            "Missing lowercase letters in mandatory characters",
        )
        self.assertTrue(
            space.issubset(MANDATORY_CHARACTERS),
            "Missing space character in mandatory characters",
        )

        # Verify minimum expected size (at least 63 core characters)
        self.assertGreaterEqual(
            len(MANDATORY_CHARACTERS),
            63,
            f"Expected at least 63 mandatory characters, got {len(MANDATORY_CHARACTERS)}",
        )

    def test_validate_font_character_coverage_structure(self):
        """Test that font validation returns expected data structure."""
        # Test with default font (should be complete)
        result = validate_font_character_coverage("default")

        # Check required keys are present
        required_keys = {
            "font",
            "total_mandatory",
            "available",
            "missing",
            "missing_characters",
            "coverage_percentage",
            "is_complete",
        }
        self.assertEqual(set(result.keys()), required_keys)

        # Check data types
        self.assertIsInstance(result["font"], str)
        self.assertIsInstance(result["total_mandatory"], int)
        self.assertIsInstance(result["available"], int)
        self.assertIsInstance(result["missing"], int)
        self.assertIsInstance(result["missing_characters"], list)
        self.assertIsInstance(result["coverage_percentage"], (int, float))
        self.assertIsInstance(result["is_complete"], bool)

        # Check logical consistency
        self.assertEqual(result["total_mandatory"], len(MANDATORY_CHARACTERS))
        self.assertEqual(
            result["available"] + result["missing"], result["total_mandatory"]
        )
        self.assertEqual(result["missing"], len(result["missing_characters"]))
        self.assertTrue(0 <= result["coverage_percentage"] <= 100)

    def test_default_font_completeness(self):
        """Test that default font has complete character coverage."""
        result = validate_font_character_coverage("default")

        self.assertTrue(
            result["is_complete"],
            f"Default font is missing characters: {result['missing_characters']}",
        )
        self.assertEqual(result["coverage_percentage"], 100.0)
        self.assertEqual(result["missing"], 0)
        self.assertEqual(len(result["missing_characters"]), 0)

    def test_all_fonts_have_space_character(self):
        """Test that all fonts include the space character."""
        available_fonts = get_available_fonts()

        for font_name in available_fonts:
            result = validate_font_character_coverage(font_name)
            self.assertNotIn(
                " ",
                result["missing_characters"],
                f"Font '{font_name}' is missing space character",
            )

    def test_all_fonts_have_digits(self):
        """Test that JSON fonts include all digits."""
        available_fonts = get_available_fonts()
        digits = set("0123456789")

        # Only test original JSON fonts for complete digit coverage
        json_fonts = [
            "default",
            "block",
            "blur",
            "compact",
            "fire",
            "quadrant",
            "small",
        ]

        for font_name in available_fonts:
            if font_name in json_fonts:
                result = validate_font_character_coverage(font_name)
                missing_digits = digits.intersection(set(result["missing_characters"]))
                self.assertEqual(
                    len(missing_digits),
                    0,
                    f"JSON font '{font_name}' is missing digits: {missing_digits}",
                )

    def test_all_fonts_have_uppercase_letters(self):
        """Test that JSON fonts include all uppercase letters."""
        available_fonts = get_available_fonts()
        uppercase = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Only test original JSON fonts for complete uppercase coverage
        json_fonts = [
            "default",
            "block",
            "blur",
            "compact",
            "fire",
            "quadrant",
            "small",
        ]

        for font_name in available_fonts:
            if font_name in json_fonts:
                result = validate_font_character_coverage(font_name)
                missing_uppercase = uppercase.intersection(
                    set(result["missing_characters"])
                )
                self.assertEqual(
                    len(missing_uppercase),
                    0,
                    f"JSON font '{font_name}' is missing uppercase letters: {missing_uppercase}",
                )

    def test_get_all_fonts_validation_report(self):
        """Test comprehensive validation report for all fonts."""
        report = get_all_fonts_validation_report()
        available_fonts = get_available_fonts()

        # Check that report covers all available fonts
        self.assertEqual(set(report.keys()), set(available_fonts))

        # Check that each font report has valid structure
        for font_name, font_report in report.items():
            self.assertEqual(font_report["font"], font_name)
            self.assertIsInstance(font_report["coverage_percentage"], (int, float))
            self.assertTrue(0 <= font_report["coverage_percentage"] <= 100)

    def test_critical_characters_coverage(self):
        """Test that JSON fonts have critical characters for basic functionality."""
        available_fonts = get_available_fonts()

        # Define absolutely critical characters that every JSON font MUST have
        critical_chars = {
            " ",  # Space - essential for word separation
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",  # Uppercase
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",  # Digits
        }

        # Only test original JSON fonts for complete critical character coverage
        json_fonts = [
            "default",
            "block",
            "blur",
            "compact",
            "fire",
            "quadrant",
            "small",
        ]

        for font_name in available_fonts:
            if font_name in json_fonts:
                result = validate_font_character_coverage(font_name)
                missing_critical = critical_chars.intersection(
                    set(result["missing_characters"])
                )
                self.assertEqual(
                    len(missing_critical),
                    0,
                    f"JSON font '{font_name}' is missing critical characters: {missing_critical}",
                )

    def test_font_validation_with_invalid_font(self):
        """Test validation behavior with non-existent font."""
        result = validate_font_character_coverage("nonexistent_font")

        # With new font system, non-existent fonts correctly return 0% coverage
        self.assertEqual(result["font"], "nonexistent_font")
        self.assertEqual(result["coverage_percentage"], 0.0)
        self.assertFalse(result["is_complete"])
        self.assertEqual(result["available"], 0)

    def test_minimum_coverage_expectations(self):
        """Test that JSON fonts meet minimum coverage expectations for usability."""
        available_fonts = get_available_fonts()

        # Only test original JSON fonts for minimum coverage
        json_fonts = [
            "default",
            "block",
            "blur",
            "compact",
            "fire",
            "quadrant",
            "small",
        ]

        for font_name in available_fonts:
            if font_name in json_fonts:
                result = validate_font_character_coverage(font_name)

                # Every JSON font should have at least basic alphanumeric + space (37 chars minimum)
                min_expected_coverage = 37 / len(MANDATORY_CHARACTERS) * 100
                self.assertGreaterEqual(
                    result["coverage_percentage"],
                    min_expected_coverage,
                    f"JSON font '{font_name}' has insufficient coverage: {result['coverage_percentage']:.1f}% "
                    f"(expected >= {min_expected_coverage:.1f}%)",
                )

    def test_dynamic_fonts_functionality(self):
        """Test that dynamic fonts work correctly."""
        available_fonts = get_available_fonts()

        # Test dynamic fonts
        dynamic_fonts = ["matrix"]

        for font_name in available_fonts:
            if font_name in dynamic_fonts:
                result = validate_font_character_coverage(font_name)

                # Dynamic fonts should have at least some characters
                self.assertGreater(
                    result["available"],
                    0,
                    f"Dynamic font '{font_name}' has no available characters",
                )
                self.assertGreater(
                    result["coverage_percentage"],
                    0,
                    f"Dynamic font '{font_name}' has 0% coverage",
                )

                # Dynamic fonts should support space character
                self.assertNotIn(
                    " ",
                    result["missing_characters"],
                    f"Dynamic font '{font_name}' is missing space character",
                )


if __name__ == "__main__":
    unittest.main()

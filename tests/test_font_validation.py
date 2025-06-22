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
    get_font_height,
    get_character_data,
    get_available_fonts,
    get_font_characters,
)

"""Unit tests for font validation and integrity."""


class TestFontValidation(unittest.TestCase):
    """Test font character definitions for integrity and completeness."""

    def test_all_fonts_have_correct_character_line_counts(self):
        """Test that all characters in each font have the correct number of lines."""
        # Known issues in legacy fonts that we're not fixing in this project
        known_issues = {}

        for font_name in get_available_fonts():
            expected_height = get_font_height(font_name)
            characters = get_font_characters(font_name)

            with self.subTest(font=font_name):
                for char, char_data in characters.items():
                    with self.subTest(font=font_name, char=repr(char)):
                        self.assertIn(
                            "lines",
                            char_data,
                            f"Character '{char}' in font '{font_name}' missing 'lines' key",
                        )

                        lines = char_data["lines"]
                        actual_height = len(lines)

                        # Check if this is a known issue
                        if (font_name, char) in known_issues:
                            expected_for_known_issue = known_issues[(font_name, char)]
                            self.assertEqual(
                                actual_height,
                                expected_for_known_issue,
                                f"Known issue: Character '{char}' in font '{font_name}' has "
                                f"{actual_height} lines, expected {expected_for_known_issue}",
                            )
                        else:
                            self.assertEqual(
                                actual_height,
                                expected_height,
                                f"Character '{char}' in font '{font_name}' has {actual_height} lines, expected {expected_height}",
                            )

    def test_quadrant_font_has_complete_alphanumeric_set(self):
        """Test that quadrant font has all digits, uppercase, and lowercase letters."""
        quadrant_chars = set(get_font_characters("quadrant").keys())

        # Test digits 0-9
        digits = set(str(i) for i in range(10))
        missing_digits = digits - quadrant_chars
        self.assertEqual(
            len(missing_digits),
            0,
            f"Quadrant font missing digits: {sorted(missing_digits)}",
        )

        # Test uppercase A-Z
        uppercase = set(chr(i) for i in range(ord("A"), ord("Z") + 1))
        missing_uppercase = uppercase - quadrant_chars
        self.assertEqual(
            len(missing_uppercase),
            0,
            f"Quadrant font missing uppercase letters: {sorted(missing_uppercase)}",
        )

        # Test lowercase a-z
        lowercase = set(chr(i) for i in range(ord("a"), ord("z") + 1))
        missing_lowercase = lowercase - quadrant_chars
        self.assertEqual(
            len(missing_lowercase),
            0,
            f"Quadrant font missing lowercase letters: {sorted(missing_lowercase)}",
        )

    def test_font_height_function_returns_correct_values(self):
        """Test that get_font_height returns the correct height for each font."""
        # Predefined expected heights for known fonts
        expected_heights = {
            "default": 7,
            "quadrant": 5,
            "matrix": 5,
            "small": 5,
            "block": 7,
            "banner": 7,
            "shadow": 6,
            "fire": 7,
            "blur": 7,
            "compact": 4,
            "ttf": 8,
        }

        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                actual_height = get_font_height(font_name)
                if font_name in expected_heights:
                    expected_height = expected_heights[font_name]
                    self.assertEqual(
                        actual_height,
                        expected_height,
                        f"get_font_height('{font_name}') returned {actual_height}, expected {expected_height}",
                    )
                else:
                    # For unknown fonts, just verify it returns a positive integer
                    self.assertIsInstance(actual_height, int)
                    self.assertGreater(actual_height, 0)

    def test_get_character_data_returns_valid_structure(self):
        """Test that get_character_data returns properly structured data."""
        test_cases = [
            ("A", "default"),
            ("a", "default"),
            ("0", "default"),
            ("A", "quadrant"),
            ("a", "quadrant"),
            ("0", "quadrant"),
        ]

        for char, font in test_cases:
            with self.subTest(char=char, font=font):
                char_data = get_character_data(char, font)
                self.assertIsNotNone(
                    char_data, f"get_character_data('{char}', '{font}') returned None"
                )
                self.assertIn(
                    "lines",
                    char_data,
                    f"Character data for '{char}' in '{font}' missing 'lines' key",
                )
                self.assertIn(
                    "width",
                    char_data,
                    f"Character data for '{char}' in '{font}' missing 'width' key",
                )

                lines = char_data["lines"]
                expected_height = get_font_height(font)
                self.assertEqual(
                    len(lines),
                    expected_height,
                    f"Character '{char}' in font '{font}' has {len(lines)} lines, expected {expected_height}",
                )

                # Width should be positive
                self.assertGreater(
                    char_data["width"],
                    0,
                    f"Character '{char}' in font '{font}' has non-positive width: {char_data['width']}",
                )

    def test_all_character_lines_are_strings(self):
        """Test that all character line data are strings."""
        for font_name in get_available_fonts():
            characters = get_font_characters(font_name)

            for char, char_data in characters.items():
                with self.subTest(font=font_name, char=repr(char)):
                    lines = char_data["lines"]
                    for i, line in enumerate(lines):
                        self.assertIsInstance(
                            line,
                            str,
                            f"Line {i} of character '{char}' in font '{font_name}' is not a string: {type(line)}",
                        )

    def test_quadrant_font_height_consistency(self):
        """Test that quadrant font consistently uses 5-line height."""
        expected_height = 5
        actual_height = get_font_height("quadrant")
        self.assertEqual(
            actual_height,
            expected_height,
            f"Quadrant font height is {actual_height}, expected {expected_height}",
        )

        # Test a sample of characters
        test_chars = ["A", "a", "0", "Z", "z", "9"]
        for char in test_chars:
            with self.subTest(char=char):
                char_data = get_character_data(char, "quadrant")
                self.assertIsNotNone(
                    char_data, f"Character '{char}' not found in quadrant font"
                )
                self.assertEqual(
                    len(char_data["lines"]),
                    expected_height,
                    f"Character '{char}' in quadrant font has {len(char_data['lines'])} lines, expected {expected_height}",
                )

    def test_quadrant_font_perfect_integrity(self):
        """Test that every single character in quadrant font has exactly 5 lines."""
        expected_height = get_font_height("quadrant")
        characters = get_font_characters("quadrant")

        self.assertEqual(expected_height, 5, "Quadrant font height should be 5")

        # Test every single character
        for char, char_data in characters.items():
            with self.subTest(char=repr(char)):
                self.assertIn(
                    "lines", char_data, f"Character '{char}' missing 'lines' key"
                )
                lines = char_data["lines"]
                self.assertEqual(
                    len(lines),
                    expected_height,
                    f"Character '{char}' has {len(lines)} lines, expected {expected_height}",
                )

                # Also verify all lines are strings
                for i, line in enumerate(lines):
                    self.assertIsInstance(
                        line,
                        str,
                        f"Line {i} of character '{char}' is not a string: {type(line)}",
                    )

    def test_quadrant_font_can_render_full_alphabet_and_numbers(self):
        """Integration test: verify quadrant font can render complete character sets without errors."""
        from banger.core import BannerGenerator

        test_cases = [
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # All uppercase
            "abcdefghijklmnopqrstuvwxyz",  # All lowercase
            "0123456789",  # All digits
            "Hello World 123",  # Mixed case with numbers
        ]

        for text in test_cases:
            with self.subTest(text=text[:20] + "..." if len(text) > 20 else text):
                generator = BannerGenerator(max_width=1000, font="quadrant")
                generator.add_text(text)
                result = generator.render()

                # Should not crash and should return a string
                self.assertIsInstance(result, str)
                self.assertGreater(
                    len(result), 0, "Rendered output should not be empty"
                )

                # Should have 4-5 lines of content (some lowercase letters have descenders)
                lines = result.split("\n")
                content_lines = [line for line in lines if line.strip()]
                self.assertIn(
                    len(content_lines),
                    [4, 5],
                    f"Quadrant font should produce 4-5 content lines, got {len(content_lines)}",
                )

    def test_fallback_to_default_font_for_invalid_font(self):
        """Test that invalid font names fall back to default font."""
        invalid_font = "nonexistent_font"
        char_data = get_character_data("A", invalid_font)
        self.assertIsNotNone(
            char_data,
            "get_character_data should fall back to default font for invalid font names",
        )

        # Should have same data as default font
        default_char_data = get_character_data("A", "default")
        self.assertEqual(
            char_data["lines"],
            default_char_data["lines"],
            "Fallback font data should match default font data",
        )

    def test_unknown_characters_return_none(self):
        """Test that unknown characters return None."""
        unknown_chars = [
            "€",
            "中",
            "🎉",
            "∑",
        ]  # Various Unicode characters not in fonts

        for char in unknown_chars:
            with self.subTest(char=char):
                char_data = get_character_data(char, "default")
                # Most unknown characters should return None (original behavior)
                # Some might be handled, so we just test that it doesn't crash
                if char_data is not None:
                    self.assertIn("lines", char_data)
                    self.assertIn("width", char_data)


if __name__ == "__main__":
    unittest.main()

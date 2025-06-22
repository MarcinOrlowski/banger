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

from banger.fonts import get_available_fonts
from banger.fonts.factory import create_font

"""Unit tests for uppercase letter completeness validation.

Tests that fonts claiming to support uppercase letters actually implement
all A-Z characters with proper data structures (non-empty lines list).
Characters can have empty content (0 lit pixels) but must exist with valid structure.
"""


class TestUppercaseCompleteness(unittest.TestCase):
    """Test that fonts properly implement all uppercase letters A-Z."""

    def _validate_font_uppercase_completeness(self, font_name):
        """Helper method to validate that a font has complete A-Z uppercase implementation."""
        font = create_font(font_name)
        available_chars = set(font.get_available_characters())

        # Define all uppercase letters A-Z
        uppercase_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        # Check that all A-Z characters exist
        missing_letters = uppercase_letters - available_chars
        self.assertEqual(
            len(missing_letters),
            0,
            f"Font '{font_name}' missing uppercase letters: {sorted(missing_letters)}",
        )

        # Validate each A-Z character has proper structure
        for letter in uppercase_letters:
            with self.subTest(font=font_name, letter=letter):
                char_data = font.get_character(letter)

                # Character data must exist (not None)
                self.assertIsNotNone(
                    char_data,
                    f"Font '{font_name}' character '{letter}' returned None data",
                )

                # Must have lines attribute
                self.assertTrue(
                    hasattr(char_data, "lines"),
                    f"Font '{font_name}' character '{letter}' missing 'lines' attribute",
                )

                lines = char_data.lines

                # Lines must be a list
                self.assertIsInstance(
                    lines,
                    list,
                    f"Font '{font_name}' character '{letter}' lines is not a list: {type(lines)}",
                )

                # Lines list must not be empty (but individual lines can be empty strings)
                self.assertGreater(
                    len(lines),
                    0,
                    f"Font '{font_name}' character '{letter}' has empty lines list",
                )

                # Each line must be a string (can be empty string - 0 lit pixels allowed)
                for line_idx, line in enumerate(lines):
                    self.assertIsInstance(
                        line,
                        str,
                        f"Font '{font_name}' character '{letter}' line {line_idx} "
                        f"is not a string: {type(line)} = {repr(line)}",
                    )

    def test_all_app_fonts_implement_complete_uppercase_A_to_Z(self):
        """Test that ALL fonts in the app implement complete A-Z uppercase letters.

        This runs the uppercase completeness validation against every font
        available in the application to ensure system-wide consistency.
        """
        available_fonts = get_available_fonts()
        self.assertGreater(len(available_fonts), 0, "No fonts available for testing")

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                # Run the validation for this font
                self._validate_font_uppercase_completeness(font_name)

    def test_uppercase_characters_have_consistent_height(self):
        """Test that all A-Z characters in each font have consistent height.

        All uppercase letters in a font should have the same number of lines
        as the font's declared height.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                declared_height = font.height
                uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                for letter in uppercase_letters:
                    with self.subTest(font=font_name, letter=letter):
                        char_data = font.get_character(letter)

                        if (
                            char_data
                        ):  # Skip if character doesn't exist (some fonts may not have all)
                            lines = char_data.lines
                            actual_height = len(lines)

                            self.assertEqual(
                                actual_height,
                                declared_height,
                                f"Font '{font_name}' character '{letter}' has {actual_height} lines, "
                                f"expected {declared_height}",
                            )

    def test_uppercase_characters_have_positive_width(self):
        """Test that all A-Z characters have positive width values.

        Width must be positive for proper character spacing.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

                for letter in uppercase_letters:
                    with self.subTest(font=font_name, letter=letter):
                        char_data = font.get_character(letter)

                        if char_data:  # Skip if character doesn't exist
                            self.assertTrue(
                                hasattr(char_data, "width"),
                                f"Font '{font_name}' character '{letter}' missing 'width' attribute",
                            )

                            width = char_data.width
                            self.assertIsInstance(
                                width,
                                int,
                                f"Font '{font_name}' character '{letter}' width is not an integer: {type(width)}",
                            )

                            self.assertGreater(
                                width,
                                0,
                                f"Font '{font_name}' character '{letter}' has non-positive width: {width}",
                            )

    def test_specific_font_uppercase_completeness_quadrant(self):
        """Test that quadrant font specifically has complete A-Z implementation.

        Quadrant is the default font, so it must have complete uppercase support.
        """
        self._validate_font_uppercase_completeness("quadrant")

    def test_specific_font_uppercase_completeness_default(self):
        """Test that default font specifically has complete A-Z implementation.

        Default font must have complete uppercase support.
        """
        self._validate_font_uppercase_completeness("default")


if __name__ == "__main__":
    unittest.main()

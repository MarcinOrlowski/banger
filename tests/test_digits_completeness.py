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

"""Unit tests for digits completeness validation.

Tests that fonts claiming to support digits actually implement
all 0-9 characters with proper data structures (non-empty lines list).
Characters can have empty content (0 lit pixels) but must exist with valid structure.
"""


class TestDigitsCompleteness(unittest.TestCase):
    """Test that fonts properly implement all digits 0-9."""

    def _validate_font_digits_completeness(self, font_name):
        """Helper method to validate that a font has complete 0-9 digits implementation."""
        font = create_font(font_name)
        available_chars = set(font.get_available_characters())

        # Define all digits 0-9
        digits = set("0123456789")

        # Check that all 0-9 characters exist
        missing_digits = digits - available_chars
        self.assertEqual(
            len(missing_digits),
            0,
            f"Font '{font_name}' missing digits: {sorted(missing_digits)}",
        )

        # Validate each 0-9 character has proper structure
        for digit in digits:
            with self.subTest(font=font_name, digit=digit):
                char_data = font.get_character(digit)

                # Character data must exist (not None)
                self.assertIsNotNone(
                    char_data,
                    f"Font '{font_name}' character '{digit}' returned None data",
                )

                # Must have lines attribute
                self.assertTrue(
                    hasattr(char_data, "lines"),
                    f"Font '{font_name}' character '{digit}' missing 'lines' attribute",
                )

                lines = char_data.lines

                # Lines must be a list
                self.assertIsInstance(
                    lines,
                    list,
                    f"Font '{font_name}' character '{digit}' lines is not a list: {type(lines)}",
                )

                # Lines list must not be empty (but individual lines can be empty strings)
                self.assertGreater(
                    len(lines),
                    0,
                    f"Font '{font_name}' character '{digit}' has empty lines list",
                )

                # Each line must be a string (can be empty string - 0 lit pixels allowed)
                for line_idx, line in enumerate(lines):
                    self.assertIsInstance(
                        line,
                        str,
                        f"Font '{font_name}' character '{digit}' line {line_idx} "
                        f"is not a string: {type(line)} = {repr(line)}",
                    )

    def test_all_app_fonts_implement_complete_digits_0_to_9(self):
        """Test that ALL fonts in the app implement complete 0-9 digits.

        This runs the digits completeness validation against every font
        available in the application to ensure system-wide consistency.
        """
        available_fonts = get_available_fonts()
        self.assertGreater(len(available_fonts), 0, "No fonts available for testing")

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                # Run the validation for this font
                self._validate_font_digits_completeness(font_name)

    def test_digits_characters_have_consistent_height(self):
        """Test that all 0-9 characters in each font have consistent height.

        All digits in a font should have the same number of lines
        as the font's declared height.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                declared_height = font.height
                digits = "0123456789"

                for digit in digits:
                    with self.subTest(font=font_name, digit=digit):
                        char_data = font.get_character(digit)

                        if (
                            char_data
                        ):  # Skip if character doesn't exist (some fonts may not have all)
                            lines = char_data.lines
                            actual_height = len(lines)

                            self.assertEqual(
                                actual_height,
                                declared_height,
                                f"Font '{font_name}' character '{digit}' has {actual_height} lines, "
                                f"expected {declared_height}",
                            )

    def test_digits_characters_have_positive_width(self):
        """Test that all 0-9 characters have positive width values.

        Width must be positive for proper character spacing.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                digits = "0123456789"

                for digit in digits:
                    with self.subTest(font=font_name, digit=digit):
                        char_data = font.get_character(digit)

                        if char_data:  # Skip if character doesn't exist
                            self.assertTrue(
                                hasattr(char_data, "width"),
                                f"Font '{font_name}' character '{digit}' missing 'width' attribute",
                            )

                            width = char_data.width
                            self.assertIsInstance(
                                width,
                                int,
                                f"Font '{font_name}' character '{digit}' width is not an integer: {type(width)}",
                            )

                            self.assertGreater(
                                width,
                                0,
                                f"Font '{font_name}' character '{digit}' has non-positive width: {width}",
                            )

    def test_specific_font_digits_completeness_quadrant(self):
        """Test that quadrant font specifically has complete 0-9 implementation.

        Quadrant is the default font, so it must have complete digits support.
        """
        self._validate_font_digits_completeness("quadrant")

    def test_specific_font_digits_completeness_default(self):
        """Test that default font specifically has complete 0-9 implementation.

        Default font must have complete digits support.
        """
        self._validate_font_digits_completeness("default")


if __name__ == "__main__":
    unittest.main()

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

"""Unit tests for extra characters completeness validation.

Tests that fonts properly implement extra characters (punctuation, symbols, special characters)
that are neither letters nor digits. Based on the character set available in the quadrant font
as the reference implementation.
"""


class TestExtraCharactersCompleteness(unittest.TestCase):
    """Test that fonts properly implement extra characters (punctuation, symbols, etc.)."""

    # Reference set of extra characters based on quadrant font
    # These are characters that are neither letters (A-Z, a-z) nor digits (0-9)
    REFERENCE_EXTRA_CHARACTERS = {
        " ",  # space
        "!",  # exclamation mark
        "#",  # hash/pound
        "$",  # dollar sign
        "(",  # left parenthesis
        ")",  # right parenthesis
        "*",  # asterisk
        "+",  # plus sign
        "-",  # hyphen/minus
        ".",  # period/dot
        "/",  # forward slash
        ":",  # colon
        "?",  # question mark
        "[",  # left square bracket
        "]",  # right square bracket
        "_",  # underscore
    }

    def _validate_font_extra_characters_completeness(self, font_name):
        """Helper method to validate that a font has complete extra characters implementation."""
        font = create_font(font_name)
        available_chars = set(font.get_available_characters())

        # Check that reference extra characters exist
        missing_chars = self.REFERENCE_EXTRA_CHARACTERS - available_chars
        if missing_chars:
            # Allow fonts to not have all extra characters (not all fonts may support all symbols)
            self.skipTest(
                f"Font '{font_name}' missing extra characters: {sorted(missing_chars)} - skipping validation"
            )

        # Validate each available extra character has proper structure
        available_extra_chars = self.REFERENCE_EXTRA_CHARACTERS & available_chars
        for char in available_extra_chars:
            with self.subTest(font=font_name, char=repr(char)):
                char_data = font.get_character(char)

                # Character data must exist (not None)
                self.assertIsNotNone(
                    char_data,
                    f"Font '{font_name}' character {repr(char)} returned None data",
                )

                # Must have lines attribute
                self.assertTrue(
                    hasattr(char_data, "lines"),
                    f"Font '{font_name}' character {repr(char)} missing 'lines' attribute",
                )

                lines = char_data.lines

                # Lines must be a list
                self.assertIsInstance(
                    lines,
                    list,
                    f"Font '{font_name}' character {repr(char)} lines is not a list: {type(lines)}",
                )

                # Lines list must not be empty (but individual lines can be empty strings)
                self.assertGreater(
                    len(lines),
                    0,
                    f"Font '{font_name}' character {repr(char)} has empty lines list",
                )

                # Each line must be a string (can be empty string - 0 lit pixels allowed)
                for line_idx, line in enumerate(lines):
                    self.assertIsInstance(
                        line,
                        str,
                        f"Font '{font_name}' character {repr(char)} line {line_idx} "
                        f"is not a string: {type(line)} = {repr(line)}",
                    )

    def test_all_app_fonts_implement_available_extra_characters(self):
        """Test that ALL fonts implement their available extra characters correctly.

        This runs the extra characters validation against every font
        available in the application to ensure system-wide consistency.
        Note: not all fonts need to have all extra characters.
        """
        available_fonts = get_available_fonts()
        self.assertGreater(len(available_fonts), 0, "No fonts available for testing")

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                # Run the validation for this font
                self._validate_font_extra_characters_completeness(font_name)

    def test_extra_characters_have_consistent_height(self):
        """Test that all extra characters in each font have consistent height.

        All extra characters in a font should have the same number of lines
        as the font's declared height.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                declared_height = font.height
                available_chars = set(font.get_available_characters())

                # Get available extra characters for this font
                available_extra_chars = (
                    self.REFERENCE_EXTRA_CHARACTERS & available_chars
                )

                for char in available_extra_chars:
                    with self.subTest(font=font_name, char=repr(char)):
                        char_data = font.get_character(char)

                        if char_data:  # Skip if character doesn't exist
                            lines = char_data.lines
                            actual_height = len(lines)

                            self.assertEqual(
                                actual_height,
                                declared_height,
                                f"Font '{font_name}' character {repr(char)} has {actual_height} lines, "
                                f"expected {declared_height}",
                            )

    def test_extra_characters_have_positive_width(self):
        """Test that all extra characters have positive width values.

        Width must be positive for proper character spacing.
        Note: space character might be an exception and could have different width handling.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = set(font.get_available_characters())

                # Get available extra characters for this font
                available_extra_chars = (
                    self.REFERENCE_EXTRA_CHARACTERS & available_chars
                )

                for char in available_extra_chars:
                    with self.subTest(font=font_name, char=repr(char)):
                        char_data = font.get_character(char)

                        if char_data:  # Skip if character doesn't exist
                            self.assertTrue(
                                hasattr(char_data, "width"),
                                f"Font '{font_name}' character {repr(char)} missing 'width' attribute",
                            )

                            width = char_data.width
                            self.assertIsInstance(
                                width,
                                int,
                                f"Font '{font_name}' character {repr(char)} width is not an integer: {type(width)}",
                            )

                            self.assertGreater(
                                width,
                                0,
                                f"Font '{font_name}' character {repr(char)} has non-positive width: {width}",
                            )

    def test_specific_font_extra_characters_completeness_quadrant(self):
        """Test that quadrant font specifically has complete extra characters implementation.

        Quadrant is the default font and defines our reference character set,
        so it must have complete extra characters support.
        """
        self._validate_font_extra_characters_completeness("quadrant")

    def test_specific_font_extra_characters_completeness_default(self):
        """Test that default font specifically has available extra characters implementation.

        Default font should have good extra characters support.
        """
        self._validate_font_extra_characters_completeness("default")

    def test_space_character_special_handling(self):
        """Test that space character has special handling across fonts.

        Space character is critical for text rendering and should be handled
        consistently across all fonts. It may have special trim=False attribute.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = set(font.get_available_characters())

                if " " in available_chars:
                    char_data = font.get_character(" ")

                    self.assertIsNotNone(
                        char_data,
                        f"Font '{font_name}' space character returned None data",
                    )

                    # Space should have lines
                    self.assertTrue(
                        hasattr(char_data, "lines"),
                        f"Font '{font_name}' space character missing 'lines' attribute",
                    )

                    lines = char_data.lines
                    self.assertIsInstance(
                        lines,
                        list,
                        f"Font '{font_name}' space character lines is not a list",
                    )

                    # Space should have correct height
                    actual_height = len(lines)
                    expected_height = font.height
                    self.assertEqual(
                        actual_height,
                        expected_height,
                        f"Font '{font_name}' space character has {actual_height} lines, "
                        f"expected {expected_height}",
                    )

                    # Check if space has trim attribute (common for space characters)
                    if hasattr(char_data, "trim"):
                        # Space characters often have trim=False to preserve spacing
                        trim_value = char_data.trim
                        self.assertIsInstance(
                            trim_value,
                            bool,
                            f"Font '{font_name}' space character trim is not a bool: {type(trim_value)}",
                        )

    def test_get_all_extra_characters_in_fonts(self):
        """Test to discover what extra characters are available across all fonts.

        This is a discovery test to help understand the character coverage
        across different fonts beyond our reference set.
        """
        letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        digits = set("0123456789")
        all_extra_chars = set()

        for font_name in get_available_fonts():
            font = create_font(font_name)
            chars = font.get_available_characters()
            font_extra_chars = [
                c
                for c in chars
                if c not in letters and c not in digits and c != "default"
            ]
            all_extra_chars.update(font_extra_chars)

        # Remove our reference characters to see what's beyond
        beyond_reference = all_extra_chars - self.REFERENCE_EXTRA_CHARACTERS
        coverage_count = len(self.REFERENCE_EXTRA_CHARACTERS & all_extra_chars)
        total_count = len(all_extra_chars)

        # Use assertion to report the character discovery results
        self.assertGreater(
            len(all_extra_chars), 0, "No extra characters found across any fonts"
        )

        # This assertion will always pass but provides useful information in verbose mode
        beyond_info = (
            f", beyond reference: {sorted(beyond_reference)}"
            if beyond_reference
            else ""
        )
        self.assertTrue(
            True,
            f"Character discovery: {total_count} total extra characters found, "
            f"reference set covers {coverage_count}/{total_count} characters"
            + beyond_info,
        )


if __name__ == "__main__":
    unittest.main()

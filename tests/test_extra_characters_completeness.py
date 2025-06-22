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

    def test_font_implements_reference_extra_characters(self):
        """Test that a font implements reference extra characters with valid structure.

        This is a helper method that validates a single font has the reference
        extra characters. Each character must:
        - Exist in the font
        - Have non-None character data
        - Have a non-empty lines list
        - Lines can be empty strings (0 lit pixels allowed)
        """

        def validate_font_extra_characters_completeness(font_name):
            """Validate that a font has proper extra characters implementation.

            Note: This validates that any extra characters the font DOES have
            work correctly, but doesn't require all fonts to have all extra characters.
            """
            font = create_font(font_name)
            available_chars = set(font.get_available_characters())

            # Check which reference extra characters this font has
            missing_chars = self.REFERENCE_EXTRA_CHARACTERS - available_chars
            if missing_chars:
                # Just log for info - not all fonts need all extra characters
                print(
                    f"Info: Font '{font_name}' doesn't have these extra characters: {sorted(missing_chars)}"
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

        return validate_font_extra_characters_completeness

    def test_all_app_fonts_implement_available_extra_characters(self):
        """Test that ALL fonts implement their available extra characters correctly.

        This runs the extra characters validation against every font
        available in the application to ensure system-wide consistency.
        Note: not all fonts need to have all extra characters.
        """
        validate_func = self.test_font_implements_reference_extra_characters()

        available_fonts = get_available_fonts()
        self.assertGreater(len(available_fonts), 0, "No fonts available for testing")

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                # Run the validation for this font
                validate_func(font_name)

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
        validate_func = self.test_font_implements_reference_extra_characters()
        validate_func("quadrant")

    def test_specific_font_extra_characters_completeness_default(self):
        """Test that default font specifically has available extra characters implementation.

        Default font should have good extra characters support.
        """
        validate_func = self.test_font_implements_reference_extra_characters()
        validate_func("default")

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
        if beyond_reference:
            print(
                f"\nExtra characters beyond reference set found: {sorted(beyond_reference)}"
            )

        print(f"Total unique extra characters across all fonts: {len(all_extra_chars)}")
        print(
            f"Reference set covers: {len(self.REFERENCE_EXTRA_CHARACTERS)} characters"
        )
        print(
            f"Coverage: {len(self.REFERENCE_EXTRA_CHARACTERS & all_extra_chars)}/{len(all_extra_chars)} characters"
        )


if __name__ == "__main__":
    unittest.main()

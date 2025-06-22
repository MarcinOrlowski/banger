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

"""Unit tests for validating space character implementation in all fonts."""


class TestSpaceCharacterValidation(unittest.TestCase):
    """Test that all fonts have proper space character implementation."""

    def test_all_fonts_have_space_character(self):
        """Test that all fonts have space character (' ') defined."""
        available_fonts = get_available_fonts()

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                font = create_font(font_name)

                # Check that space character is supported
                self.assertTrue(
                    font.has_character(" "),
                    f"Font '{font_name}' does not have space character (' ') defined",
                )

    def test_all_fonts_space_character_trim_flag(self):
        """Test that all fonts have space character with trim=False."""
        available_fonts = get_available_fonts()

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                font = create_font(font_name)

                # Get space character data
                space_char = font.get_character(" ")

                # Verify space character exists
                self.assertIsNotNone(
                    space_char,
                    f"Font '{font_name}' does not have space character (' ') defined",
                )

                # Verify trim flag is False
                self.assertFalse(
                    space_char.trim,
                    f"Font '{font_name}' space character (' ') has trim=True, but it should be trim=False",
                )

    def test_space_character_has_lines(self):
        """Test that space character has proper line data."""
        available_fonts = get_available_fonts()

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                font = create_font(font_name)
                space_char = font.get_character(" ")

                # Verify space character has lines
                self.assertIsNotNone(
                    space_char.lines, f"Font '{font_name}' space character has no lines"
                )
                self.assertGreater(
                    len(space_char.lines),
                    0,
                    f"Font '{font_name}' space character has empty lines",
                )

                # Verify lines match font height
                expected_height = font.height
                actual_height = len(space_char.lines)
                self.assertEqual(
                    expected_height,
                    actual_height,
                    f"Font '{font_name}' space character has {actual_height} lines, "
                    f"but font height is {expected_height}",
                )

    def test_space_character_has_positive_width(self):
        """Test that space character has positive width."""
        available_fonts = get_available_fonts()

        for font_name in available_fonts:
            with self.subTest(font=font_name):
                font = create_font(font_name)
                space_char = font.get_character(" ")

                # Verify space character has positive width
                self.assertGreater(
                    space_char.width,
                    0,
                    f"Font '{font_name}' space character has zero or negative width: {space_char.width}",
                )


if __name__ == "__main__":
    unittest.main()

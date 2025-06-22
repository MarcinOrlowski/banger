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

"""Unit tests for default character validation.

Tests that all fonts have a properly defined, visible default character.
The default character is critical as it's used as a fallback when requested characters are missing.
"""


class TestDefaultCharacter(unittest.TestCase):
    """Test that all fonts have a properly defined default character."""

    def test_all_fonts_have_default_character(self):
        """Test that all fonts have a 'default' character defined.

        The 'default' character is used as a fallback when a requested character
        is not available in the font. It must exist in all fonts.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = set(font.get_available_characters())

                self.assertIn(
                    "default",
                    available_chars,
                    f"Font '{font_name}' missing required 'default' character",
                )

    def test_default_character_has_valid_data(self):
        """Test that default character has proper character data structure.

        The default character must have a CharacterData object with proper structure.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                default_char_data = font.get_character("default")

                self.assertIsNotNone(
                    default_char_data,
                    f"Font '{font_name}' has None for default character data",
                )

                # Check that it has lines attribute
                self.assertTrue(
                    hasattr(default_char_data, "lines"),
                    f"Font '{font_name}' default character missing 'lines' attribute",
                )

                # Check that it has width attribute
                self.assertTrue(
                    hasattr(default_char_data, "width"),
                    f"Font '{font_name}' default character missing 'width' attribute",
                )

    def test_default_character_has_visible_content(self):
        """Test that default character has at least one visible (non-empty after trimming) line.

        The default character must be visible to the user - it cannot be all spaces or empty.
        This ensures that when we fall back to the default character, something is actually displayed.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                default_char_data = font.get_character("default")

                self.assertIsNotNone(
                    default_char_data,
                    f"Font '{font_name}' has None for default character data",
                )

                lines = default_char_data.lines

                # Check that at least one line has visible content after trimming
                has_visible_content = any(line.strip() for line in lines)

                self.assertTrue(
                    has_visible_content,
                    f"Font '{font_name}' default character has no visible content - "
                    f"all lines are empty or whitespace-only: {lines}",
                )

    def test_default_character_width_is_positive(self):
        """Test that default character has positive width.

        The default character width must be positive to ensure proper spacing.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                default_char_data = font.get_character("default")

                self.assertIsNotNone(
                    default_char_data,
                    f"Font '{font_name}' has None for default character data",
                )

                width = default_char_data.width
                self.assertIsInstance(
                    width,
                    int,
                    f"Font '{font_name}' default character width is not an integer: {type(width)}",
                )

                self.assertGreater(
                    width,
                    0,
                    f"Font '{font_name}' default character has non-positive width: {width}",
                )

    def test_default_character_lines_match_font_height(self):
        """Test that default character has correct number of lines for font height.

        The default character must have the same number of lines as the font's declared height.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                expected_height = font.height

                default_char_data = font.get_character("default")
                self.assertIsNotNone(
                    default_char_data,
                    f"Font '{font_name}' has None for default character data",
                )

                lines = default_char_data.lines
                actual_height = len(lines)

                self.assertEqual(
                    actual_height,
                    expected_height,
                    f"Font '{font_name}' default character has {actual_height} lines, expected {expected_height}",
                )


if __name__ == "__main__":
    unittest.main()

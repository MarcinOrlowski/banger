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

"""Unit tests for font height consistency validation.

Tests that every character in every font has exactly the same number of lines
as declared in the font's height metadata. This ensures consistent rendering
and prevents layout issues.
"""


class TestFontHeightConsistency(unittest.TestCase):
    """Test that all characters in each font have consistent line counts matching font height."""

    def test_all_characters_match_declared_font_height(self):
        """Test that every character has exactly the same number of lines as font height.

        This is critical for consistent rendering - all characters in a font must have
        the same number of lines to maintain proper alignment and baseline consistency.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                declared_height = font.height
                available_chars = font.get_available_characters()

                # Test every single character in the font
                for char in available_chars:
                    with self.subTest(font=font_name, char=repr(char)):
                        char_data = font.get_character(char)

                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' character '{char}' returned None data",
                        )

                        self.assertTrue(
                            hasattr(char_data, "lines"),
                            f"Font '{font_name}' character '{char}' missing 'lines' attribute",
                        )

                        lines = char_data.lines
                        self.assertIsInstance(
                            lines,
                            list,
                            f"Font '{font_name}' character '{char}' lines is not a list: {type(lines)}",
                        )

                        actual_height = len(lines)
                        self.assertEqual(
                            actual_height,
                            declared_height,
                            f"Font '{font_name}' character '{char}' has {actual_height} lines, "
                            f"but font declares height of {declared_height}",
                        )

    def test_font_metadata_height_is_positive(self):
        """Test that all fonts declare a positive height.

        Font height must be a positive integer for proper rendering.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                height = font.height

                self.assertIsInstance(
                    height,
                    int,
                    f"Font '{font_name}' height is not an integer: {type(height)}",
                )

                self.assertGreater(
                    height, 0, f"Font '{font_name}' has non-positive height: {height}"
                )

    def test_all_lines_in_characters_are_strings(self):
        """Test that all lines in all characters are strings.

        Each line must be a string for proper text rendering.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = font.get_available_characters()

                for char in available_chars:
                    with self.subTest(font=font_name, char=repr(char)):
                        char_data = font.get_character(char)

                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' character '{char}' returned None data",
                        )

                        lines = char_data.lines

                        for line_idx, line in enumerate(lines):
                            self.assertIsInstance(
                                line,
                                str,
                                f"Font '{font_name}' character '{char}' line {line_idx} "
                                f"is not a string: {type(line)} = {repr(line)}",
                            )

    def test_font_height_matches_actual_character_line_counts(self):
        """Test that font height declaration matches reality across all characters.

        This is a comprehensive validation that the font's declared height
        is actually consistent with every character's line count.
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                declared_height = font.height
                available_chars = font.get_available_characters()

                # Collect actual heights from all characters
                actual_heights = set()
                problem_chars = []

                for char in available_chars:
                    char_data = font.get_character(char)
                    if char_data and hasattr(char_data, "lines"):
                        actual_height = len(char_data.lines)
                        actual_heights.add(actual_height)

                        if actual_height != declared_height:
                            problem_chars.append((char, actual_height))

                # All characters should have the same height as declared
                if len(actual_heights) > 1:
                    self.fail(
                        f"Font '{font_name}' has inconsistent character heights: "
                        f"declared={declared_height}, actual_heights={sorted(actual_heights)}, "
                        f"problem_chars={problem_chars}"
                    )

                # The single height should match declaration
                if actual_heights:
                    single_height = actual_heights.pop()
                    self.assertEqual(
                        single_height,
                        declared_height,
                        f"Font '{font_name}' declared height {declared_height} "
                        f"doesn't match actual character heights {single_height}",
                    )

    def test_no_characters_have_empty_lines_list(self):
        """Test that no character has an empty lines list.

        Every character must have at least one line (even if that line is empty string).
        """
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = font.get_available_characters()

                for char in available_chars:
                    with self.subTest(font=font_name, char=repr(char)):
                        char_data = font.get_character(char)

                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' character '{char}' returned None data",
                        )

                        lines = char_data.lines
                        self.assertGreater(
                            len(lines),
                            0,
                            f"Font '{font_name}' character '{char}' has empty lines list",
                        )


if __name__ == "__main__":
    unittest.main()

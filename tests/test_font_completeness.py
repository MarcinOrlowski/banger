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

"""Unit tests for font completeness validation.

Tests that fonts claiming to support character sets actually have complete implementations.
"""


class TestFontCompleteness(unittest.TestCase):
    """Test that fonts have complete character sets for their declared capabilities."""

    def test_fonts_claiming_uppercase_support_have_complete_uppercase_set(self):
        """Test that fonts claiming uppercase support have all A-Z characters."""
        uppercase_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)

                # Only test fonts that claim to support uppercase
                if font.metadata.supports_uppercase:
                    available_chars = set(font.get_available_characters())
                    missing_uppercase = uppercase_chars - available_chars

                    self.assertEqual(
                        len(missing_uppercase),
                        0,
                        f"Font '{font_name}' claims supports_uppercase=True but missing: {sorted(missing_uppercase)}",
                    )

                    # Also verify characters have non-empty line data
                    for char in uppercase_chars:
                        char_data = font.get_character(char)
                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' missing character data for '{char}'",
                        )
                        self.assertGreater(
                            len(char_data.lines),
                            0,
                            f"Font '{font_name}' has empty lines for character '{char}'",
                        )
                        self.assertTrue(
                            any(line.strip() for line in char_data.lines),
                            f"Font '{font_name}' has all-empty lines for character '{char}'",
                        )

    def test_fonts_claiming_lowercase_support_have_complete_lowercase_set(self):
        """Test that fonts claiming lowercase support have all a-z characters."""
        lowercase_chars = set("abcdefghijklmnopqrstuvwxyz")

        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)

                # Only test fonts that claim to support lowercase
                if font.metadata.supports_lowercase:
                    available_chars = set(font.get_available_characters())
                    missing_lowercase = lowercase_chars - available_chars

                    self.assertEqual(
                        len(missing_lowercase),
                        0,
                        f"Font '{font_name}' claims supports_lowercase=True but missing: {sorted(missing_lowercase)}",
                    )

                    # Also verify characters have non-empty line data
                    for char in lowercase_chars:
                        char_data = font.get_character(char)
                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' missing character data for '{char}'",
                        )
                        self.assertGreater(
                            len(char_data.lines),
                            0,
                            f"Font '{font_name}' has empty lines for character '{char}'",
                        )
                        self.assertTrue(
                            any(line.strip() for line in char_data.lines),
                            f"Font '{font_name}' has all-empty lines for character '{char}'",
                        )

    def test_fonts_claiming_digits_support_have_complete_digits_set(self):
        """Test that fonts claiming digits support have all 0-9 characters."""
        digit_chars = set("0123456789")

        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)

                # Only test fonts that claim to support digits
                if font.metadata.supports_digits:
                    available_chars = set(font.get_available_characters())
                    missing_digits = digit_chars - available_chars

                    self.assertEqual(
                        len(missing_digits),
                        0,
                        f"Font '{font_name}' claims supports_digits=True but missing: {sorted(missing_digits)}",
                    )

                    # Also verify characters have non-empty line data
                    for char in digit_chars:
                        char_data = font.get_character(char)
                        self.assertIsNotNone(
                            char_data,
                            f"Font '{font_name}' missing character data for '{char}'",
                        )
                        self.assertGreater(
                            len(char_data.lines),
                            0,
                            f"Font '{font_name}' has empty lines for character '{char}'",
                        )
                        self.assertTrue(
                            any(line.strip() for line in char_data.lines),
                            f"Font '{font_name}' has all-empty lines for character '{char}'",
                        )

    def test_fonts_have_consistent_metadata_with_actual_characters(self):
        """Test that font metadata consistency matches actual character availability."""
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = set(font.get_available_characters())

                # Check if metadata claims match reality
                uppercase_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                lowercase_chars = set("abcdefghijklmnopqrstuvwxyz")
                digit_chars = set("0123456789")

                has_any_uppercase = bool(uppercase_chars.intersection(available_chars))
                has_any_lowercase = bool(lowercase_chars.intersection(available_chars))
                has_any_digits = bool(digit_chars.intersection(available_chars))

                # If font has NO characters from a set, it shouldn't claim to support it
                # (This is a softer check - we allow partial support but flag complete absence)
                if not has_any_uppercase and font.metadata.supports_uppercase:
                    self.fail(
                        f"Font '{font_name}' claims supports_uppercase=True but has NO uppercase characters"
                    )

                if not has_any_lowercase and font.metadata.supports_lowercase:
                    self.fail(
                        f"Font '{font_name}' claims supports_lowercase=True but has NO lowercase characters"
                    )

                if not has_any_digits and font.metadata.supports_digits:
                    self.fail(
                        f"Font '{font_name}' claims supports_digits=True but has NO digit characters"
                    )

    def test_all_fonts_have_space_character(self):
        """Test that all fonts have a space character for word separation."""
        for font_name in get_available_fonts():
            with self.subTest(font=font_name):
                font = create_font(font_name)
                available_chars = set(font.get_available_characters())

                self.assertIn(
                    " ",
                    available_chars,
                    f"Font '{font_name}' missing space character ' '",
                )

                # Verify space character has proper data
                space_data = font.get_character(" ")
                self.assertIsNotNone(
                    space_data, f"Font '{font_name}' missing character data for space"
                )
                self.assertGreater(
                    len(space_data.lines),
                    0,
                    f"Font '{font_name}' has empty lines for space character",
                )


if __name__ == "__main__":
    unittest.main()

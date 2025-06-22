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

from banger.fonts.factory import create_font, get_available_fonts

"""Unit tests for font factory functionality."""


class TestFontFactory(unittest.TestCase):
    """Test font factory pattern implementation."""

    def test_create_font_with_valid_name(self):
        """Test that create_font creates valid font instances."""
        font = create_font("default")

        self.assertIsNotNone(font)
        self.assertEqual(font.name, "default")
        self.assertGreater(font.height, 0)

    def test_create_font_with_invalid_name_falls_back_to_default(self):
        """Test that create_font falls back to default for invalid names."""
        font = create_font("nonexistent_font")

        self.assertIsNotNone(font)
        self.assertEqual(font.name, "default")

    def test_create_font_creates_new_instances(self):
        """Test that create_font creates new instances each time (no caching)."""
        font1 = create_font("default")
        font2 = create_font("default")

        self.assertIsNotNone(font1)
        self.assertIsNotNone(font2)
        self.assertIsNot(font1, font2)  # Different objects

    def test_get_available_font_types_returns_list(self):
        """Test that get_available_font_types returns a non-empty list."""
        font_types = get_available_fonts()

        self.assertIsInstance(font_types, list)
        self.assertGreater(len(font_types), 0)
        self.assertIn("default", font_types)

    def test_get_available_font_types_contains_expected_fonts(self):
        """Test that get_available_font_types contains expected built-in fonts."""
        font_types = get_available_fonts()

        expected_fonts = [
            "default",
            "matrix",
            "banner",
            "block",
            "blur",
            "compact",
            "fire",
            "quadrant",
            "shadow",
            "small",
        ]

        for expected_font in expected_fonts:
            self.assertIn(expected_font, font_types)

    def test_factory_pattern_with_all_built_in_fonts(self):
        """Test that factory can create all built-in font types."""
        font_types = get_available_fonts()

        for font_type in font_types:
            with self.subTest(font_type=font_type):
                font = create_font(font_type)

                self.assertIsNotNone(font)
                self.assertEqual(font.name, font_type)
                self.assertGreater(font.height, 0)

    def test_font_instances_have_required_interface(self):
        """Test that created font instances implement required interface."""
        font = create_font("default")

        # Test required properties
        self.assertTrue(hasattr(font, "name"))
        self.assertTrue(hasattr(font, "height"))
        self.assertTrue(hasattr(font, "metadata"))

        # Test required methods
        self.assertTrue(hasattr(font, "get_character"))
        self.assertTrue(hasattr(font, "get_available_characters"))
        self.assertTrue(callable(font.get_character))
        self.assertTrue(callable(font.get_available_characters))


if __name__ == "__main__":
    unittest.main()

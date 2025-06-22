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

"""Core font system components."""

from .character_data import CharacterData
from .font_metadata import FontMetadata
from .interface import FontInterface
from .base import BaseFont
from .utils import calculate_character_width, normalize_character_lines

__all__ = [
    "CharacterData",
    "FontMetadata",
    "FontInterface",
    "BaseFont",
    "calculate_character_width",
    "normalize_character_lines"
]

"""
##################################################################################
#
# Bänger (Library) by Marcin Orlowski
# Because your `banner` deserves to be a `bänger`!
#
# @author    Marcin Orlowski <mail@marcinOrlowski.com>
# Copyright  ©2025-2026 Marcin Orlowski <MarcinOrlowski.com>
# @link      https://github.com/MarcinOrlowski/banger-lib
#
##################################################################################
"""

from .constants import DEFAULT_CHAR_SPACING, MANDATORY_CHARACTERS

from .core import (
    CharacterData,
    FontMetadata,
    FontInterface,
    BaseFont,
    calculate_character_width,
    normalize_character_lines,
)

from .factory import create_font, get_available_fonts, register_font

from .api import (
    get_font_height,
    get_font_characters,
    get_character_data,
    _get_character_data_object,
    validate_font_character_coverage,
    get_all_fonts_validation_report,
    get_max_character_width,
    _font_supports_lowercase,
    _font_supports_uppercase,
)

from .ttf import TtfFont

__all__ = [
    # Constants
    "DEFAULT_CHAR_SPACING",
    "MANDATORY_CHARACTERS",
    # Core
    "CharacterData",
    "FontMetadata",
    "FontInterface",
    "BaseFont",
    "calculate_character_width",
    "normalize_character_lines",
    # Factory
    "create_font",
    "get_available_fonts",
    "register_font",
    # API
    "get_font_height",
    "get_font_characters",
    "get_character_data",
    "_get_character_data_object",
    "validate_font_character_coverage",
    "get_all_fonts_validation_report",
    "get_max_character_width",
    "_font_supports_lowercase",
    "_font_supports_uppercase",
    # TTF
    "TtfFont",
]

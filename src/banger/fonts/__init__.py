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

# Import constants
from .constants import DEFAULT_CHAR_SPACING, MANDATORY_CHARACTERS

# Import core font system
from .core import (
    CharacterData,
    FontMetadata,
    FontInterface,
    BaseFont,
    calculate_character_width,
    normalize_character_lines,
)

# Import fonts
from .default import DefaultFont
from .matrix import MatrixFont

# Import factory functions
from .factory import create_font, get_available_fonts

# Import API functions
from .api import (
    get_font_height,
    get_font_characters,
    get_character_data,
    _get_character_data_object,
    validate_font_character_coverage,
    get_all_fonts_validation_report,
    get_max_character_width,
)

"""Unified fonts package - clean and simple.

This package contains all font-related functionality:
- Core font system (interfaces, base classes, utilities)
- Built-in font implementations
- Font registry and management
- Public API functions
- Style-specific definitions
"""


__all__ = [
    # Constants
    "DEFAULT_CHAR_SPACING",
    "MANDATORY_CHARACTERS",
    # Core font system
    "CharacterData",
    "FontMetadata",
    "FontInterface",
    "BaseFont",
    "calculate_character_width",
    "normalize_character_lines",
    # Built-in fonts
    "DefaultFont",
    "MatrixFont",
    # Factory
    "create_font",
    "get_available_fonts",
    # API functions
    "get_font_height",
    "get_font_characters",
    "get_character_data",
    "_get_character_data_object",
    "validate_font_character_coverage",
    "get_all_fonts_validation_report",
    "get_max_character_width",
]

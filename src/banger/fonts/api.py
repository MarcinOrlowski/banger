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

from typing import List, Dict, Any

from .factory import get_available_fonts as _get_available_font_types, create_font
from .constants import MANDATORY_CHARACTERS

"""Main API functions for font operations."""


def get_available_fonts() -> List[str]:
    """Get list of available font names.

    Returns:
        List of available font names
    """
    return _get_available_font_types()


def get_font_height(font_name: str) -> int:
    """Get font height in lines.

    Args:
        font_name: Name of the font

    Returns:
        Font height in lines
    """
    font = create_font(font_name)
    return font.height


def get_font_characters(font_name: str) -> Dict[str, Dict[str, Any]]:
    """Get all characters supported by a font.

    Args:
        font_name: Name of the font

    Returns:
        Dictionary of character names to character data structures
    """
    font = create_font(font_name)
    characters = {}
    for char in font.get_available_characters():
        char_data = font.get_character(char)
        if char_data:
            characters[char] = {
                "lines": char_data.lines,
                "width": char_data.width,
                "trim": getattr(char_data, "trim", True),
            }
    return characters


def get_character_data(char: str, font_name: str):
    """Get character data for rendering.

    Args:
        char: Character to get data for
        font_name: Name of the font

    Returns:
        Dictionary with character data if available, None otherwise
    """
    font = create_font(font_name)
    char_data = font.get_character(char)
    if char_data:
        return {
            "lines": getattr(char_data, "lines", []),
            "width": getattr(char_data, "width", 0),
            "trim": getattr(char_data, "trim", True),
        }
    return None


def _get_character_data_object(char: str, font_name: str):
    """Get character data as CharacterData object for internal use.

    Args:
        char: Character to get data for
        font_name: Name of the font

    Returns:
        CharacterData if available, None otherwise
    """
    font = create_font(font_name)
    return font.get_character(char)


def validate_font_character_coverage(font: str) -> Dict[str, Any]:
    """Validate that a font has all mandatory characters.

    Args:
        font: Font name to validate

    Returns:
        Dictionary with validation results including missing characters and coverage percentage
    """
    try:
        available_fonts = get_available_fonts()
        if font not in available_fonts:
            # Font doesn't exist
            return {
                "font": font,
                "total_mandatory": len(MANDATORY_CHARACTERS),
                "available": 0,
                "missing": len(MANDATORY_CHARACTERS),
                "missing_characters": list(MANDATORY_CHARACTERS),
                "coverage_percentage": 0.0,
                "is_complete": False,
            }

        # Get font characters
        font_obj = create_font(font)
        supported_chars = font_obj.get_available_characters()

        # Calculate coverage
        available_chars = MANDATORY_CHARACTERS.intersection(supported_chars)
        missing_chars = MANDATORY_CHARACTERS - supported_chars

        available_count = len(available_chars)
        missing_count = len(missing_chars)
        total_mandatory = len(MANDATORY_CHARACTERS)
        coverage_percentage = (available_count / total_mandatory) * 100.0

        return {
            "font": font,
            "total_mandatory": total_mandatory,
            "available": available_count,
            "missing": missing_count,
            "missing_characters": list(missing_chars),
            "coverage_percentage": coverage_percentage,
            "is_complete": missing_count == 0,
        }
    except Exception:
        # Error case - return zero coverage
        return {
            "font": font,
            "total_mandatory": len(MANDATORY_CHARACTERS),
            "available": 0,
            "missing": len(MANDATORY_CHARACTERS),
            "missing_characters": list(MANDATORY_CHARACTERS),
            "coverage_percentage": 0.0,
            "is_complete": False,
        }


def get_all_fonts_validation_report() -> Dict[str, Dict[str, Any]]:
    """Get validation report for all available fonts.

    Returns:
        Dictionary mapping font names to their validation results
    """
    report = {}
    for font_name in get_available_fonts():
        report[font_name] = validate_font_character_coverage(font_name)
    return report


def get_max_character_width(font_name: str, characters: str = None) -> int:
    """Get maximum character width for a font.

    Args:
        font_name: Name of the font
        characters: Characters to check (if None, checks all supported characters)

    Returns:
        Maximum character width
    """
    font = create_font(font_name)

    if characters is None:
        characters = font.get_available_characters()

    max_width = 0
    for char in characters:
        char_data = font.get_character(char)
        if char_data:
            max_width = max(max_width, char_data.width)

    return max_width


def _font_supports_lowercase(font_name: str) -> bool:
    """Check if font supports lowercase characters."""
    font = create_font(font_name)
    supported_chars = font.get_available_characters()
    # Check if font has any lowercase letters
    lowercase_letters = set("abcdefghijklmnopqrstuvwxyz")
    return bool(lowercase_letters.intersection(supported_chars))


def _font_supports_uppercase(font_name: str) -> bool:
    """Check if font supports uppercase characters."""
    font = create_font(font_name)
    supported_chars = font.get_available_characters()
    # Check if font has any uppercase letters
    uppercase_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return bool(uppercase_letters.intersection(supported_chars))

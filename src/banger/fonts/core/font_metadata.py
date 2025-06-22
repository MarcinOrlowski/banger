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

from dataclasses import dataclass
from typing import Optional

"""Font metadata structure for banner fonts."""


@dataclass
class FontMetadata:
    """Metadata about a banner font.

    This dataclass contains descriptive information about a font,
    including its capabilities and authorship information.

    Attributes:
        name: Unique font name/identifier
        height: Height of the font in lines
        description: Human-readable description of the font
        version: Font version (default "1.0")
        author: Optional author information
        supports_lowercase: Whether font supports lowercase letters
        supports_uppercase: Whether font supports uppercase letters
        supports_digits: Whether font supports digit characters
        supports_punctuation: Whether font supports punctuation marks
        bottom_padding: Number of extra blank lines to add at bottom (default 1)
    """

    name: str
    height: int
    description: str
    version: str = "1.0"
    author: Optional[str] = None
    supports_lowercase: bool = True
    supports_uppercase: bool = True
    supports_digits: bool = True
    supports_punctuation: bool = True
    bottom_padding: int = 1

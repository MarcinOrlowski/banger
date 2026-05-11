"""
##################################################################################
#
# Bänger by Marcin Orlowski
# Because your `banner` deserves to be a `bänger`!
#
# @author    Marcin Orlowski <mail@marcinOrlowski.com>
# Copyright  ©2025-2026 Marcin Orlowski <MarcinOrlowski.com>
# @link      https://github.com/MarcinOrlowski/banger
#
##################################################################################

Classic Unix banner command on steroids — CLI tool and Python library in one package.
"""

from .engine import Banger
from .exceptions import BangerError, CharacterNotSupportedError, FontNotFoundError
from . import fonts
from .fonts import (
    BaseFont,
    CharacterData,
    DEFAULT_CHAR_SPACING,
    FontInterface,
    FontMetadata,
    TtfFont,
    register_font,
)

__version__ = "1.2.0"

__all__ = [
    "Banger",
    "BangerError",
    "BaseFont",
    "CharacterData",
    "CharacterNotSupportedError",
    "DEFAULT_CHAR_SPACING",
    "FontInterface",
    "FontMetadata",
    "FontNotFoundError",
    "TtfFont",
    "fonts",
    "register_font",
]

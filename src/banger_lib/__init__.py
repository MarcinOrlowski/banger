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

banger_lib - ASCII banner generation library.

Usage:
    from banger_lib import Banger

    banger = Banger(font="fire")
    banger.add_text("Hello")
    output = banger.render()
"""

from .banger import Banger
from .exceptions import BangerError, FontNotFoundError, CharacterNotSupportedError
from . import fonts
from .fonts import (
    TtfFont,
    BaseFont,
    register_font,
    CharacterData,
    FontMetadata,
    FontInterface,
)

__version__ = "1.0.0"

__all__ = [
    # Main API
    "Banger",
    # Fonts module
    "fonts",
    "TtfFont",
    "BaseFont",
    "register_font",
    # Data structures
    "CharacterData",
    "FontMetadata",
    "FontInterface",
    # Exceptions
    "BangerError",
    "FontNotFoundError",
    "CharacterNotSupportedError",
]

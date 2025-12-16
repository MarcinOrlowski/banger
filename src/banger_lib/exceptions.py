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

Custom exceptions for banger_lib.
"""


class BangerError(Exception):
    """Base exception for banger_lib."""

    pass


class FontNotFoundError(BangerError):
    """Raised when requested font doesn't exist."""

    def __init__(self, font_name: str):
        self.font_name = font_name
        super().__init__(f"Font not found: {font_name}")


class CharacterNotSupportedError(BangerError):
    """Raised when character is not supported by font."""

    def __init__(self, char: str, font_name: str):
        self.char = char
        self.font_name = font_name
        super().__init__(f"Character '{char}' not supported by font '{font_name}'")

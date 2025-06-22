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

from typing import List, NamedTuple

"""Character data structure for banner fonts."""


class CharacterData(NamedTuple):
    """Data structure for a single character in a font.

    This immutable data structure contains all the information needed
    to render a single character in a banner font.

    Attributes:
        lines: List of strings representing each line of the character
        width: Width of the character in columns
        trim: Whether trailing spaces should be trimmed (default True)
    """

    lines: List[str]
    width: int
    trim: bool = True

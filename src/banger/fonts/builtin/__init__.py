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

from .banner import BannerFont
from .block import BlockFont
from .blur import BlurFont
from .classic import ClassicFont
from .compact import CompactFont
from .fire import FireFont
from .matrix import MatrixFont
from .quadrant import QuadrantFont
from .shadow import ShadowFont
from .small import SmallFont

# Built-in font implementations.
__all__ = [
    "BannerFont",
    "BlockFont",
    "BlurFont",
    "ClassicFont",
    "CompactFont",
    "FireFont",
    "MatrixFont",
    "QuadrantFont",
    "ShadowFont",
    "SmallFont",
]

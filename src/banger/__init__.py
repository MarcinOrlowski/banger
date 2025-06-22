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

Classic Unix banner command reimplemented in Python.
"""

from .core import BannerGenerator
from .fonts import DEFAULT_CHAR_SPACING

__all__ = ["BannerGenerator", "DEFAULT_CHAR_SPACING"]

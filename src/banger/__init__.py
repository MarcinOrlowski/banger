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

This is the CLI package. For the library API, use banger_lib.
"""

# Re-export from banger_lib for backward compatibility
from banger_lib import Banger
from banger_lib.fonts import DEFAULT_CHAR_SPACING

# Alias for backward compatibility
BannerGenerator = Banger

__all__ = ["Banger", "BannerGenerator", "DEFAULT_CHAR_SPACING"]

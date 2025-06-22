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

from typing import Dict, Callable, List

from .banner import BannerFont
from .block import BlockFont
from .blur import BlurFont
from .compact import CompactFont
from .core import FontInterface
from .default import DefaultFont
from .fire import FireFont
from .matrix import MatrixFont
from .quadrant import QuadrantFont
from .shadow import ShadowFont
from .small import SmallFont

"""Font factory and management."""

# Font factory - maps font names to factory functions
BUILTIN_FONTS: Dict[str, Callable[[], FontInterface]] = {
    "default": lambda: DefaultFont(),
    "matrix": lambda: MatrixFont(),
    "banner": lambda: BannerFont(),
    "block": lambda: BlockFont(),
    "blur": lambda: BlurFont(),
    "compact": lambda: CompactFont(),
    "fire": lambda: FireFont(),
    "quadrant": lambda: QuadrantFont(),
    "shadow": lambda: ShadowFont(),
    "small": lambda: SmallFont(),
}


def create_font(name: str) -> FontInterface:
    """Create a font instance by name.

    Args:
        name: Font name to create

    Returns:
        Font instance, falls back to default if not found
    """
    if name in BUILTIN_FONTS:
        return BUILTIN_FONTS[name]()

    # Fallback to default
    return BUILTIN_FONTS["default"]()


def get_available_fonts() -> List[str]:
    """Get list of available font type names.

    Returns:
        List of available font type names
    """
    return list(BUILTIN_FONTS.keys())

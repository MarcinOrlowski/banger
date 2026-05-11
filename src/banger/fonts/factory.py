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

from typing import Dict, Callable, List, Type

from .builtin import (
    BannerFont,
    BlockFont,
    BlurFont,
    ClassicFont,
    CompactFont,
    FireFont,
    MatrixFont,
    QuadrantFont,
    ShadowFont,
    SmallFont,
)
from .core import FontInterface

"""Font factory and management."""

# Font factory - maps font names to factory functions
_FONTS: Dict[str, Callable[[], FontInterface]] = {
    "classic": lambda: ClassicFont(),
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


def register_font(name: str, font_class: Type[FontInterface]) -> None:
    """Register a custom font.

    Args:
        name: Name to register the font under
        font_class: Font class (must implement FontInterface)
    """
    _FONTS[name] = lambda: font_class()


def create_font(name: str, fallback: bool = True) -> FontInterface:
    """Create a font instance by name.

    Args:
        name: Font name to create
        fallback: If True, fall back to classic font if not found

    Returns:
        Font instance

    Raises:
        KeyError: If font not found and fallback is False
    """
    if name in _FONTS:
        return _FONTS[name]()

    if fallback:
        return _FONTS["classic"]()

    raise KeyError(f"Font not found: {name}")


def get_available_fonts() -> List[str]:
    """Get list of available font type names.

    Returns:
        List of available font type names
    """
    return list(_FONTS.keys())

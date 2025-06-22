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

from typing import List

"""Font utilities for character processing."""


def calculate_character_width(lines: List[str], trim: bool = True) -> int:
    """Calculate character width from lines.

    This finds the actual content width by removing trailing spaces and taking
    the maximum width needed, which prevents issues with inconsistent padding
    in font files.

    Args:
        lines: List of character line strings
        trim: If True (default), removes trailing spaces when calculating width

    Returns:
        Width of the character (maximum line length)
    """
    if not lines:
        return 0

    if trim:
        # When trim is True (default), use right-stripped line lengths
        max_content_width = max(len(line.rstrip()) for line in lines)
    else:
        # When trim is False, use original line lengths (for spaces, etc.)
        max_content_width = max(len(line) for line in lines)

    return max_content_width


def normalize_character_lines(lines: List[str], trim: bool = True) -> List[str]:
    """Normalize character lines to use consistent width.

    This calculates the actual content width (longest right-stripped line) and
    pads all lines to that width, ensuring consistent character boundaries while
    removing unnecessary trailing spaces.

    Args:
        lines: List of character line strings
        trim: If True (default), removes trailing spaces and uses stripped line lengths

    Returns:
        List of normalized lines padded to consistent width
    """
    if not lines:
        return lines

    if trim:
        # When trim is True (default), calculate content width after right-stripping
        content_width = max(len(line.rstrip()) for line in lines)

        # Normalize all lines: right-strip then pad to content_width
        normalized_lines = []
        for line in lines:
            stripped_line = line.rstrip()
            # Pad to content_width if needed
            padded_line = stripped_line.ljust(content_width)
            normalized_lines.append(padded_line)
    else:
        # When trim is False, use the original line lengths without stripping
        content_width = max(len(line) for line in lines)
        # Don't strip, just pad to max width
        normalized_lines = []
        for line in lines:
            padded_line = line.ljust(content_width)
            normalized_lines.append(padded_line)

    return normalized_lines

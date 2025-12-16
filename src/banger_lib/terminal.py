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

import os
import shutil

"""Terminal utilities for bang"""


def get_terminal_width() -> int:
    """Get terminal width with fallback to 80.

    Checks in order:
    1. COLUMNS environment variable (original banner behavior)
    2. Terminal size query using shutil
    3. Default fallback of 80 columns

    Returns:
        Terminal width in columns
    """
    # 1. Check COLUMNS env var (original behavior)
    if "COLUMNS" in os.environ:
        try:
            width = int(os.environ["COLUMNS"])
            if width > 0:
                return width
        except ValueError:
            pass

    # 2. Try terminal size detection
    try:
        size = shutil.get_terminal_size()
        if size.columns > 0:
            return size.columns
    except Exception:
        pass

    # 3. Default fallback
    return 80

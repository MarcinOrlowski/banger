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

Core banner generation logic with proportional font support.
"""

from typing import List, Optional, Union

from .fonts import (
    _get_character_data_object,
    get_font_height,
    DEFAULT_CHAR_SPACING,
    create_font,
)
from .terminal import get_terminal_width


class BannerGenerator:
    """Generate banners from text using ASCII art characters with proportional spacing support."""

    def __init__(
        self,
        max_width: Optional[int] = None,
        font: Union[str, any] = "quadrant",
        character_width: Optional[int] = None,
    ):
        """Initialize banner generator.

        Args:
            max_width: Maximum width for banner lines. If None, uses terminal width.
            font: Font name (str) or font object to use for rendering
            character_width: Minimum width for each character. If not provided, each character
                takes as much space as it needs, making each font proportional. Setting custom width
                will enforce min fixed width of the character which makes each font act as monospaced.
        """
        self.max_width = max_width or get_terminal_width()
        self.font = font
        self.character_width = character_width

        # Get font height - handle both string names and font objects
        if isinstance(font, str):
            self.font_height = get_font_height(font)
            self._font_obj = create_font(font)
        else:
            # Font object provided directly
            self._font_obj = font
            self.font_height = font.height

        self.lines: List[str] = [""] * self.font_height
        self._truncated = False

    def _clip_character_lines(self, char_lines: List[str], min_width: int) -> List[str]:
        """Clip character lines to calculated width based on minimum width.

        Args:
            char_lines: List of character line strings
            min_width: Minimum width to use

        Returns:
            List of clipped/padded strings with calculated width
        """
        # Calculate actual width: max of min_width and longest right-trimmed line
        actual_width = min_width
        for line in char_lines:
            trimmed_length = len(line.rstrip())
            actual_width = max(actual_width, trimmed_length)

        # Clip and pad all lines to the calculated width
        processed_lines = []
        for line in char_lines:
            if len(line) >= actual_width:
                # Clip if line is longer than actual width
                processed_line = line[:actual_width]
            else:
                # Pad if line is shorter than actual width
                processed_line = line.ljust(actual_width)
            processed_lines.append(processed_line)
        return processed_lines

    def add_character(self, char: str) -> bool:
        """Add a single character to the banner.

        Args:
            char: Character to add

        Returns:
            True if character was added, False if it would exceed max_width
        """
        # Get character data - handle both string names and font objects
        if self._font_obj:
            # Font object provided directly
            char_data = self._font_obj.get_character(char)
            if char_data is None:
                # Try to get default character as fallback
                char_data = self._font_obj.get_character("default")
                if char_data is None:
                    raise RuntimeError(
                        f"TTF font missing both character '{char}' and 'default' fallback"
                    )
        else:
            # Font name string - use existing API
            char_data = _get_character_data_object(char, self.font)
            if char_data is None:
                # Try to get default character as fallback
                char_data = _get_character_data_object("default", self.font)
                if char_data is None:
                    raise RuntimeError(
                        f"Font '{self.font}' missing both character '{char}' and 'default' fallback"
                    )
            # If we got default, continue processing it

        char_lines = char_data.lines
        char_width = (
            char_data.width
        )  # This is now calculated dynamically in get_character_data()

        # Determine effective width and modify character lines if needed
        if self.character_width is not None:
            # Character width override: clip characters to calculated width based on minimum
            char_lines = self._clip_character_lines(char_lines, self.character_width)
            # Calculate actual effective width from the clipped lines (lines are already right-stripped from get_character_data)
            effective_width = (
                max(len(line) for line in char_lines)
                if char_lines
                else self.character_width
            )
        else:
            # Proportional mode: use natural character width (lines are already normalized)
            effective_width = char_width

        # Calculate new line length including spacing (but not for first character)
        spacing_width = DEFAULT_CHAR_SPACING if self.lines[0] else 0
        new_line_length = len(self.lines[0]) + effective_width + spacing_width

        # Check if adding this character would exceed max width
        if new_line_length > self.max_width:
            self._truncated = True
            return False

        # Add the character with spacing (same for both modes)
        for i in range(self.font_height):
            if self.lines[i]:  # Not first character, add spacing
                self.lines[i] += " " * DEFAULT_CHAR_SPACING + char_lines[i]
            else:
                self.lines[i] += char_lines[i]

        return True

    def add_text(self, text: str) -> None:
        """Add text to the banner, processing each character.

        Args:
            text: Text to add to banner
        """
        for char in text:
            if not self.add_character(char):
                break  # Stop on truncation

    def render(self) -> str:
        """Render the banner as a string.

        Returns:
            Complete banner with trailing newlines
        """
        # Right-strip spaces from each line (original behavior)
        stripped_lines = [line.rstrip() for line in self.lines]

        # Add bottom padding based on font configuration
        bottom_padding = 1  # default
        if self._font_obj and hasattr(self._font_obj, "bottom_padding"):
            bottom_padding = self._font_obj.bottom_padding

        # Add empty lines for bottom padding
        padding_lines = [""] * bottom_padding
        all_lines = stripped_lines + padding_lines

        # Format with newlines
        return "\n".join(all_lines) + "\n"

    def is_truncated(self) -> bool:
        """Check if the banner was truncated.

        Returns:
            True if banner was truncated due to width limit
        """
        return self._truncated

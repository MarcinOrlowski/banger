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

from abc import ABC
from typing import List, Optional, Set

from .character_data import CharacterData
from .font_metadata import FontMetadata

"""Base font class providing common functionality."""


class BaseFont(ABC):
    """Abstract base class providing common functionality for fonts.

    All font classes extend this base to get consistent behavior for
    character caching, normalization, width calculation, etc.

    Subclasses must implement:
    - _get_character_data: Get character data for a specific character
    - _get_all_supported_characters: Get set of all supported characters
    """

    _FONT_DATA = {
        "name": "???",
        "height": 7,
        "description": "???",
        "bottom_padding": 1,
        "characters": {
            "default": {
                "lines": [
                    "# # #",
                    " # # ",
                    "# # #",
                    " # # ",
                    "# # #",
                ]
            }
        },
    }

    def __init__(self):
        """Initialize the base font with metadata from _FONT_DATA."""
        metadata = FontMetadata(
            name=self._FONT_DATA["name"],
            height=self._FONT_DATA["height"],
            description=self._FONT_DATA["description"],
            bottom_padding=self._FONT_DATA["bottom_padding"],
            supports_lowercase=self._FONT_DATA.get("supports_lowercase", True),
            supports_uppercase=self._FONT_DATA.get("supports_uppercase", True),
            supports_digits=self._FONT_DATA.get("supports_digits", True),
            supports_punctuation=self._FONT_DATA.get("supports_punctuation", True),
        )

        self._metadata = metadata

    @property
    def metadata(self) -> FontMetadata:
        """Get font metadata."""
        return self._metadata

    @property
    def name(self) -> str:
        """Get the font name."""
        return self._metadata.name

    @property
    def height(self) -> int:
        """Get the font height in lines."""
        return self._metadata.height

    @property
    def description(self) -> str:
        """Get the font description."""
        return self._metadata.description

    @property
    def bottom_padding(self) -> int:
        """Get the font bottom padding in lines."""
        return self._metadata.bottom_padding

    def has_character(self, char: str) -> bool:
        """Check if the font supports a specific character."""
        try:
            return self._get_character_data(char) is not None
        except Exception:
            return False

    def get_character(self, char: str) -> Optional[CharacterData]:
        """Get character data for a specific character."""
        return self._get_character_data(char)

    def get_available_characters(self) -> Set[str]:
        """Get set of all characters supported by this font."""
        return self._get_all_supported_characters()

    # @abstractmethod
    # def _get_character_data(self, char: str) -> Optional[CharacterData]:
    #     """Get character data for a specific character.
    #
    #     Args:
    #         char: Character to get data for
    #
    #     Returns:
    #         CharacterData if available, None otherwise
    #     """
    #     ...

    def _get_character_data(self, char: str) -> Optional[CharacterData]:
        """Get character data from embedded font data."""
        characters = self._FONT_DATA["characters"]

        if char not in characters:
            # If font doesn't support lowercase, try converting to uppercase
            if (
                char.islower()
                and not self._metadata.supports_lowercase
                and self._metadata.supports_uppercase
            ):
                uppercase_char = char.upper()
                if uppercase_char in characters:
                    char = uppercase_char
            # If font doesn't support uppercase, try converting to lowercase
            elif (
                char.isupper()
                and not self._metadata.supports_uppercase
                and self._metadata.supports_lowercase
            ):
                lowercase_char = char.lower()
                if lowercase_char in characters:
                    char = lowercase_char

            # If still not found, try "default" character fallback
            if char not in characters:
                if char != "default" and "default" in characters:
                    char = "default"
                else:
                    return None

        char_info = characters[char]
        lines = char_info.get("lines", [])
        trim = char_info.get("trim", True)

        if not lines:
            return None

        # Normalize lines and calculate width
        normalized_lines = self._normalize_character_lines(lines, trim=trim)
        width = self._calculate_character_width(normalized_lines, trim=trim)

        return CharacterData(lines=normalized_lines, width=width, trim=trim)

    def _get_all_supported_characters(self) -> Set[str]:
        """Get all supported characters."""
        return set(self._FONT_DATA["characters"].keys())

    def _normalize_character_lines(
        self, lines: List[str], trim: bool = True
    ) -> List[str]:
        """Normalize character lines to consistent width.

        Args:
            lines: List of character line strings
            trim: If True, removes trailing spaces

        Returns:
            Normalized lines
        """
        if not lines:
            return lines

        if trim:
            content_width = max(len(line.rstrip()) for line in lines)
            normalized_lines = []
            for line in lines:
                stripped_line = line.rstrip()
                padded_line = stripped_line.ljust(content_width)
                normalized_lines.append(padded_line)
        else:
            content_width = max(len(line) for line in lines)
            normalized_lines = []
            for line in lines:
                padded_line = line.ljust(content_width)
                normalized_lines.append(padded_line)

        return normalized_lines

    def _calculate_character_width(self, lines: List[str], trim: bool = True) -> int:
        """Calculate character width from lines.

        Args:
            lines: List of character line strings
            trim: If True, removes trailing spaces when calculating width

        Returns:
            Character width
        """
        if not lines:
            return 0

        if trim:
            return max(len(line.rstrip()) for line in lines)
        else:
            return max(len(line) for line in lines)

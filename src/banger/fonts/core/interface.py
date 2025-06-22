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

from typing import Protocol, Set, Optional
from .character_data import CharacterData
from .font_metadata import FontMetadata

"""Font interface protocol for banner fonts."""


class FontInterface(Protocol):
    """Protocol defining the interface that all banner fonts must implement."""

    @property
    def metadata(self) -> FontMetadata:
        """Get font metadata including name, height, description, etc.

        Returns:
            FontMetadata object containing font information
        """
        ...

    @property
    def name(self) -> str:
        """Get the font name.

        Returns:
            Font name string
        """
        ...

    @property
    def height(self) -> int:
        """Get the font height in lines.

        Returns:
            Height of the font in lines
        """
        ...

    @property
    def description(self) -> str:
        """Get the font description.

        Returns:
            Human-readable font description
        """
        ...

    def has_character(self, char: str) -> bool:
        """Check if the font supports a specific character.

        Args:
            char: Character to check

        Returns:
            True if the font has this character
        """
        ...

    def get_character(self, char: str) -> Optional[CharacterData]:
        """Get character data for a specific character.

        Args:
            char: Character to get data for

        Returns:
            CharacterData if available, None otherwise
        """
        ...

    def get_available_characters(self) -> Set[str]:
        """Get set of all characters supported by this font.

        Returns:
            Set of character strings
        """
        ...

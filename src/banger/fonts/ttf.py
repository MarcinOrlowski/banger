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

from typing import Dict, Optional, Tuple
from pathlib import Path

from .core import FontInterface, CharacterData, FontMetadata

"""TTF Banner Font Implementation

This module provides TTF font rendering using PIL/Pillow for bitmap generation
and quadrant block characters for 2×2 pixel control.

Quadrant blocks used: ▘ ▝ ▀ ▖ ▌ ▞ ▛ ▗ ▚ ▐ ▜ ▄ ▙ ▟ █
"""


class TtfFont(FontInterface):
    """TTF font implementation using PIL/Pillow rendering and quadrant rasterization."""

    # Quadrant block characters for 2×2 pixel control
    # Each quadrant represents a 2×2 pixel area
    QUADRANT_BLOCKS = {
        (False, False, False, False): " ",  # No pixels
        (True, False, False, False): "▘",  # Top-left
        (False, True, False, False): "▝",  # Top-right
        (True, True, False, False): "▀",  # Top half
        (False, False, True, False): "▖",  # Bottom-left
        (True, False, True, False): "▌",  # Left half
        (False, True, True, False): "▞",  # Diagonal \
        (True, True, True, False): "▛",  # Top and bottom-left
        (False, False, False, True): "▗",  # Bottom-right
        (True, False, False, True): "▚",  # Anti-diagonal /
        (False, True, False, True): "▐",  # Right half
        (True, True, False, True): "▜",  # Top and bottom-right
        (False, False, True, True): "▄",  # Bottom half
        (True, False, True, True): "▙",  # Left and bottom-right
        (False, True, True, True): "▟",  # Right and bottom-left
        (True, True, True, True): "█",  # Full block
    }

    def __init__(self, font_path: str, font_size: int = 48, character_height: int = 7):
        """Initialize TTF font.

        Args:
            font_path: Path to TTF font file
            font_size: Font size in points for rendering
            character_height: Target character height in terminal lines
        """
        self.font_path = Path(font_path)
        self.font_size = font_size
        self.character_height = character_height
        self._font = None
        self._character_cache: Dict[str, CharacterData] = {}
        self._metadata_name_override = None

        # Validate font file exists
        if not self.font_path.exists():
            raise FileNotFoundError(f"TTF font file not found: {font_path}")

    def _ensure_font_loaded(self) -> None:
        """Lazy load PIL font object."""
        if self._font is None:
            try:
                from PIL import Image, ImageDraw, ImageFont

                self._font = ImageFont.truetype(str(self.font_path), self.font_size)
                self._PIL_Image = Image
                self._PIL_ImageDraw = ImageDraw
            except ImportError:
                raise ImportError(
                    "PIL/Pillow is required for TTF font support. "
                    "Install with: pip install Pillow"
                )

    def _render_character_bitmap(self, char: str) -> Tuple[list, int, int]:
        """Render character to bitmap using PIL.

        Args:
            char: Character to render

        Returns:
            Tuple of (bitmap_2d, width, height) where bitmap_2d is list of lists of booleans
        """
        self._ensure_font_loaded()

        # Get text bounding box
        bbox = self._font.getbbox(char)
        if bbox == (0, 0, 0, 0):  # Character not supported
            return [], 0, 0

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        # Create image with some padding
        padding = 4
        img_width = width + 2 * padding
        img_height = height + 2 * padding

        # Create white background image
        image = self._PIL_Image.new("L", (img_width, img_height), 255)
        draw = self._PIL_ImageDraw.Draw(image)

        # Draw black text
        draw.text((padding - bbox[0], padding - bbox[1]), char, font=self._font, fill=0)

        # Convert to 2D boolean array (True = pixel set)
        bitmap_2d = []
        for y in range(img_height):
            row = []
            for x in range(img_width):
                pixel_value = image.getpixel((x, y))
                # Consider pixel "set" if it's darker than middle gray
                row.append(pixel_value < 128)
            bitmap_2d.append(row)

        # Clip bitmap to actual content bounding box (X-axis only)
        clipped_bitmap, clipped_width = self._clip_bitmap_to_content(
            bitmap_2d, img_width, img_height
        )

        return clipped_bitmap, clipped_width, img_height

    def _clip_bitmap_to_content(
        self, bitmap_2d: list, width: int, height: int
    ) -> Tuple[list, int]:
        """Clip bitmap to actual content bounding box on X-axis only.

        This makes all fonts effectively proportional by removing empty space
        on the left and right sides of each character.

        Args:
            bitmap_2d: 2D list of booleans representing pixels
            width: Original bitmap width
            height: Original bitmap height

        Returns:
            Tuple of (clipped_bitmap_2d, clipped_width)
        """
        if not bitmap_2d or width == 0 or height == 0:
            return bitmap_2d, width

        # Find leftmost and rightmost columns with any set pixels
        left_bound = width
        right_bound = -1

        for y in range(height):
            for x in range(width):
                if bitmap_2d[y][x]:  # Pixel is set
                    left_bound = min(left_bound, x)
                    right_bound = max(right_bound, x)

        # If no pixels found, return minimal bitmap
        if right_bound == -1:
            # Return single column of empty pixels for space characters
            clipped_bitmap = []
            for y in range(height):
                clipped_bitmap.append([False])
            return clipped_bitmap, 1

        # Clip the bitmap to the content bounds (X-axis only)
        clipped_width = right_bound - left_bound + 1
        clipped_bitmap = []

        for y in range(height):
            clipped_row = []
            for x in range(left_bound, right_bound + 1):
                clipped_row.append(bitmap_2d[y][x])
            clipped_bitmap.append(clipped_row)

        return clipped_bitmap, clipped_width

    def _bitmap_to_quadrants(
        self, bitmap_2d: list, width: int, height: int
    ) -> Tuple[list, int]:
        """Convert bitmap to quadrant block characters.

        Args:
            bitmap_2d: 2D list of booleans representing pixels
            width: Bitmap width
            height: Bitmap height

        Returns:
            Tuple of (lines, character_width) where lines is list of strings
        """
        if not bitmap_2d or width == 0 or height == 0:
            return [""], 0

        # Calculate quadrant dimensions
        quad_width = (width + 1) // 2  # Round up
        quad_height = (height + 1) // 2  # Round up

        lines = []
        for quad_y in range(quad_height):
            line = ""
            for quad_x in range(quad_width):
                # Get 2×2 pixel values for this quadrant
                y_base = quad_y * 2
                x_base = quad_x * 2

                # Sample 4 pixels (handle edge cases where bitmap doesn't align perfectly)
                top_left = (
                    bitmap_2d[y_base][x_base]
                    if y_base < height and x_base < width
                    else False
                )
                top_right = (
                    bitmap_2d[y_base][x_base + 1]
                    if y_base < height and x_base + 1 < width
                    else False
                )
                bottom_left = (
                    bitmap_2d[y_base + 1][x_base]
                    if y_base + 1 < height and x_base < width
                    else False
                )
                bottom_right = (
                    bitmap_2d[y_base + 1][x_base + 1]
                    if y_base + 1 < height and x_base + 1 < width
                    else False
                )

                # Get corresponding quadrant character
                quadrant_key = (top_left, top_right, bottom_left, bottom_right)
                char = self.QUADRANT_BLOCKS.get(quadrant_key, " ")
                line += char

            lines.append(line)

        # For TTF fonts, preserve natural bitmap proportions
        # No height scaling - let the font render at its natural size
        # The bitmap size is determined by the font size and should not be artificially constrained

        return lines, len(lines[0]) if lines else 0

    def _scale_bitmap_to_height(
        self, bitmap_2d: list, current_height: int, target_height: int
    ) -> list:
        """Scale bitmap to target height using nearest neighbor interpolation.

        Args:
            bitmap_2d: 2D list of booleans representing pixels
            current_height: Current height of the bitmap
            target_height: Desired height of the bitmap (in pixels)

        Returns:
            Scaled bitmap as 2D list of booleans
        """
        if not bitmap_2d or current_height == 0 or target_height == 0:
            return bitmap_2d

        if current_height == target_height:
            return bitmap_2d

        scaled_bitmap = []

        # Scale using nearest neighbor interpolation
        for y in range(target_height):
            # Map target y to source y
            source_y = int(y * current_height / target_height)
            source_y = min(source_y, current_height - 1)  # Clamp to valid range

            # Copy the row from source
            scaled_bitmap.append(bitmap_2d[source_y][:])

        return scaled_bitmap

    def get_character(self, char: str) -> Optional[CharacterData]:
        """Get character data for TTF font.

        Args:
            char: Character to get data for

        Returns:
            CharacterData object or None if character not supported
        """
        # Check cache first
        if char in self._character_cache:
            return self._character_cache[char]

        # Render character to bitmap
        bitmap_2d, width, height = self._render_character_bitmap(char)

        if not bitmap_2d:
            # Character not supported
            self._character_cache[char] = None
            return None

        # Scale bitmap to desired character height
        # character_height is in terminal lines, we need pixels (quadrants use 2x2 pixels)
        target_pixel_height = self.character_height * 2
        scaled_bitmap = self._scale_bitmap_to_height(
            bitmap_2d, height, target_pixel_height
        )

        # Convert bitmap to quadrant blocks
        lines, char_width = self._bitmap_to_quadrants(
            scaled_bitmap, width, target_pixel_height
        )

        # Create character data
        char_data = CharacterData(lines=lines, width=char_width)

        # Cache result
        self._character_cache[char] = char_data
        return char_data

    @property
    def metadata(self) -> FontMetadata:
        """Get font metadata."""
        name = self._metadata_name_override or f"ttf_{self.font_path.stem}"
        return FontMetadata(
            name=name,
            description=f"TTF font from {self.font_path.name}",
            height=self.character_height,
            supports_lowercase=True,
            supports_uppercase=True,
        )

    @property
    def height(self) -> int:
        """Get the font height in lines."""
        # Return the configured character height since we now scale to this
        return self.character_height


def list_system_ttf_fonts(sort_by="path"):
    """List common system TTF and OTF font locations.

    Args:
        sort_by: Sort by "name" (font name) or "path" (file path)

    Returns:
        List of (font_name, font_path) tuples for available system fonts
    """
    import platform
    import glob
    import os

    system_fonts = []
    system = platform.system()

    # Common font directories by OS with expanded coverage
    font_patterns = []
    if system == "Linux":
        # Base directories to search
        base_dirs = [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            "~/.fonts",
            "~/.local/share/fonts",
        ]

        # Subdirectories to check within each base
        subdirs = ["", "truetype", "opentype", "TTF", "OTF", "type1"]

        # Build patterns for both TTF and OTF files
        for base in base_dirs:
            for subdir in subdirs:
                if subdir:
                    path = f"{base}/{subdir}"
                else:
                    path = base
                # Add patterns for both lowercase and uppercase extensions
                font_patterns.extend(
                    [
                        f"{path}/**/*.ttf",
                        f"{path}/**/*.TTF",
                        f"{path}/**/*.otf",
                        f"{path}/**/*.OTF",
                    ]
                )

    elif system == "Darwin":  # macOS
        base_dirs = ["/System/Library/Fonts", "/Library/Fonts", "~/Library/Fonts"]

        for base in base_dirs:
            font_patterns.extend(
                [
                    f"{base}/**/*.ttf",
                    f"{base}/**/*.TTF",
                    f"{base}/**/*.otf",
                    f"{base}/**/*.OTF",
                ]
            )

    elif system == "Windows":
        font_patterns = [
            "C:/Windows/Fonts/**/*.ttf",
            "C:/Windows/Fonts/**/*.TTF",
            "C:/Windows/Fonts/**/*.otf",
            "C:/Windows/Fonts/**/*.OTF",
        ]

    # Find font files
    seen_paths = set()  # To avoid duplicates
    for pattern in font_patterns:
        expanded_pattern = os.path.expanduser(pattern)
        try:
            for font_path in glob.glob(expanded_pattern, recursive=True):
                # Normalize path to avoid duplicates
                normalized_path = os.path.normpath(font_path)
                if normalized_path not in seen_paths:
                    seen_paths.add(normalized_path)
                    font_name = os.path.splitext(os.path.basename(font_path))[0]
                    system_fonts.append((font_name, font_path))
        except (OSError, PermissionError):
            # Skip directories we can't access
            continue

    # Sort based on the specified criteria
    if sort_by == "name":
        return sorted(system_fonts, key=lambda x: x[0].lower())
    else:  # sort_by == "path"
        return sorted(system_fonts, key=lambda x: x[1].lower())

# Product Requirements Document: TTF Font Support

## Overview

This PRD documents the TTF (TrueType Font) support feature in banger, which enables users to convert
any system TTF font into ASCII art banners using Unicode quadrant block characters.

## Problem Statement

Users are limited to the built-in ASCII fonts and want to use their system's installed TTF fonts to
create unique banners. The ability to leverage existing system fonts would greatly expand creative
possibilities.

## Goals

1. Enable users to create banners using any TTF font installed on their system
2. Provide automatic font discovery to help users find available fonts
3. Maintain consistent output quality through intelligent scaling
4. Offer flexible control over rendering quality and output size

## Success Metrics

- Users can successfully render text using any valid TTF font file
- Output quality is consistent regardless of font size or style
- Performance remains acceptable for typical use cases
- Feature integrates seamlessly with existing banger functionality

## Requirements

### Functional Requirements

#### Core TTF Rendering

1. **Font Loading**
  - Accept path to any valid TTF font file via `--ttf-font` parameter
  - Validate font file exists and is readable
  - Lazy-load PIL/Pillow dependencies only when TTF features are used
  - Provide clear error messages for missing dependencies or invalid fonts

2. **Character Rendering**
  - Render individual characters to high-resolution bitmaps using PIL/Pillow
  - Support full Unicode character range that the font provides
  - Cache rendered characters to improve performance for repeated characters
  - Provide fallback to 'default' character for unsupported glyphs

3. **Bitmap to ASCII Conversion**
  - Convert rendered bitmaps to Unicode quadrant block characters
  - Use 2×2 pixel sampling for quadrant mapping
  - Support all 16 quadrant block variations: `▘ ▝ ▀ ▖ ▌ ▞ ▛ ▗ ▚ ▐ ▜ ▄ ▙ ▟ █`
  - Automatically clip horizontal whitespace for proportional spacing

4. **Height Scaling**
  - Scale rendered bitmaps to match desired terminal line height
  - Use nearest-neighbor interpolation for scaling
  - Maintain aspect ratio during scaling operations

#### User Controls

1. **Output Size Control**
  - `--ttf-lines LINES`: Control output height in terminal lines (default: 7)
  - Support range from 3 to reasonable maximum (e.g., 50 lines)
  - Ensure consistent output height regardless of font or rendering size

2. **Rendering Quality Control**
  - `--ttf-size SIZE`: Override automatic font size calculation
  - Auto-calculate optimal size when not specified (lines × 8 points)
  - Allow manual override for quality vs. performance trade-offs

3. **Font Discovery**
  - `--ttf-list`: List all system TTF fonts with paths
  - `--ttf-list-sort [name|path]`: Control sort order of font list
  - Search common system font directories based on OS platform

### Non-Functional Requirements

1. **Performance**
  - Character rendering should complete in reasonable time (<1s for typical text)
  - Implement character caching to avoid re-rendering
  - Minimize memory usage through efficient bitmap handling

2. **Compatibility**
  - Support Linux, macOS, and Windows font directories
  - Work with standard TTF font files
  - Graceful degradation when PIL/Pillow not installed

3. **Integration**
  - TTF fonts work seamlessly with existing banger features
  - Respect max-width settings and other formatting options
  - Support all text processing features (word wrapping, etc.)

## User Experience

### Basic Usage

```ascii
# Simple usage with auto-calculated parameters
banger --ttf-font "/path/to/font.ttf" "Hello World"

# Control output size
banger --ttf-font "/path/to/font.ttf" --ttf-lines 10 "Large Text"

# Override rendering quality
banger --ttf-font "/path/to/font.ttf" --ttf-size 100 --ttf-lines 5 "Quality"
```

### Font Discovery

```ascii
# List all system fonts
banger --ttf-list

# Sort by font name
banger --ttf-list --ttf-list-sort name
```

### Error Handling

- Clear error when font file not found
- Helpful message when PIL/Pillow not installed
- Graceful handling of unsupported characters

## Technical Implementation

### Architecture

1. **TtfFont Class**
  - Implements FontInterface for compatibility
  - Handles all TTF-specific rendering logic
  - Manages character cache and bitmap operations

2. **Bitmap Processing Pipeline**
  - Render character → Clip whitespace → Scale to height → Convert to quadrants
  - Each step is modular and testable

3. **Integration Points**
  - CLI argument parsing for TTF-specific options
  - Font factory integration for seamless usage
  - Standard FontInterface compliance

### Dependencies

- PIL/Pillow (optional): Required only for TTF functionality
- Python 3.8+: Standard library features

## Future Considerations

1. **Antialiasing Support**: Currently uses 1-bit conversion, could explore grayscale
2. **Kerning**: Implement proper character spacing based on font metrics
3. **Multi-line Layout**: Better support for paragraph formatting
4. **Font Effects**: Bold, italic synthesis for fonts lacking variants
5. **Performance**: GPU acceleration for large-scale rendering

## Acceptance Criteria

1. ✓ Users can render text using any valid TTF font file
2. ✓ Output height is controllable via `--ttf-lines` parameter
3. ✓ Font size auto-calculates sensibly when not specified
4. ✓ System font discovery works on major platforms
5. ✓ Character caching improves performance
6. ✓ Errors are handled gracefully with helpful messages
7. ✓ Integration with existing banger features is seamless
8. ✓ Documentation clearly explains usage and parameters

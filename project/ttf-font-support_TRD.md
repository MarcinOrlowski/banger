# Technical Requirements Document: TTF Font Support

## Overview

This TRD provides the technical design and implementation details for the TTF font support feature
in banger, enabling conversion of TrueType fonts to ASCII art using Unicode quadrant block
characters.

## Architecture Overview

### Component Diagram

```text
CLI Layer (cli.py)
    ├── TTF Arguments Parser
    └── Font Factory Integration
          │
TTF Font Layer (fonts/ttf.py)
    ├── TtfFont Class (implements FontInterface)
    ├── Bitmap Renderer (PIL/Pillow)
    ├── Bitmap Scaler
    └── Quadrant Converter
          │
Core Layer (core.py)
    └── BannerGenerator (unchanged)
```

## Technical Design

### 1. Font Interface Integration

The `TtfFont` class implements the standard `FontInterface` to ensure compatibility:

```python
class TtfFont(FontInterface):
    def get_character(self, char: str) -> Optional[CharacterData]

        @property
        def metadata(self) -> FontMetadata

        @property
        def height(self) -> int
```

### 2. Character Rendering Pipeline

The rendering process follows these steps:

1. **Font Loading** (lazy-loaded on first use)

   ```python
   PIL.ImageFont.truetype(font_path, font_size)
   ```

2. **Bitmap Generation**

   - Create white background image with padding
   - Render character in black using PIL
   - Convert to 2D boolean array (True = black pixel)

3. **Bitmap Clipping**

   - Remove horizontal whitespace for proportional spacing
   - Preserve vertical space for consistent height

4. **Height Scaling**

   - Calculate target pixel height: `terminal_lines × 2`
   - Apply nearest-neighbor interpolation
   - Maintain horizontal proportions

5. **Quadrant Conversion**

   - Sample 2×2 pixel blocks
   - Map to appropriate Unicode character
   - Build line-by-line output

### 3. Quadrant Block Mapping

```python
QUADRANT_BLOCKS = {
    (False, False, False, False): ' ',  # Empty
    (True, False, False, False): '▘',  # Top-left
    (False, True, False, False): '▝',  # Top-right
    (True, True, False, False): '▀',  # Top half
    (False, False, True, False): '▖',  # Bottom-left
    (True, False, True, False): '▌',  # Left half
    (False, True, True, False): '▞',  # Diagonal \
    (True, True, True, False): '▛',  # Top and bottom-left
    (False, False, False, True): '▗',  # Bottom-right
    (True, False, False, True): '▚',  # Anti-diagonal /
    (False, True, False, True): '▐',  # Right half
    (True, True, False, True): '▜',  # Top and bottom-right
    (False, False, True, True): '▄',  # Bottom half
    (True, False, True, True): '▙',  # Bottom and left
    (False, True, True, True): '▟',  # Bottom and right
    (True, True, True, True): '█',  # Full block
}
```

### 4. Parameter Design

#### User-Facing Parameters

- `--ttf-font PATH`: Path to TTF font file
- `--ttf-lines N`: Output height in terminal lines (default: 7)
- `--ttf-size N`: Font rendering size in points (auto-calculated if omitted)
- `--ttf-list`: List system fonts
- `--ttf-list-sort [name|path]`: Sort order for font listing

#### Auto-Calculation Logic

```python
if ttf_size is None:
    ttf_size = max(24, ttf_lines * 8)
```

### 5. Caching Strategy

Character-level caching to optimize performance:

```python
class TtfFont:
    def __init__(self, ...):
        self._character_cache: Dict[str, CharacterData] = {}

    def get_character(self, char: str):
        if char in self._character_cache:
            return self._character_cache[char]
        # ... render character ...
        self._character_cache[char] = char_data
        return char_data
```

### 6. Font Discovery

Platform-specific font directories:

```python
# Linux
"~/.fonts/**/*.ttf"
"~/.local/share/fonts/**/*.ttf"
"/usr/share/fonts/truetype/**/*.ttf"
"/usr/local/share/fonts/**/*.ttf"

# macOS
"~/Library/Fonts/**/*.ttf"
"/System/Library/Fonts/**/*.ttf"
"/Library/Fonts/**/*.ttf"

# Windows
"C:/Windows/Fonts/**/*.ttf"
```

## Implementation Details

### 1. Error Handling

- **Missing Font File**: FileNotFoundError with clear message
- **Missing PIL/Pillow**: ImportError with installation instructions
- **Unsupported Character**: Fallback to 'default' character
- **Invalid Parameters**: Validation in CLI argument parser

### 2. Performance Considerations

- **Lazy Loading**: PIL/Pillow loaded only when needed
- **Character Cache**: Avoid re-rendering same characters
- **Efficient Scaling**: Nearest-neighbor for speed
- **Bitmap Clipping**: Reduce memory usage

### 3. Memory Management

- Cache size unbounded (acceptable for typical usage)
- Bitmap data converted to string lines immediately
- Original PIL images not retained

### 4. Integration Points

#### CLI Integration

```python
# In cli.py
if args.ttf_font:
    ttf_font = TtfFont(args.ttf_font, ttf_size, args.ttf_lines)
    font_name = ttf_font  # Direct object usage
```

#### BannerGenerator Compatibility

- TtfFont object passed directly as font parameter
- BannerGenerator checks for font object vs. string name
- No changes required to core banner logic

## Testing Strategy

### Unit Tests

1. **Bitmap Rendering**

   - Verify character renders to expected size
   - Test edge cases (missing glyphs, special chars)

2. **Scaling Algorithm**

   - Test various scale factors
   - Verify output dimensions

3. **Quadrant Conversion**

   - Test all 16 quadrant patterns
   - Verify edge alignment

### Integration Tests

1. **CLI Parameter Handling**

   - Test all parameter combinations
   - Verify auto-calculation logic

2. **Font Discovery**

   - Mock file system for consistent tests
   - Test sorting options

3. **End-to-End Rendering**

   - Test with various fonts and text
   - Verify output consistency

## Security Considerations

1. **File Access**

   - Only read access to font files
   - Path validation to prevent directory traversal

2. **Resource Limits**

   - Reasonable maximum font size
   - Character cache could be bounded if needed

3. **Input Validation**

   - Font path sanitization
   - Parameter range validation

## Deployment Notes

### Dependencies

- **Required**: Python 3.8+
- **Optional**: PIL/Pillow (for TTF support)

### Installation

```ascii
# Without TTF support
pip install banger

# With TTF support
pip install banger[ttf]
```

### Compatibility

- **Operating Systems**: Linux, macOS, Windows
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Terminal Requirements**: Unicode support for quadrant blocks

## Future Enhancements

1. **Advanced Rendering**

   - Grayscale support using more Unicode blocks
   - Subpixel rendering for smoother edges

2. **Font Features**

   - Kerning support
   - Ligature handling
   - Style synthesis (bold, italic)

3. **Performance**

   - Parallel character rendering
   - Persistent cache between runs
   - C extension for critical paths

4. **User Experience**

   - Font preview mode
   - Interactive font selector
   - Web service API

## Acceptance Criteria

- [x] PIL/Pillow integration works correctly
- [x] Character rendering produces valid bitmaps
- [x] Scaling maintains readable output
- [x] Quadrant conversion preserves character shape
- [x] Parameter auto-calculation is sensible
- [x] Font discovery works on major platforms
- [x] Caching improves performance measurably
- [x] Error messages are helpful and actionable
- [x] Integration requires no core changes
- [x] Tests provide adequate coverage

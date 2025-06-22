# Proportional Font Design for banger

## Current Problem

- We have two separate font sets (CHARACTERS and ALL_CAPS_CHARACTERS)
- All characters are padded to a fixed width
- No support for proportional spacing

## Proposed Solution

### Single Font Set with Natural Widths

Each character will be stored at its natural width:

- 'I' might be 3 characters wide
- 'M' might be 7 characters wide
- 'A' might be 7 characters wide

### Font Data Structure

```python
FONT_DATA = {
    'A': {
        'lines': [
            "   #   ",
            "  # #  ",
            " #   # ",
            "#     #",
            "#######",
            "#     #",
            "#     #"
        ],
        'width': 7
    },
    'I': {
        'lines': [
            "###",
            " # ",
            " # ",
            " # ",
            " # ",
            " # ",
            "###"
        ],
        'width': 3
    },
    # Lowercase variants
    'a': {
        'lines': [
            "     ",
            "     ",
            "  #  ",
            " # # ",
            "#####",
            "#   #",
            "#   #"
        ],
        'width': 5  # Natural width
    }
}
```

### Spacing Modes

1. **Proportional** (`--spacing proportional`):
  - Use character's natural width + inter-character spacing
  - More compact, professional appearance

2. **Fixed-width** (`--spacing fixed`):
  - Pad all characters to maximum width in set
  - Maintains current behavior

### Character Style Modes

1. **Default** (`--style default`):
  - Mixed case with cursive-style lowercase

2. **All-caps** (`--style all-caps`):
  - Lowercase uses smaller uppercase shapes

### Combined Options

```ascii
# Current behavior (fixed-width, mixed case)
banger "Hello"

# Proportional spacing with mixed case  
banger --spacing proportional "Hello"

# Fixed spacing with all-caps style
banger --style all-caps "Hello"  

# Proportional spacing with all-caps style
banger --spacing proportional --style all-caps "Hello"
```

## Implementation Plan

1. Redesign font data structure to include natural widths
2. Update core rendering logic to handle variable widths
3. Add spacing mode support
4. Separate style from spacing concerns
5. Maintain backward compatibility

## Benefits

- Single font set eliminates duplication
- More flexible and maintainable
- Better typography with proportional spacing
- Cleaner separation of concerns
- Future-ready for additional fonts/styles

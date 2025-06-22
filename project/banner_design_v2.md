# Python Banner Tool - Design Document v2

## Executive Summary

A focused Python implementation of the classic Unix `banner` command that maintains 100%
compatibility while leveraging Python's strengths for maintainability and distribution.

## Design Principles

1. **Compatibility First**: Exact output match with classic banner
2. **Zero Dependencies**: Core functionality requires only Python stdlib
3. **Simple Architecture**: Minimal code structure for maximum reliability
4. **Easy Distribution**: Single package installable via pip

## Technical Architecture

### Package Structure (Simplified)

```
banger/
├── src/
│   └── banner/
│       ├── __init__.py
│       ├── __main__.py      # CLI entry point
│       ├── core.py          # Banner generation
│       ├── fonts.py         # Character definitions
│       └── terminal.py      # Terminal utilities
├── tests/
│   ├── test_core.py
│   ├── test_compatibility.py
│   └── test_cli.py
├── pyproject.toml
├── setup.py
├── README.md
└── LICENSE
```

### Core Components

#### 1. Character Storage (fonts.py)

```python
# Exact representation from letters.h
CHAR_HEIGHT = 7
CHAR_SPACING = 2

CHARACTERS = {
    'A': (
        "   #   ",
        "  # #  ",
        " #   # ",
        "#     #",
        "#######",
        "#     #",
        "#     #"
    ),
    # ... all other characters
}
```

#### 2. Banner Generator (core.py)

```python
class BannerGenerator:
    def __init__(self, width=None):
        self.width = width or get_terminal_width()
        self.lines = [''] * CHAR_HEIGHT

    def add_character(self, char):
        """Add a character to current banner"""
        if char not in CHARACTERS:
            return False

        char_lines = CHARACTERS[char]
        for i in range(CHAR_HEIGHT):
            new_line = self.lines[i] + char_lines[i] + (' ' * CHAR_SPACING)
            if len(new_line) > self.width:
                return False  # Truncation point
            self.lines[i] = new_line
        return True

    def render(self):
        """Return the complete banner"""
        return '\n' + '\n'.join(line.rstrip() for line in self.lines) + '\n'
```

#### 3. Terminal Width Detection (terminal.py)

```python
import os
import shutil


def get_terminal_width():
    """Get terminal width with fallback to 80"""
    # 1. Check COLUMNS env var (original behavior)
    if 'COLUMNS' in os.environ:
        try:
            return int(os.environ['COLUMNS'])
        except ValueError:
            pass

    # 2. Try terminal size detection
    try:
        size = shutil.get_terminal_size()
        return size.columns
    except:
        pass

    # 3. Default fallback
    return 80
```

#### 4. CLI Interface (__main__.py)

```python
import sys
from .core import BannerGenerator
from .terminal import get_terminal_width


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Handle help flags
    if sys.argv[1] in ('-h', '--help'):
        print_usage()
        sys.exit(0)

    # Handle -- separator (compatibility)
    args = sys.argv[1:]
    if args[0] == '--':
        args = args[1:]

    # Process each word as separate banner
    width = get_terminal_width()
    for word in args:
        banner = BannerGenerator(width)
        word = word.upper().replace('\t', ' ').replace('\n', ' ')

        for char in word:
            if not banner.add_character(char):
                break  # Truncation

        print(banner.render())
```

### Key Implementation Details

1. **Text Processing**:
  - Convert to uppercase: `text.upper()`
  - Normalize whitespace: Replace all whitespace with spaces
  - Handle each argument as separate banner

2. **Truncation Logic**:
  - Check line length before adding each character
  - Stop adding characters when width exceeded
  - No partial character rendering

3. **Output Format**:
  - Leading newline before banner
  - Each line of banner
  - Trailing newline after banner
  - Right-side spaces trimmed from each line

4. **Error Handling**:
  - Unknown characters silently ignored
  - Width detection failures default to 80
  - No exceptions thrown to user

### Testing Strategy

1. **Compatibility Tests**:
  - Compare output with reference C implementation
  - Test all supported characters
  - Verify truncation behavior

2. **Unit Tests**:
  - Character rendering
  - Width detection
  - Text preprocessing

3. **Integration Tests**:
  - CLI argument handling
  - Multi-word banners
  - Edge cases (empty input, special chars)

### Distribution Plan

1. **Package Metadata**:
   ```toml
   [project]
   name = "banger"
   version = "1.0.0"
   description = "Classic Unix banner command in Python"
   requires-python = ">=3.8"
   
   [project.scripts]
   banner = "banner.__main__:main"
   ```

2. **Installation**:
   ```ascii
   pip install banger
   banger "HELLO WORLD"
   ```

### Performance Considerations

- Character lookup: O(1) using dict
- String concatenation: Use list join for efficiency
- Memory: Fixed height arrays, linear with input length
- Target: <50ms for typical 10-char input

### Compatibility Matrix

| Feature               | Original | Python Implementation |
|-----------------------|----------|-----------------------|
| Uppercase letters     | ✓        | ✓                     |
| Numbers               | ✓        | ✓                     |
| Special chars         | ✓        | ✓                     |
| Lowercase → uppercase | ✓        | ✓                     |
| Width detection       | ✓        | ✓                     |
| COLUMNS env var       | ✓        | ✓                     |
| Multiple arguments    | ✓        | ✓                     |
| -- separator          | ✓        | ✓                     |

### Development Phases

1. **Phase 1**: Core implementation (1 day)
  - Character definitions
  - Banner generation logic
  - Basic CLI

2. **Phase 2**: Compatibility (0.5 day)
  - Terminal width detection
  - Exact output matching
  - Edge case handling

3. **Phase 3**: Packaging (0.5 day)
  - Setup packaging files
  - Create test suite
  - Documentation

### Success Criteria

1. Binary compatibility with original banner output
2. Pip installable with no dependencies
3. Cross-platform support (Linux, macOS, Windows)
4. Performance under 50ms for typical usage

## Next Steps

1. Implement core functionality
2. Validate against original C implementation
3. Package for PyPI distribution
4. Create comprehensive test suite

# Python Banner Tool - Design Document v1

## Overview

A Python-based replacement for the classic Unix `banner` command that prints text in large ASCII art
letters.

## Core Features (from original C implementation)

1. **Character Support**:

- Uppercase letters A-Z
- Numbers 0-9
- Special characters: `# ~ ! @ $ % ^ & * ( ) _ + = { } [ ] | \ : ; " ' > < . , ? / - space`

1. **Display Characteristics**:

- Fixed height characters (7 lines)
- Variable width characters
- 2-space separation between characters
- Automatic terminal width detection
- Truncation for oversized banners

1. **Input Processing**:

- Converts lowercase to uppercase
- Converts all whitespace to spaces
- Handles multiple words as separate banners

## Proposed Python Architecture

### 1. Module Structure

```ascii
banger/
├── src/
│   ├── __init__.py
│   ├── __main__.py          # Entry point for `python -m banger`
│   ├── core.py              # Core banner generation logic
│   ├── fonts/
│   │   ├── __init__.py
│   │   └── classic.py       # Classic 7-line font definitions
│   ├── terminal.py          # Terminal width detection
│   └── cli.py               # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_fonts.py
│   ├── test_terminal.py
│   └── test_cli.py
├── setup.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

### 2. Key Components

#### Font Storage (fonts/classic.py)

- Store character definitions as dictionaries
- Each character is a list of 7 strings
- Support for easy font addition/modification

#### Core Logic (core.py)

- `Banner` class for generating banners
- Methods:
  - `add_character()`: Add a character to the banner
  - `generate()`: Create the complete banner
  - `format_text()`: Process input text (uppercase, whitespace)

#### Terminal Handling (terminal.py)

- Detect terminal width from:
  1. COLUMNS environment variable
  2. Terminal size query (using `shutil.get_terminal_size()`)
  3. Default to 80 characters

#### CLI Interface (cli.py)

- Argument parsing using `argparse`
- Support for:
  - Multiple words (each as separate banner)
  - Help/version flags
  - Width override option

## Improvements Over Original

1. **Extensibility**:

- Plugin system for custom fonts
- JSON/YAML font definition support
- Font preview command

1. **Enhanced Features**:

- Color support (using colorama/termcolor)
- Lowercase letter support
- Unicode character support (future)
- Horizontal/vertical alignment options
- Custom spacing between letters

1. **Developer Experience**:

- Comprehensive test suite
- Type hints throughout
- Proper Python packaging
- API for programmatic use

1. **User Experience**:

- Better error messages
- Progress indicator for long text
- Config file support
- Shell completion support

## Implementation Phases

### Phase 1: Core Functionality (MVP)

- Basic character rendering
- Terminal width detection
- CLI with original banner compatibility
- Classic font support

### Phase 2: Enhanced Features

- Color support
- Additional fonts
- Configuration file
- Extended character set

### Phase 3: Advanced Features

- Plugin system
- Unicode support
- Web service API
- Font editor tool

## Technical Considerations

1. **Performance**:

- Lazy loading of fonts
- Efficient string concatenation
- Memory-conscious for large banners

1. **Compatibility**:

- Python 3.8+ support
- Cross-platform (Windows, macOS, Linux)
- No mandatory external dependencies for core

1. **Quality Assurance**:

- Unit tests for all components
- Integration tests for CLI
- Property-based testing for text processing
- Code coverage >90%

## API Example

```python
from banner import Banner, ClassicFont

# Simple usage
banner = Banner(font=ClassicFont())
print(banner.generate("HELLO"))

# Advanced usage
banner = Banner(
    font=ClassicFont(),
    spacing=3,
    max_width=120,
    color='red'
)
result = banner.generate("PYTHON")
```

## CLI Examples

```ascii
# Basic usage (compatible with original)
banner "HELLO WORLD"

# Enhanced features
banner --color red "HELLO"
banner --font modern "PYTHON"
banner --spacing 4 "WIDE"
banner --center "CENTERED"
```

## Next Steps

1. Review and refine this design
2. Create detailed technical specifications
3. Set up project structure
4. Implement Phase 1 MVP
5. Gather feedback and iterate

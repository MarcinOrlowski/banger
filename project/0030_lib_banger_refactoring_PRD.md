# banger_lib Library Refactoring PRD

**Ticket**: [#0030 - Refactor: Extract core functionality into banger_lib library](https://github.com/MarcinOrlowski/banger/issues/30)

## Problem Statement

The current `banger` package mixes CLI frontend code with core banner generation functionality. This prevents
other applications from using the banner rendering capabilities as a library. Developers who want to generate
ASCII banners programmatically must either duplicate the code or awkwardly invoke the CLI.

## Solution Overview

Extract core functionality into a separate `banger_lib` package that provides a clean, usable Python API for
banner generation. The existing `banger` CLI becomes a thin wrapper around this library. Other applications can
then import and use `banger_lib` directly without CLI overhead.

## User Stories

1. As a Python developer, I want to import a banner library and render text with one function call, so that I
   can add ASCII banners to my applications without subprocess calls
2. As a library consumer, I want to discover available fonts and their capabilities programmatically, so that I
   can build font selection UIs or validate user input
3. As an advanced user, I want to create and register custom fonts with the library, so that I can extend
   functionality without modifying library source code

## Acceptance Criteria

- [ ] `banger_lib` is installable as a standalone package
- [ ] `render("text")` produces banner output with sensible defaults
- [ ] `Banger` class provides full control over rendering options
- [ ] All 10 built-in fonts work identically to current behavior
- [ ] TTF font support works via the library API
- [ ] Font discovery API returns list of available fonts
- [ ] Custom font registration is supported
- [ ] `banger` CLI continues to work unchanged (uses banger_lib internally)
- [ ] All existing tests pass after refactoring
- [ ] Type hints are complete for public API

## Out of Scope

- New fonts or font features (use existing font system as-is)
- CLI changes or new CLI features
- Configuration file format changes
- Breaking changes to internal font data structures
- PyPI publishing strategy (separate task)
- Documentation website or extensive docs

## Success Metrics

1. Library can render banners without importing any CLI code
2. Existing test suite passes with no modifications to test logic
3. `banger` CLI produces identical output before and after refactoring

## Proposed Public API

### Simple API (convenience function)

```python
from banger_lib import render

# One-liner - returns string
output = render("Hello World")
output = render("Hello", font="fire", max_width=80)
```

### Full Control API (Banger class)

```python
from banger_lib import Banger

# Class-based when you need more control or truncation info
b = Banger("Hello World", font="matrix", max_width=80)
output = b.render()
if b.is_truncated():
    print("Warning: text was truncated")
```

### Font Discovery API

```python
from banger_lib import fonts

fonts.list_available()              # -> ['banner', 'block', 'blur', ...]
fonts.get_height("classic")         # -> 7
fonts.get_metadata("classic")       # -> FontMetadata object
fonts.supports_character("A", "classic")  # -> True
fonts.validate("classic")           # -> validation report dict
```

### TTF Font API

```python
from banger_lib import TtfFont, render

ttf = TtfFont("/path/to/font.ttf", size=48, lines=7)
output = render("Hello", font=ttf)
```

### Custom Font Registration

```python
from banger_lib import BaseFont, register_font

class MyCustomFont(BaseFont):
    _FONT_DATA = {
        "name": "custom",
        "height": 5,
        "description": "My custom font",
        "bottom_padding": 1,
        "characters": { ... }
    }

register_font("custom", MyCustomFont)
```

### Exception Handling

```python
from banger_lib import BangerError, FontNotFoundError, CharacterNotSupportedError

try:
    output = render("Hello", font="nonexistent")
except FontNotFoundError as e:
    print(f"Font not found: {e.font_name}")
```

## Package Structure

```ascii
src/
├── banger_lib/                    # Core library
│   ├── __init__.py               # Public API exports
│   ├── banger.py                 # Banger class
│   ├── exceptions.py             # Custom exceptions
│   ├── terminal.py               # Terminal utilities
│   └── fonts/                    # Font system
│       ├── __init__.py
│       ├── api.py
│       ├── factory.py
│       ├── constants.py
│       ├── ttf.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── interface.py
│       │   ├── base.py
│       │   ├── character_data.py
│       │   └── font_metadata.py
│       └── builtin/
│           ├── __init__.py
│           └── *.py
│
└── banger/                        # CLI only (thin wrapper)
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── config.py
    └── constants.py
```

## Migration Notes

- `banger_lib` is the primary package with core functionality
- `banger` becomes a CLI package that depends on `banger_lib`
- Both packages can be installed together or `banger_lib` standalone

# banger_lib Library Refactoring TRD

**Ticket**: [#0030 - Refactor: Extract core functionality into banger_lib library](https://github.com/MarcinOrlowski/banger/issues/30)
**PRD Reference**: project/0030_lib_banger_refactoring_PRD.md

## Technical Approach

Extract core banner generation code from `banger` into `banger_lib` package (monorepo). The `banger_lib` package
contains the `Banger` class, font system, and rendering logic. The `banger` package becomes a thin CLI wrapper.
Both packages defined in `pyproject.toml`.

## Package Structure

```
src/
├── banger_lib/
│   ├── __init__.py           # Public API exports
│   ├── banger.py             # Banger class
│   ├── exceptions.py         # BangerError, FontNotFoundError, etc.
│   ├── terminal.py           # Terminal utilities
│   └── fonts/
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
└── banger/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── config.py
    └── constants.py
```

## API Design

### Public API (`banger_lib/__init__.py`)

```python
from .banger import Banger, render
from . import fonts
from .fonts import TtfFont, BaseFont, register_font
from .exceptions import BangerError, FontNotFoundError, CharacterNotSupportedError
from .fonts import CharacterData, FontMetadata, FontInterface
```

### Banger Class

```python
class Banger:
    def __init__(
        self,
        text: str,
        font: Union[str, FontInterface] = "quadrant",
        max_width: Optional[int] = None,
        character_width: Optional[int] = None,
    ) -> None: ...

    def render(self) -> str: ...
    def is_truncated(self) -> bool: ...

    @property
    def font_height(self) -> int: ...
```

### Convenience Function

```python
def render(
    text: str,
    font: Union[str, FontInterface] = "quadrant",
    max_width: Optional[int] = None,
    character_width: Optional[int] = None,
) -> str: ...
```

### Usage Examples

```python
from banger_lib import render, Banger

# Simple one-liner
output = render("Hello World")

# With options
output = render("Hello", font="fire", max_width=80)

# Class-based when you need truncation info
b = Banger("Hello World", font="matrix")
output = b.render()
if b.is_truncated():
    print("Warning: text was truncated")
```

### Exceptions

```python
class BangerError(Exception): ...
class FontNotFoundError(BangerError): ...
class CharacterNotSupportedError(BangerError): ...
```

## Technical Risks & Mitigations

1. **Circular imports** → banger_lib has zero imports from banger
2. **Test breakage** → Update imports incrementally, test after each change
3. **PyPI naming** → Verify "banger-lib" availability before publishing

## Implementation Plan

1. Create `src/banger_lib/` structure
2. Move fonts/, terminal.py, core logic to banger_lib
3. Create exceptions.py, update __init__.py
4. Add `render()` convenience function
5. Update banger/cli.py imports to use banger_lib
6. Update pyproject.toml
7. Update tests, run full suite

## Rollback

Git revert if critical issues. Validate CLI output before/after.

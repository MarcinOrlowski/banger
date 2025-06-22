# Python Banner Tool - Design Document v3

## Executive Summary

A properly structured Python package that reimplements the classic Unix `banner` command, designed
for PyPI distribution and installation via pip/pipx.

## Package Structure

```ascii
banger/
├── src/
│   └── banger/
│       ├── __init__.py
│       ├── __main__.py      # Entry point for `python -m banner_ng`
│       ├── cli.py           # CLI logic and argument parsing
│       ├── core.py          # Banner generation logic
│       ├── fonts.py         # Character definitions
│       └── terminal.py      # Terminal utilities
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_cli.py
│   ├── test_fonts.py
│   └── test_terminal.py
├── .gitignore
├── .python-version          # Python 3.8
├── CHANGELOG.md
├── LICENSE                  # MIT to match original
├── README.md
├── pyproject.toml          # Modern Python packaging
└── tox.ini                 # Testing across Python versions
```

## Modern Python Packaging Setup

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "banger"
version = "1.0.0"
description = "Classic Unix banner command reimplemented in Python"
readme = "README.md"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Text Processing",
    "Topic :: Utilities",
]
keywords = ["banner", "ascii", "text", "console"]
requires-python = ">=3.8"
dependencies = []  # No runtime dependencies!

[project.urls]
Homepage = "https://github.com/yourusername/banger"
Repository = "https://github.com/yourusername/banger"
Issues = "https://github.com/yourusername/banger/issues"

[project.scripts]
banger = "banner_ng.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
    "tox>=4.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
banner_ng = ["py.typed"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.ruff]
target-version = "py38"
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
addopts = "-ra -q --cov=banner_ng --cov-report=term-missing"
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
```

### Package Implementation Structure

#### src/banner_ng/__init__.py

```python
"""Classic Unix banner command reimplemented in Python."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import BannerGenerator
from .fonts import CHARACTERS, CHAR_HEIGHT, CHAR_SPACING

__all__ = ["BannerGenerator", "CHARACTERS", "CHAR_HEIGHT", "CHAR_SPACING"]
```

#### src/banner_ng/cli.py

```python
"""Command-line interface for banner."""

import sys
from typing import List, Optional

from .core import BannerGenerator
from .terminal import get_terminal_width

__version__ = "1.0.0"


def print_usage() -> None:
    """Print usage information."""
    print(f"""\
Usage: banger string

This is a classic-style banner program similar to the one found in Solaris or
AIX in the late 1990s. It prints a short string to the console in very large
letters.

Version: {__version__}
""")


def parse_args(args: List[str]) -> Optional[List[str]]:
    """Parse command-line arguments."""
    if not args:
        print_usage()
        return None

    if args[0] in ("-h", "--help"):
        print_usage()
        sys.exit(0)

    # Handle -- separator
    if args[0] == "--" and len(args) > 1:
        return args[1:]

    return args


def main() -> int:
    """Main entry point."""
    args = parse_args(sys.argv[1:])
    if args is None:
        return 1

    width = get_terminal_width()

    for word in args:
        generator = BannerGenerator(max_width=width)
        processed_word = word.upper()

        # Convert all whitespace to spaces
        for char in ['\t', '\n', '\r', '\v', '\f']:
            processed_word = processed_word.replace(char, ' ')

        generator.add_text(processed_word)
        print(generator.render())

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

#### src/banner_ng/__main__.py

```python
"""Allow banger to be run as python -m banner_ng."""

from .cli import main

if __name__ == "__main__":
    main()
```

### Installation and Usage

#### For end users (via pipx - recommended for CLI tools)

```ascii
pipx install banger
banger "HELLO WORLD"
```

#### For developers (via pip)

```ascii
pip install banger
python -m banner_ng "HELLO WORLD"
```

#### For development

```ascii
git clone https://github.com/yourusername/baner
cd banger
pip install -e ".[dev]"
```

### Testing Strategy

#### tox.ini

```ini
[tox]
envlist = py38,py39,py310,py311,py312,lint,type
isolated_build = True

[testenv]
deps = pytest>=7.0
       pytest-cov>=4.0
commands = pytest {posargs}

[testenv:lint]
deps = ruff>=0.1.0
       black>=23.0
commands = 
    black --check src tests
    ruff check src tests

[testenv:type]
deps = mypy>=1.0
commands = mypy src
```

### GitHub Actions Workflow

#### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main, dev ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ ubuntu-latest, macos-latest, windows-latest ]
        python-version: [ '3.8', '3.9', '3.10', '3.11', '3.12' ]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install tox tox-gh-actions
      - name: Test with tox
        run: tox
```

### Publishing to PyPI

#### Build and upload process

```ascii
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ banger

# Upload to real PyPI
twine upload dist/*
```

### Key Design Decisions

1. **Source Layout**: Using `src/` layout prevents accidental imports during testing
2. **Modern Packaging**: pyproject.toml instead of setup.py for future-proofing
3. **No Dependencies**: Pure Python implementation for maximum compatibility
4. **Type Hints**: Full type annotations for better IDE support and documentation
5. **Testing**: Comprehensive test suite with tox for multiple Python versions
6. **pipx Friendly**: Designed as a CLI tool, perfect for pipx installation

### Benefits of This Structure

1. **Professional**: Follows Python packaging best practices
2. **Maintainable**: Clear separation of concerns
3. **Testable**: Easy to test individual components
4. **Distributable**: Ready for PyPI upload
5. **Cross-platform**: Works on Windows, macOS, and Linux
6. **Future-proof**: Uses modern Python packaging standards

This structure ensures the package is properly organized from the start and ready for
distribution on PyPI, making it easy for users to install with either pip or pipx.

# Python Banner Implementation Plan

## Overview

This document outlines the step-by-step implementation plan for creating a Python-based replacement
for the Unix `banner` command, structured as a proper Python package ready for PyPI distribution.

## Implementation Phases

### Phase 1: Project Setup and Structure (30 minutes)

1. **Initialize Git repository**

   ```ascii
   git init
   git branch -M main
   ```

1. **Create directory structure**

   ```ascii
   mkdir -p src/banner_ng tests .github/workflows
   touch src/banner_ng/{__init__.py,__main__.py,cli.py,core.py,fonts.py,terminal.py}
   touch tests/{__init__.py,test_core.py,test_cli.py,test_fonts.py,test_terminal.py}
   ```

1. **Create essential files**

- `.gitignore` (Python template)
- `LICENSE` (GPL-2.0 to match original)
- `README.md`
- `CHANGELOG.md`
- `pyproject.toml`
- `.python-version` (3.8)

1. **Set up virtual environment**

   ```ascii
   python3.8 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

### Phase 2: Core Implementation (2-3 hours)

1. **Implement fonts.py**

- Extract character definitions from `banner-main/letters.h`
- Convert to Python dictionary format
- Verify all characters are included

1. **Implement terminal.py**

- Terminal width detection logic
- COLUMNS environment variable support
- Fallback to 80 columns

1. **Implement core.py**

- `BannerGenerator` class
- Character addition logic
- Width truncation handling
- Banner rendering

1. **Implement cli.py**

- Argument parsing
- Help text
- Main entry point
- Error handling

1. **Wire up init.py and main.py**

- Package exports
- Version information
- Entry point configuration

### Phase 3: Testing (1-2 hours)

1. **Unit tests**

- Test each character renders correctly
- Test width truncation
- Test terminal width detection
- Test argument parsing

1. **Integration tests**

- Test full banner generation
- Test CLI interface
- Test edge cases

1. **Compatibility tests**

- Compare output with original C banner
- Test all supported characters
- Verify exact output match

### Phase 4: Development Tools Setup (30 minutes)

1. **Configure linting and formatting**

- Black configuration
- Ruff configuration
- MyPy configuration

1. **Set up tox**

- Test multiple Python versions
- Linting environment
- Type checking environment

1. **GitHub Actions**

- CI workflow
- Test matrix (OS × Python version)
- Linting and type checking

### Phase 5: Documentation (30 minutes)

1. **README.md**

- Installation instructions (pip and pipx)
- Usage examples
- Comparison with original banner
- Development setup

1. **CHANGELOG.md**

- Initial 1.0.0 release notes

1. **Code documentation**

- Docstrings for all public functions
- Type hints throughout

### Phase 6: Package and Publish (30 minutes)

1. **Build package**

   ```ascii
   python -m build
   ```

1. **Test package**

   ```ascii
   # Create test environment
   python -m venv test-env
   source test-env/bin/activate
   pip install dist/*.whl
   banger "TEST"
   ```

1. **Publish to Test PyPI**

   ```ascii
   twine upload --repository testpypi dist/*
   ```

1. **Final testing**

   ```ascii
   pipx install --index-url https://test.pypi.org/simple/ banner-ng
   ```

1. **Publish to PyPI**

   ```ascii
   twine upload dist/*
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 (enforced by Black)
- Use type hints for all functions
- Write docstrings for public APIs
- Keep functions small and focused

### Testing Strategy

- Aim for >90% code coverage
- Test edge cases explicitly
- Use parametrized tests for character rendering
- Mock terminal operations for consistent testing

### Performance Targets

- Import time: <100ms
- Render time: <50ms for 10 characters
- Memory usage: <10MB for typical usage

## Validation Checklist

Before declaring the implementation complete:

- [ ] All characters from original banner are supported
- [ ] Output matches original banner exactly
- [ ] Terminal width detection works correctly
- [ ] COLUMNS environment variable is respected
- [ ] Multiple arguments create separate banners
- [ ] `--` separator works correctly
- [ ] Help text is displayed appropriately
- [ ] Package installs cleanly via pip
- [ ] Package installs cleanly via pipx
- [ ] Tests pass on Python 3.8-3.12
- [ ] Tests pass on Linux, macOS, and Windows
- [ ] No runtime dependencies required
- [ ] Documentation is complete
- [ ] Package is uploaded to PyPI

## Risk Mitigation

1. **Character accuracy**: Use automated testing to compare against C implementation
2. **Cross-platform compatibility**: Use GitHub Actions to test on multiple OS
3. **Package naming**: Using `banger` to avoid conflicts with existing packages
4. **Terminal detection failures**: Robust fallback mechanisms

## Success Metrics

1. **Functionality**: 100% compatibility with original banner
2. **Quality**: >90% test coverage, all linters pass
3. **Performance**: <50ms render time for typical usage
4. **Usability**: Installable via `pipx install banger` in one command

## Next Steps

1. Review and approve this implementation plan
2. Begin Phase 1: Project Setup
3. Proceed through phases sequentially
4. Validate against checklist before release

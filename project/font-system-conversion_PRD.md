# Font System Conversion PRD

**Ticket**: TBD (Planning Phase)

## Problem Statement

The current font system relies on JSON files with runtime loading and validation, creating unnecessary
complexity with FontLoader and FontValidator classes. Developers must maintain separate JSON files and
validation logic, increasing maintenance overhead and potential runtime errors. This architecture adds
500+ lines of infrastructure code for functionality that could be compile-time validated.

## Solution Overview

Convert all JSON-based fonts to direct Python classes that extend the existing BaseBannerFont foundation.
Each font becomes a self-contained class with embedded character data, eliminating JSON files, loader, and
validator infrastructure. This maintains full API compatibility while simplifying the codebase and
improving performance through direct class instantiation rather than runtime JSON parsing.

## User Stories

1. As a maintainer, I want fonts defined as Python classes, so that I can modify font data with IDE support and compile-time validation
2. As a developer, I want the font API to remain unchanged, so that existing code continues working without modifications  
3. As a user, I want font loading to be faster, so that banner generation has improved performance

## Acceptance Criteria

- [ ] All 8 JSON fonts converted to Python classes extending BaseBannerFont
- [ ] FontLoader and FontValidator classes completely removed
- [ ] All JSON font files deleted from the repository
- [ ] Font registry updated to instantiate classes directly instead of JSON loaders
- [ ] All existing API functions maintain identical behavior and signatures
- [ ] All tests pass without modification
- [ ] Performance improves (measured via font instantiation benchmarks)

## Out of Scope

- Changes to font rendering logic or character data format
- Modifications to dynamic font system (SimpleDotMatrixFont, TtfFont)
- Updates to the FontInterface or BaseBannerFont base classes
- Addition of new fonts or character sets
- Changes to the public font API or function signatures

## Success Metrics

1. Codebase reduced by 500+ lines through infrastructure removal
2. Font instantiation performance improves by 20% (measured via benchmarks)
3. Zero API breaking changes - all existing tests pass unchanged

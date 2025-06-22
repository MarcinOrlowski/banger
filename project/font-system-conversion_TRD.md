# Font System Conversion TRD

**Ticket**: TBD (Planning Phase)
**PRD Reference**: font-system-conversion_PRD.md

## Technical Approach

We'll generate Python font classes by parsing existing JSON font files and creating classes that extend `BaseBannerFont`. Each font class will embed its character data as a class attribute dictionary, implementing `_load_font_data()` to return this embedded data. The existing font registry in `fonts.py` will be updated to instantiate these classes directly instead of using JSON loaders. This maintains the current FontInterface while eliminating JSON parsing and validation infrastructure.

## Data Model

No database changes required. Font data structure remains identical:

```python
# Each font class will contain embedded data like:
class BannerFont(BaseBannerFont):
    _FONT_DATA = {
        'name': 'banner',
        'height': 7,
        'description': 'Classic banner style font',
        'characters': {
            'A': {'lines': ['...', '...'], 'trim': True},
            # ... 95 characters total
        }
    }
    
    def _load_font_data(self) -> Dict[str, Any]:
        return self._FONT_DATA
```

## API Design

No API changes required. All existing functions maintain identical signatures:

```python
# These functions remain unchanged:
get_font(name: str) -> FontInterface
get_cached_font(name: str) -> FontInterface  
get_character_data(char: str, font: str, style: str) -> CharacterData
get_available_fonts() -> List[str]
validate_font_character_coverage(text: str, font_name: str) -> ValidationResult

# Internal changes only:
BUILTIN_FONTS = {
    'banner': lambda: BannerFont(),      # was: lambda: _load_json_font('banner')
    'default': lambda: DefaultFont(),    # was: lambda: _load_json_font('default')
    # ... all 8 fonts
}
```

## Security & Performance

- **Performance**: Font instantiation improves ~20% by eliminating JSON parsing overhead
- **Validation**: Compile-time validation replaces runtime JSON schema validation  
- **Memory**: Identical memory footprint - data still cached in _font_cache
- **Import time**: Slightly faster due to removing JSON file I/O during imports

## Technical Risks & Mitigations

1. **Risk**: Large embedded data increases module size → **Mitigation**: Keep fonts in separate modules, import on demand
2. **Risk**: Breaking API compatibility during conversion → **Mitigation**: Maintain identical FontInterface, run full test suite 
3. **Risk**: Character data corruption during JSON conversion → **Mitigation**: Automated validation comparing old vs new output

## Implementation Plan

- **Phase 1** (S): Create font class generator script - 1 day
- **Phase 2** (M): Generate all 8 font classes in separate modules - 2 days  
- **Phase 3** (S): Update font registry and remove JSON infrastructure - 1 day
- **Phase 4** (S): Remove JSON files, loader.py, validator.py - 1 day
- **Phase 5** (S): Fix import errors and run test validation - 1 day

Dependencies: None

## Monitoring & Rollback

- **Feature flag**: Not required - internal refactoring only
- **Key metrics**: Test suite pass rate, font instantiation benchmarks
- **Rollback**: Git revert maintains all JSON files and infrastructure until conversion is validated
- **Validation**: Compare character output between old/new implementations for all 95 characters across 8 fonts
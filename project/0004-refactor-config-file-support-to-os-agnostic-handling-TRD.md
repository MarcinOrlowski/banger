# Cross-Platform Configuration File Support TRD

**Ticket**: [#0004: Refactor config file support to OS agnostic handling](https://github.com/MarcinOrlowski/banger/issues/4)
**PRD Reference**: 0004-refactor-config-file-support-to-os-agnostic-handling-PRD.md

## Technical Approach

Replace hardcoded Unix-style configuration paths with `platformdirs` library to automatically determine OS-appropriate configuration directories. Implement a new `ConfigManager` class that encapsulates all configuration operations and handles migration from legacy locations. The existing `Config` class will be refactored to use the new manager internally, maintaining full backward compatibility with the current API.

## Data Model

No database changes required. File system changes only:

```
Current Structure:
~/.config/banger/banger.yml (Linux/Unix only)

New Structure:
Linux:   ~/.config/banger/banger.yml
macOS:   ~/Library/Application Support/banger/banger.yml
Windows: %APPDATA%/banger/banger/banger.yml
```

Migration logic: Check for old config at `~/.config/banger/banger.yml` and copy to new location if new location doesn't exist.

## API Design

Internal API changes only (no external API impact):

```python
# New ConfigManager class
class ConfigManager:
    def __init__(self, app_name="banger", app_author="MarcinOrlowski")
    def get_config_dir(self) -> Path
    def get_config_file_path(self) -> Path
    def ensure_config_dir(self) -> None
    def migrate_legacy_config(self) -> bool

# Modified Config class (maintains existing interface)
class Config:
    def __init__(self)  # Now uses ConfigManager internally
    def get_font(self) -> Optional[str]  # No change
    def get_banner_width(self) -> Optional[int]  # No change
    def get_width(self) -> Optional[int]  # No change
    def get_config_file_path(self) -> Path  # Updated implementation
```

## Security & Performance

- **File permissions**: Use default OS permissions (no special handling needed)
- **Migration safety**: Atomic copy operation using `shutil.copy2()` to preserve metadata
- **Performance**: One-time migration check on first run, minimal overhead
- **Error handling**: Graceful degradation - config failures don't crash the application

## Technical Risks & Mitigations

1. **Risk**: Legacy config migration fails silently → **Mitigation**: Return boolean from migration function and log results
2. **Risk**: `platformdirs` not available on older systems → **Mitigation**: Add minimum version requirement in pyproject.toml
3. **Risk**: Permission errors in new config directories → **Mitigation**: Use existing error handling pattern (silent fallback to defaults)

## Implementation Plan

- **Phase 1** (S): Add platformdirs dependency and ConfigManager class - 1 day
- **Phase 2** (M): Refactor Config class to use ConfigManager - 2 days
- **Phase 3** (S): Update CLI help text and documentation - 1 day
- **Phase 4** (S): Add migration logic and testing - 1 day

Dependencies: None

## Monitoring & Rollback

- **Feature flag**: Not applicable (internal refactor)
- **Key metrics**: Configuration file access success rate, migration completion rate
- **Rollback**: Revert to previous Config class implementation if critical issues arise
- **Testing**: Verify existing tests pass, add new tests for ConfigManager functionality

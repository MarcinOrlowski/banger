# Implementation Plan for Cross-Platform Configuration File Support

## Phase 1: Dependencies & Core Infrastructure (1 day)

- Add `platformdirs>=3.0.0` to pyproject.toml dependencies
- Create new `ConfigManager` class in config.py with OS-agnostic path handling
- Implement basic directory creation and path resolution methods

## Phase 2: Configuration Refactor (2 days)

- Refactor existing `Config` class to use `ConfigManager` internally
- Implement legacy config migration logic from `~/.config/banger/` to new OS-specific locations
- Ensure all existing configuration methods continue to work unchanged
- Update `create_config_template()` function to use new paths

## Phase 3: CLI and Documentation Updates (1 day)

- Update help text in cli.py to remove hardcoded path references
- Update template content to reflect cross-platform nature
- Test configuration initialization across different scenarios

## Phase 4: Testing & Validation (1 day)

- Add unit tests for ConfigManager functionality
- Test migration logic with mock legacy configurations
- Verify existing tests still pass with new implementation
- Manual testing of config file operations

## Implementation Details

- Use `platformdirs.user_config_dir("banger", "MarcinOrlowski")` for consistent naming
- Migration checks on first Config class instantiation
- Atomic file operations for safe migration
- Maintain existing YAML format and all current functionality
- No breaking changes to public API

## Platform-Specific Configuration Locations

The new implementation will store configuration files in OS-appropriate directories:

- **Linux**: `~/.config/banger/banger.yml`
  - Example: `/home/username/.config/banger/banger.yml`
- **macOS**: `~/Library/Application Support/banger/banger.yml`
  - Example: `/Users/username/Library/Application Support/banger/banger.yml`
- **Windows**: `%APPDATA%\banger\banger\banger.yml`
  - Example: `C:\Users\username\AppData\Roaming\banger\banger\banger.yml`

**Total Estimated Time:** 5 days

**Risk Level:** Low - Internal refactor with backward compatibility maintained

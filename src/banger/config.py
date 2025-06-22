"""
##################################################################################
#
# Bänger by Marcin Orlowski
# Because your `banner` deserves to be a `bänger`!
#
# @author    Marcin Orlowski <mail@marcinOrlowski.com>
# Copyright  ©2025 Marcin Orlowski <MarcinOrlowski.com>
# @link      https://github.com/MarcinOrlowski/banger
#
##################################################################################

Configuration management for banger.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

import yaml


class Config:
    """Configuration loader and manager for banger."""

    def __init__(self):
        self.config_data: Dict[str, Any] = {}
        self._load_config()

    def _get_config_path(self) -> Optional[Path]:
        """Get the path to the configuration file."""
        config_dir = Path.home() / ".config" / "banger"
        config_file = config_dir / "banger.yml"

        if config_file.exists():
            return config_file
        return None

    def get_config_file_path(self) -> Path:
        """Get the full path to the configuration file (whether it exists or not)."""
        config_dir = Path.home() / ".config" / "banger"
        return config_dir / "banger.yml"

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        config_path = self._get_config_path()
        if config_path is None:
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config_data = yaml.safe_load(f) or {}
        except (yaml.YAMLError, OSError):
            # Silently ignore config file errors - use defaults
            self.config_data = {}

    def get_font(self) -> Optional[str]:
        """Get the default font from configuration."""
        return self.config_data.get("font")

    def get_banner_width(self) -> Optional[int]:
        """Get the default banner width from configuration."""
        return self.config_data.get("banner_width")

    def get_width(self) -> Optional[int]:
        """Get the default character width from configuration."""
        return self.config_data.get("width")


# Global configuration instance
_config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return _config


def create_config_template(force: bool = False) -> bool:
    """Create a template configuration file.

    Args:
        force: If True, overwrite existing config file

    Returns:
        True if config file was created, False if it already exists

    Raises:
        SystemExit: If config file exists and force is False
    """
    config = get_config()
    config_path = config.get_config_file_path()

    # Check if config file already exists
    if config_path.exists() and not force:
        print(
            f"Error: Configuration file already exists at {config_path}",
            file=sys.stderr,
        )
        print(
            "Use --force to overwrite the existing configuration file.", file=sys.stderr
        )
        sys.exit(1)

    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Template content with all options commented out
    template_content = """# Configuration file for banger
# Place this file at ~/.config/banger/banger.yml

# Default font to use
# Available fonts: default, matrix, banner, block, blur, compact, fire, quadrant, small
# font: quadrant

# Default banner width in characters (auto-detects terminal width if not specified)
# banner_width: 80

# Default character width for proportional spacing
# width: 10
"""

    # Write template to file
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        print(f"Configuration template created at: {config_path}")
        print("Edit this file to customize your default settings.")
        return True

    except OSError as e:
        print(f"Error: Could not create configuration file: {e}", file=sys.stderr)
        sys.exit(1)

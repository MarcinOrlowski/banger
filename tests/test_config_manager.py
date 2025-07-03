"""
Tests for ConfigManager class.
"""

import tempfile
from pathlib import Path
from unittest import mock

from banger.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_init_with_defaults(self):
        """Test ConfigManager initialization with default values."""
        manager = ConfigManager()
        assert manager.app_name == "banger"
        assert manager.app_author == "MarcinOrlowski"
        assert manager._config_dir is None
        assert manager._config_file is None

    def test_init_with_custom_values(self):
        """Test ConfigManager initialization with custom values."""
        manager = ConfigManager(app_name="test_app", app_author="test_author")
        assert manager.app_name == "test_app"
        assert manager.app_author == "test_author"

    @mock.patch("banger.config.user_config_dir")
    def test_get_config_dir(self, mock_user_config_dir):
        """Test get_config_dir method."""
        mock_user_config_dir.return_value = "/fake/config/dir"

        manager = ConfigManager()
        config_dir = manager.get_config_dir()

        assert config_dir == Path("/fake/config/dir")
        mock_user_config_dir.assert_called_once_with("banger", "MarcinOrlowski")

    @mock.patch("banger.config.user_config_dir")
    def test_get_config_dir_caching(self, mock_user_config_dir):
        """Test that get_config_dir caches the result."""
        mock_user_config_dir.return_value = "/fake/config/dir"

        manager = ConfigManager()
        config_dir1 = manager.get_config_dir()
        config_dir2 = manager.get_config_dir()

        assert config_dir1 == config_dir2
        mock_user_config_dir.assert_called_once()

    @mock.patch("banger.config.user_config_dir")
    def test_get_config_file_path(self, mock_user_config_dir):
        """Test get_config_file_path method."""
        mock_user_config_dir.return_value = "/fake/config/dir"

        manager = ConfigManager()
        config_file = manager.get_config_file_path()

        assert config_file == Path("/fake/config/dir/banger.yml")

    @mock.patch("banger.config.user_config_dir")
    def test_get_config_file_path_caching(self, mock_user_config_dir):
        """Test that get_config_file_path caches the result."""
        mock_user_config_dir.return_value = "/fake/config/dir"

        manager = ConfigManager()
        config_file1 = manager.get_config_file_path()
        config_file2 = manager.get_config_file_path()

        assert config_file1 == config_file2
        mock_user_config_dir.assert_called_once()

    def test_ensure_config_dir(self):
        """Test ensure_config_dir method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_config_dir = Path(temp_dir) / "test_config"

            with mock.patch.object(
                ConfigManager, "get_config_dir", return_value=test_config_dir
            ):
                manager = ConfigManager()
                manager.ensure_config_dir()

                assert test_config_dir.exists()
                assert test_config_dir.is_dir()

    def test_ensure_config_dir_existing(self):
        """Test ensure_config_dir method with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_config_dir = Path(temp_dir) / "existing_config"
            test_config_dir.mkdir()

            with mock.patch.object(
                ConfigManager, "get_config_dir", return_value=test_config_dir
            ):
                manager = ConfigManager()
                manager.ensure_config_dir()  # Should not raise exception

                assert test_config_dir.exists()
                assert test_config_dir.is_dir()

    def test_migrate_legacy_config_success(self):
        """Test successful migration from legacy config location."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create legacy config
            legacy_dir = Path(temp_dir) / ".config" / "banger"
            legacy_dir.mkdir(parents=True)
            legacy_config = legacy_dir / "banger.yml"
            legacy_config.write_text("font: classic\n")

            # Setup new config location
            new_dir = Path(temp_dir) / "new_config"
            new_config = new_dir / "banger.yml"

            with mock.patch.object(Path, "home", return_value=Path(temp_dir)):
                with mock.patch.object(
                    ConfigManager, "get_config_file_path", return_value=new_config
                ):

                    def mock_ensure_dir():
                        new_dir.mkdir(parents=True, exist_ok=True)

                    with mock.patch.object(
                        ConfigManager, "ensure_config_dir", side_effect=mock_ensure_dir
                    ):
                        manager = ConfigManager()
                        result = manager.migrate_legacy_config()

                        assert result is True
                        assert new_config.exists()
                        assert new_config.read_text() == "font: classic\n"

    def test_migrate_legacy_config_no_legacy(self):
        """Test migration when no legacy config exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_config = Path(temp_dir) / "banger.yml"

            with mock.patch.object(Path, "home", return_value=Path(temp_dir)):
                with mock.patch.object(
                    ConfigManager, "get_config_file_path", return_value=new_config
                ):
                    manager = ConfigManager()
                    result = manager.migrate_legacy_config()

                    assert result is False
                    assert not new_config.exists()

    def test_migrate_legacy_config_new_exists(self):
        """Test migration when new config already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create legacy config
            legacy_dir = Path(temp_dir) / ".config" / "banger"
            legacy_dir.mkdir(parents=True)
            legacy_config = legacy_dir / "banger.yml"
            legacy_config.write_text("font: classic\n")

            # Create existing new config
            new_dir = Path(temp_dir) / "new_config"
            new_dir.mkdir(parents=True)
            new_config = new_dir / "banger.yml"
            new_config.write_text("font: matrix\n")

            with mock.patch.object(Path, "home", return_value=Path(temp_dir)):
                with mock.patch.object(
                    ConfigManager, "get_config_file_path", return_value=new_config
                ):
                    manager = ConfigManager()
                    result = manager.migrate_legacy_config()

                    assert result is False
                    assert new_config.read_text() == "font: matrix\n"  # Unchanged

    def test_migrate_legacy_config_permission_error(self):
        """Test migration with permission error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create legacy config
            legacy_dir = Path(temp_dir) / ".config" / "banger"
            legacy_dir.mkdir(parents=True)
            legacy_config = legacy_dir / "banger.yml"
            legacy_config.write_text("font: classic\n")

            # Setup new config location
            new_config = Path(temp_dir) / "new_config" / "banger.yml"

            with mock.patch.object(Path, "home", return_value=Path(temp_dir)):
                with mock.patch.object(
                    ConfigManager, "get_config_file_path", return_value=new_config
                ):
                    with mock.patch.object(ConfigManager, "ensure_config_dir"):
                        with mock.patch(
                            "banger.config.shutil.copy2",
                            side_effect=OSError("Permission denied"),
                        ):
                            manager = ConfigManager()
                            result = manager.migrate_legacy_config()

                            assert (
                                result is False
                            )  # Should not crash, just return False

"""
Tests for configuration system.

Tests the configuration loading, validation, and environment-specific settings.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.config import Settings, MCPServerConfig
from src.env_config import get_env_config, DevelopmentConfig, TestingConfig, ProductionConfig
from src.config_validator import ConfigurationError


class TestMCPServerConfig:
    """Tests for MCP server configuration."""

    def test_mcp_server_config_defaults(self):
        """Test MCP server config with default values."""
        config = MCPServerConfig(name="test-server")
        assert config.name == "test-server"
        assert config.transport == "stdio"
        assert config.enabled is True
        assert config.args == []
        assert config.env == {}

    def test_mcp_server_config_stdio(self):
        """Test MCP server config for stdio transport."""
        config = MCPServerConfig(
            name="test-server",
            transport="stdio",
            command="python",
            args=["-m", "mcp_server"],
        )
        assert config.transport == "stdio"
        assert config.command == "python"
        assert config.args == ["-m", "mcp_server"]

    def test_mcp_server_config_http(self):
        """Test MCP server config for HTTP transport."""
        config = MCPServerConfig(
            name="test-server", transport="http", url="http://localhost:8000"
        )
        assert config.transport == "http"
        assert config.url == "http://localhost:8000"


class TestSettings:
    """Tests for application settings."""

    def test_settings_defaults(self):
        """Test default settings values."""
        settings = Settings()
        assert settings.ENV == "development"
        assert settings.AGENT_NAME == "AntigravityAgent"
        assert settings.GEMINI_MODEL_NAME == "gemini-2.5-flash"
        assert settings.OPENAI_MODEL == "gpt-4o-mini"
        assert settings.MCP_ENABLED is False

    def test_settings_from_env_vars(self):
        """Test loading settings from environment variables."""
        with patch.dict(
            os.environ,
            {
                "ENV": "production",
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "AGENT_NAME": "TestAgent",
                "DEBUG_MODE": "true",
            },
        ):
            settings = Settings()
            assert settings.ENV == "production"
            assert settings.GOOGLE_API_KEY == "AIzaSyTest1234567890123456789012345678"
            assert settings.AGENT_NAME == "TestAgent"
            assert settings.DEBUG_MODE is True

    def test_settings_env_config_application(self):
        """Test that environment-specific configs are applied."""
        with patch.dict(os.environ, {"ENV": "development"}):
            settings = Settings()
            # Development should have DEBUG_MODE = True
            assert settings.DEBUG_MODE is True

    def test_settings_invalid_env(self):
        """Test handling of invalid environment name."""
        with patch.dict(os.environ, {"ENV": "invalid_env"}):
            # Should warn but not crash
            with pytest.warns(UserWarning):
                settings = Settings()
                assert settings.ENV == "invalid_env"


class TestEnvironmentConfigs:
    """Tests for environment-specific configurations."""

    def test_get_development_config(self):
        """Test getting development configuration."""
        config = get_env_config("development")
        assert config == DevelopmentConfig
        assert config.LOG_LEVEL == "DEBUG"
        assert config.DEBUG_MODE is True
        assert config.STRICT_MODE is False

    def test_get_testing_config(self):
        """Test getting testing configuration."""
        config = get_env_config("testing")
        assert config == TestingConfig
        assert config.LOG_LEVEL == "WARNING"
        assert config.DEBUG_MODE is False
        assert config.STRICT_MODE is True
        assert config.MCP_ENABLED is False

    def test_get_production_config(self):
        """Test getting production configuration."""
        config = get_env_config("production")
        assert config == ProductionConfig
        assert config.LOG_LEVEL == "INFO"
        assert config.DEBUG_MODE is False
        assert config.STRICT_MODE is True
        assert config.MCP_ENABLED is True

    def test_get_env_config_case_insensitive(self):
        """Test environment config is case insensitive."""
        assert get_env_config("DEVELOPMENT") == DevelopmentConfig
        assert get_env_config("Development") == DevelopmentConfig
        assert get_env_config("development") == DevelopmentConfig

    def test_get_env_config_invalid(self):
        """Test invalid environment name raises error."""
        with pytest.raises(ValueError, match="Unknown environment"):
            get_env_config("invalid")


class TestConfigurationValidation:
    """Tests for configuration validation."""

    def test_validate_valid_google_config(self):
        """Test validation with valid Google configuration."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "GEMINI_MODEL_NAME": "gemini-2.5-flash",
            },
        ):
            settings = Settings()
            # Should not raise
            settings.validate_configuration()

    def test_validate_invalid_google_api_key(self):
        """Test validation rejects invalid Google API key."""
        with patch.dict(
            os.environ, {"GOOGLE_API_KEY": "invalid_key", "GEMINI_MODEL_NAME": "gemini-2.5-flash"}
        ):
            settings = Settings()
            with pytest.raises(ConfigurationError, match="Invalid Google API key"):
                settings.validate_configuration()

    def test_validate_placeholder_api_key(self):
        """Test validation rejects placeholder API keys."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "your_api_key_here",
                "GEMINI_MODEL_NAME": "gemini-2.5-flash",
            },
        ):
            settings = Settings()
            with pytest.raises(ConfigurationError, match="placeholder"):
                settings.validate_configuration()

    def test_validate_invalid_model_name(self):
        """Test validation rejects invalid model names."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "GEMINI_MODEL_NAME": "invalid-model",
            },
        ):
            settings = Settings()
            with pytest.raises(ConfigurationError, match="Invalid.*model name"):
                settings.validate_configuration()

    def test_validate_creates_directories(self):
        """Test validation creates required directories."""
        import tempfile
        import shutil

        temp_dir = tempfile.mkdtemp()
        try:
            memory_file = os.path.join(temp_dir, "data", "memory.json")
            workspace_dir = os.path.join(temp_dir, "workspace")

            with patch.dict(
                os.environ,
                {
                    "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                    "MEMORY_FILE": memory_file,
                    "WORKSPACE_DIR": workspace_dir,
                },
            ):
                settings = Settings()
                settings.validate_configuration()

                # Check directories were created
                assert Path(memory_file).parent.exists()
                assert Path(workspace_dir).exists()
        finally:
            shutil.rmtree(temp_dir)

    def test_validate_openai_config(self):
        """Test validation of OpenAI configuration."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "OPENAI_API_KEY": "sk-test1234567890123456789012345678901234567",
                "OPENAI_BASE_URL": "https://api.openai.com/v1",
            },
        ):
            settings = Settings()
            # Should not raise
            settings.validate_configuration()

    def test_validate_invalid_openai_url(self):
        """Test validation rejects invalid OpenAI URL."""
        with patch.dict(
            os.environ,
            {
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "OPENAI_API_KEY": "sk-test1234567890123456789012345678901234567",
                "OPENAI_BASE_URL": "not_a_url",
            },
        ):
            settings = Settings()
            with pytest.raises(ConfigurationError, match="URL"):
                settings.validate_configuration()


class TestConfigurationIntegration:
    """Integration tests for configuration system."""

    def test_full_config_lifecycle(self):
        """Test complete configuration lifecycle."""
        with patch.dict(
            os.environ,
            {
                "ENV": "testing",
                "GOOGLE_API_KEY": "AIzaSyTest1234567890123456789012345678",
                "GEMINI_MODEL_NAME": "gemini-2.5-flash",
                "AGENT_NAME": "IntegrationTestAgent",
            },
        ):
            # Create settings
            settings = Settings()

            # Verify environment applied
            assert settings.ENV == "testing"
            assert settings.AGENT_NAME == "IntegrationTestAgent"

            # Verify validation passes
            settings.validate_configuration()

            # Verify environment config
            env_config = get_env_config(settings.ENV)
            assert env_config.LOG_LEVEL == "WARNING"

    def test_config_with_no_env_file(self):
        """Test configuration works without .env file."""
        # This should use environment variables and defaults
        settings = Settings()
        assert settings.AGENT_NAME == "AntigravityAgent"
        assert settings.ENV == "development"

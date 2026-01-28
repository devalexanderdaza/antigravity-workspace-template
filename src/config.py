import os
from pathlib import Path
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPServerConfig(BaseSettings):
    """Configuration for a single MCP server."""

    name: str = Field(description="Unique name for the MCP server")
    transport: str = Field(
        default="stdio", description="Transport type: stdio, http, sse"
    )
    command: Optional[str] = Field(
        default=None, description="Command to run for stdio transport"
    )
    args: List[str] = Field(
        default_factory=list, description="Arguments for the command"
    )
    url: Optional[str] = Field(default=None, description="URL for http/sse transport")
    env: dict = Field(
        default_factory=dict, description="Environment variables for the server"
    )
    enabled: bool = Field(default=True, description="Whether this server is enabled")

    model_config = SettingsConfigDict(extra="ignore")


class Settings(BaseSettings):
    """Application settings managed by Pydantic."""

    # Environment Configuration
    ENV: str = Field(
        default="development",
        description="Environment: development, testing, or production"
    )

    # Google GenAI Configuration
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"  # Default to latest

    # Agent Configuration
    AGENT_NAME: str = "AntigravityAgent"
    DEBUG_MODE: bool = False

    # External LLM (OpenAI-compatible) Configuration
    OPENAI_BASE_URL: str = Field(
        default="",
        description="Base URL for OpenAI-compatible API (e.g., https://api.openai.com/v1 or http://localhost:11434/v1)",
    )
    OPENAI_API_KEY: str = Field(
        default="",
        description="API key for OpenAI-compatible endpoint. Leave blank if not required.",
    )
    OPENAI_MODEL: str = Field(
        default="gpt-4o-mini",
        description="Default model name for OpenAI-compatible chat completions.",
    )

    # Memory Configuration
    # TODO: Implement a more robust memory system
    MEMORY_FILE: str = "./data/agent_memory.json"

    # MCP Configuration
    MCP_ENABLED: bool = Field(default=False, description="Enable MCP integration")
    MCP_SERVERS_CONFIG: str = Field(
        default="./data/mcp_servers.json", description="Path to MCP servers configuration file"
    )
    # TODO: Implement a more robust MCP connection timeout system
    MCP_CONNECTION_TIMEOUT: int = Field(
        default=30, description="Timeout in seconds for MCP server connections"
    )
    # TODO: Implement a more robust MCP tool prefix system
    MCP_TOOL_PREFIX: str = Field(
        default="mcp_", description="Prefix for MCP tool names to avoid conflicts"
    )

    # TODO: Implement a more robust workspace system
    WORKSPACE_DIR: str = Field(
        default="./workspace", description="Path to workspace directory"
    )

    # TODO: Implement a more robust model configuration system
    MODEL_CONFIG: dict = Field(
        default={
            "google": {
                "api_key": "",
                "model_name": "gemini-2.5-flash",
            },
            "openai": {
                "base_url": "",
                "api_key": "",
                "model_name": "gpt-4o-mini",
            },
        },
        description="Model configuration for different LLM providers",
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def __init__(self, **kwargs):
        """Initialize settings and apply environment-specific configuration."""
        super().__init__(**kwargs)
        self._apply_env_config()

    def _apply_env_config(self) -> None:
        """Apply environment-specific configuration settings."""
        from src.env_config import get_env_config
        
        try:
            env_config = get_env_config(self.ENV)
            
            # Override settings with environment-specific values if not explicitly set
            if not self.DEBUG_MODE and hasattr(env_config, 'DEBUG_MODE'):
                self.DEBUG_MODE = env_config.DEBUG_MODE
                
        except ValueError as e:
            # Log warning but continue with defaults
            import warnings
            warnings.warn(f"Environment configuration warning: {e}")

    def validate_configuration(self) -> None:
        """Validate configuration values at runtime.
        
        Raises:
            ConfigurationError: If any configuration value is invalid.
        """
        from src.config_validator import (
            validate_api_key,
            validate_url,
            validate_file_path,
            validate_model_name,
        )
        
        # Validate Google API key if set
        if self.GOOGLE_API_KEY:
            validate_api_key(self.GOOGLE_API_KEY, "Google")
            validate_model_name(self.GEMINI_MODEL_NAME, "Google")
        
        # Validate OpenAI configuration if set
        if self.OPENAI_API_KEY:
            validate_api_key(self.OPENAI_API_KEY, "OpenAI")
        
        if self.OPENAI_BASE_URL:
            validate_url(self.OPENAI_BASE_URL, "OPENAI_BASE_URL")
        
        # Validate file paths
        if self.MEMORY_FILE:
            # Create parent directory if it doesn't exist
            memory_path = Path(self.MEMORY_FILE)
            memory_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.MCP_SERVERS_CONFIG:
            # Create parent directory if it doesn't exist
            mcp_config_path = Path(self.MCP_SERVERS_CONFIG)
            mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.WORKSPACE_DIR:
            # Create workspace directory if it doesn't exist
            workspace_path = Path(self.WORKSPACE_DIR)
            workspace_path.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

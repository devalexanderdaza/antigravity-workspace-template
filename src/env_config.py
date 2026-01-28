"""
Environment-specific configuration settings.

This module provides environment-specific settings for development, testing,
and production environments. Settings are loaded based on the ENV environment
variable, with sensible defaults for each environment.

Environments:
- development: Local development with verbose logging and debug features
- testing: Unit testing with minimal external dependencies
- production: Production deployment with security and performance optimizations
"""

from typing import Dict, Any


class DevelopmentConfig:
    """Configuration for local development environment."""

    # Logging
    LOG_LEVEL = "DEBUG"
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    
    # Agent behavior
    DEBUG_MODE = True
    VERBOSE_OUTPUT = True
    
    # Performance
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 30
    
    # Memory
    MEMORY_AUTO_SAVE = True
    MEMORY_BACKUP_ENABLED = True
    
    # MCP
    MCP_ENABLED = True
    MCP_CONNECT_TIMEOUT = 10
    
    # Safety
    REQUIRE_API_KEY_VALIDATION = True
    STRICT_MODE = False


class TestingConfig:
    """Configuration for testing environment."""

    # Logging
    LOG_LEVEL = "WARNING"
    LOG_TO_FILE = False
    LOG_TO_CONSOLE = False
    
    # Agent behavior
    DEBUG_MODE = False
    VERBOSE_OUTPUT = False
    
    # Performance
    MAX_RETRIES = 1
    REQUEST_TIMEOUT = 5
    
    # Memory
    MEMORY_AUTO_SAVE = False
    MEMORY_BACKUP_ENABLED = False
    
    # MCP
    MCP_ENABLED = False
    MCP_CONNECT_TIMEOUT = 2
    
    # Safety
    REQUIRE_API_KEY_VALIDATION = False
    STRICT_MODE = True


class ProductionConfig:
    """Configuration for production environment."""

    # Logging
    LOG_LEVEL = "INFO"
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    
    # Agent behavior
    DEBUG_MODE = False
    VERBOSE_OUTPUT = False
    
    # Performance
    MAX_RETRIES = 5
    REQUEST_TIMEOUT = 60
    
    # Memory
    MEMORY_AUTO_SAVE = True
    MEMORY_BACKUP_ENABLED = True
    
    # MCP
    MCP_ENABLED = True
    MCP_CONNECT_TIMEOUT = 10
    
    # Safety
    REQUIRE_API_KEY_VALIDATION = True
    STRICT_MODE = True


# Environment configuration mapping
ENV_CONFIGS: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_env_config(env: str = "development") -> Any:
    """
    Get configuration class for the specified environment.
    
    Args:
        env: Environment name (development, testing, production)
        
    Returns:
        Configuration class for the environment
        
    Raises:
        ValueError: If environment is not recognized
    """
    env = env.lower()
    if env not in ENV_CONFIGS:
        raise ValueError(
            f"Unknown environment '{env}'. "
            f"Valid options: {', '.join(ENV_CONFIGS.keys())}"
        )
    return ENV_CONFIGS[env]

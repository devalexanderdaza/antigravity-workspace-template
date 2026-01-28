"""Configuration validation utilities for Antigravity Workspace.

This module provides validation functions for configuration values to ensure
security and correctness at runtime.
"""

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass


def validate_api_key(api_key: str, provider: str = "Google") -> None:
    """Validate API key format and presence.
    
    Args:
        api_key: The API key to validate.
        provider: The provider name for error messages.
        
    Raises:
        ConfigurationError: If the API key is invalid or missing.
    """
    if not api_key or api_key.strip() == "":
        raise ConfigurationError(
            f"{provider} API key is required but not set. "
            f"Please set it in your .env file. "
            f"See docs/security.md for instructions."
        )
    
    if api_key in ["your_google_api_key_here", "your_openai_key_here", "your_api_key_here"]:
        raise ConfigurationError(
            f"{provider} API key is still set to placeholder value. "
            f"Please replace it with your actual API key. "
            f"See docs/security.md for instructions."
        )
    
    # Basic format validation for Google API keys
    if provider.lower() == "google" and not api_key.startswith("AIza"):
        raise ConfigurationError(
            f"Invalid {provider} API key format. "
            f"Google API keys should start with 'AIza'. "
            f"Please check your API key."
        )
    
    # Basic format validation for OpenAI API keys
    if provider.lower() == "openai" and not api_key.startswith("sk-"):
        raise ConfigurationError(
            f"Invalid {provider} API key format. "
            f"OpenAI API keys should start with 'sk-'. "
            f"Please check your API key."
        )


def validate_url(url: str, field_name: str = "URL") -> None:
    """Validate URL format.
    
    Args:
        url: The URL to validate.
        field_name: The field name for error messages.
        
    Raises:
        ConfigurationError: If the URL is invalid.
    """
    if not url or url.strip() == "":
        return  # Empty URLs are allowed for optional fields
    
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ConfigurationError(
                f"Invalid {field_name}: '{url}'. "
                f"URL must include scheme (http/https) and domain."
            )
        
        if result.scheme not in ["http", "https"]:
            raise ConfigurationError(
                f"Invalid {field_name}: '{url}'. "
                f"Only http and https schemes are supported."
            )
    except Exception as e:
        raise ConfigurationError(
            f"Invalid {field_name}: '{url}'. Error: {str(e)}"
        )


def validate_file_path(path: str, must_exist: bool = False, field_name: str = "Path") -> None:
    """Validate file path.
    
    Args:
        path: The file path to validate.
        must_exist: Whether the path must exist.
        field_name: The field name for error messages.
        
    Raises:
        ConfigurationError: If the path is invalid.
    """
    if not path or path.strip() == "":
        raise ConfigurationError(
            f"{field_name} is required but not set."
        )
    
    try:
        path_obj = Path(path)
        
        # Check for path traversal attempts
        if ".." in path:
            raise ConfigurationError(
                f"Invalid {field_name}: '{path}'. "
                f"Path traversal (..) is not allowed for security reasons."
            )
        
        if must_exist and not path_obj.exists():
            raise ConfigurationError(
                f"{field_name} does not exist: '{path}'. "
                f"Please create the directory or file first."
            )
    except ConfigurationError:
        raise
    except Exception as e:
        raise ConfigurationError(
            f"Invalid {field_name}: '{path}'. Error: {str(e)}"
        )


def validate_model_name(model_name: str, provider: str = "Google") -> None:
    """Validate model name format.
    
    Args:
        model_name: The model name to validate.
        provider: The provider name for validation.
        
    Raises:
        ConfigurationError: If the model name is invalid.
    """
    if not model_name or model_name.strip() == "":
        raise ConfigurationError(
            f"{provider} model name is required but not set."
        )
    
    # Basic validation for Google models
    if provider.lower() == "google":
        if not model_name.startswith("gemini"):
            raise ConfigurationError(
                f"Invalid {provider} model name: '{model_name}'. "
                f"Google model names should start with 'gemini'."
            )
    
    # Validate no special characters that could be injection attempts
    if not re.match(r'^[a-zA-Z0-9\-_.]+$', model_name):
        raise ConfigurationError(
            f"Invalid model name: '{model_name}'. "
            f"Model names should only contain alphanumeric characters, hyphens, underscores, and dots."
        )


def sanitize_user_input(user_input: str, max_length: int = 10000) -> str:
    """Sanitize user input to prevent injection attacks.
    
    Args:
        user_input: The user input to sanitize.
        max_length: Maximum allowed length.
        
    Returns:
        Sanitized input string.
        
    Raises:
        ConfigurationError: If input is too long or contains dangerous patterns.
    """
    if not user_input:
        return ""
    
    if len(user_input) > max_length:
        raise ConfigurationError(
            f"Input too long: {len(user_input)} characters. "
            f"Maximum allowed: {max_length} characters."
        )
    
    # Remove null bytes
    sanitized = user_input.replace('\x00', '')
    
    return sanitized


def sanitize_file_path(file_path: str, base_dir: Optional[Path] = None) -> Path:
    """Sanitize file path to prevent directory traversal attacks.
    
    Args:
        file_path: The file path to sanitize.
        base_dir: Optional base directory to restrict access to.
        
    Returns:
        Sanitized Path object.
        
    Raises:
        ConfigurationError: If path is invalid or attempts traversal.
    """
    try:
        path = Path(file_path).resolve()
        
        # If base_dir is specified, ensure path is within it
        if base_dir:
            base_dir = base_dir.resolve()
            if not str(path).startswith(str(base_dir)):
                raise ConfigurationError(
                    f"Access denied: Path '{file_path}' is outside allowed directory '{base_dir}'"
                )
        
        return path
    except Exception as e:
        raise ConfigurationError(
            f"Invalid file path: '{file_path}'. Error: {str(e)}"
        )

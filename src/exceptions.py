"""
Custom exception hierarchy for Antigravity Workspace.

This module defines a comprehensive exception hierarchy that provides:
- Clear error categorization
- Rich error context and metadata
- Error recovery strategies
- Helpful error messages for debugging and user feedback

Exception Hierarchy:
    AntigravityError (base)
    ├── ConfigurationError (configuration issues)
    ├── APIError (API communication failures)
    │   ├── APIConnectionError
    │   ├── APIAuthenticationError
    │   ├── APIRateLimitError
    │   └── APITimeoutError
    ├── ToolExecutionError (tool/function execution failures)
    │   ├── ToolNotFoundError
    │   ├── ToolValidationError
    │   └── ToolTimeoutError
    ├── MCPError (MCP integration failures)
    │   ├── MCPConnectionError
    │   ├── MCPServerError
    │   └── MCPToolError
    └── MemoryError (memory/persistence failures)
        ├── MemoryIOError
        └── MemoryCorruptionError
"""

from typing import Any, Dict, Optional
from pathlib import Path


class AntigravityError(Exception):
    """
    Base exception for all Antigravity Workspace errors.
    
    All custom exceptions in the system inherit from this base class,
    allowing for catch-all error handling when needed.
    
    Attributes:
        message: Human-readable error message
        context: Additional context data for debugging
        recoverable: Whether the error can be recovered from
        suggestion: Suggested action to resolve the error
    """

    def __init__(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        recoverable: bool = False,
        suggestion: Optional[str] = None,
    ):
        """
        Initialize an Antigravity error.
        
        Args:
            message: Human-readable error description
            context: Optional dictionary with error context
            recoverable: Whether recovery is possible
            suggestion: Optional suggestion for fixing the error
        """
        self.message = message
        self.context = context or {}
        self.recoverable = recoverable
        self.suggestion = suggestion
        
        # Build full error message
        full_message = message
        if suggestion:
            full_message += f"\n\nSuggestion: {suggestion}"
        
        super().__init__(full_message)

    def __str__(self) -> str:
        """Return formatted error message."""
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert error to dictionary for serialization.
        
        Returns:
            Dictionary with error details
        """
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "context": self.context,
            "recoverable": self.recoverable,
            "suggestion": self.suggestion,
        }


# Configuration Errors

class ConfigurationError(AntigravityError):
    """
    Raised when configuration is invalid or missing.
    
    Common causes:
    - Missing required API keys
    - Invalid configuration values
    - Malformed configuration files
    - Environment variable issues
    """

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        expected_format: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize configuration error.
        
        Args:
            message: Error description
            config_key: The configuration key that caused the error
            expected_format: Expected format or value
            **kwargs: Additional arguments passed to AntigravityError
        """
        context = kwargs.pop("context", {})
        if config_key:
            context["config_key"] = config_key
        if expected_format:
            context["expected_format"] = expected_format
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", True)
        
        super().__init__(message, **kwargs)


# API Errors

class APIError(AntigravityError):
    """
    Base class for API-related errors.
    
    Raised when communication with external APIs fails.
    """

    def __init__(
        self,
        message: str,
        api_name: Optional[str] = None,
        status_code: Optional[int] = None,
        response: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize API error.
        
        Args:
            message: Error description
            api_name: Name of the API (e.g., "Google Gemini", "OpenAI")
            status_code: HTTP status code if applicable
            response: API response text
            **kwargs: Additional arguments passed to AntigravityError
        """
        context = kwargs.pop("context", {})
        if api_name:
            context["api_name"] = api_name
        if status_code:
            context["status_code"] = status_code
        if response:
            context["response"] = response
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", False)
        
        super().__init__(message, **kwargs)


class APIConnectionError(APIError):
    """Raised when unable to connect to an API endpoint."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "Check your internet connection and verify the API endpoint is accessible."
        )
        super().__init__(message, **kwargs)


class APIAuthenticationError(APIError):
    """Raised when API authentication fails."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "Verify your API key is correct and has not expired. See docs/security.md for setup instructions."
        )
        super().__init__(message, **kwargs)


class APIRateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        context = kwargs.pop("context", {})
        if retry_after:
            context["retry_after"] = retry_after
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            f"Rate limit exceeded. {'Wait ' + str(retry_after) + ' seconds before retrying.' if retry_after else 'Wait before retrying.'}"
        )
        super().__init__(message, **kwargs)


class APITimeoutError(APIError):
    """Raised when an API request times out."""

    def __init__(self, message: str, timeout: Optional[float] = None, **kwargs):
        context = kwargs.pop("context", {})
        if timeout:
            context["timeout"] = timeout
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "The request took too long. Consider increasing the timeout or checking API status."
        )
        super().__init__(message, **kwargs)


# Tool Execution Errors

class ToolExecutionError(AntigravityError):
    """
    Base class for tool execution errors.
    
    Raised when a tool/function fails during execution.
    """

    def __init__(
        self,
        message: str,
        tool_name: Optional[str] = None,
        tool_args: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize tool execution error.
        
        Args:
            message: Error description
            tool_name: Name of the tool that failed
            tool_args: Arguments passed to the tool
            **kwargs: Additional arguments passed to AntigravityError
        """
        context = kwargs.pop("context", {})
        if tool_name:
            context["tool_name"] = tool_name
        if tool_args:
            context["tool_args"] = tool_args
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", False)
        
        super().__init__(message, **kwargs)


class ToolNotFoundError(ToolExecutionError):
    """Raised when a requested tool is not found."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault(
            "suggestion",
            "Check the tool name and ensure all required tools are loaded."
        )
        super().__init__(message, **kwargs)


class ToolValidationError(ToolExecutionError):
    """Raised when tool arguments fail validation."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "Check the tool documentation for correct argument types and values."
        )
        super().__init__(message, **kwargs)


class ToolTimeoutError(ToolExecutionError):
    """Raised when tool execution exceeds timeout."""

    def __init__(self, message: str, timeout: Optional[float] = None, **kwargs):
        context = kwargs.pop("context", {})
        if timeout:
            context["timeout"] = timeout
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "The tool took too long to execute. Consider increasing the timeout."
        )
        super().__init__(message, **kwargs)


# MCP Errors

class MCPError(AntigravityError):
    """
    Base class for Model Context Protocol errors.
    
    Raised when MCP integration fails.
    """

    def __init__(
        self,
        message: str,
        server_name: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize MCP error.
        
        Args:
            message: Error description
            server_name: Name of the MCP server
            **kwargs: Additional arguments passed to AntigravityError
        """
        context = kwargs.pop("context", {})
        if server_name:
            context["server_name"] = server_name
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", False)
        
        super().__init__(message, **kwargs)


class MCPConnectionError(MCPError):
    """Raised when unable to connect to an MCP server."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "Verify the MCP server is running and the configuration is correct. Check mcp_servers.json."
        )
        super().__init__(message, **kwargs)


class MCPServerError(MCPError):
    """Raised when an MCP server returns an error."""

    def __init__(self, message: str, error_code: Optional[str] = None, **kwargs):
        context = kwargs.pop("context", {})
        if error_code:
            context["error_code"] = error_code
        
        kwargs["context"] = context
        super().__init__(message, **kwargs)


class MCPToolError(MCPError):
    """Raised when an MCP tool fails to execute."""

    def __init__(self, message: str, tool_name: Optional[str] = None, **kwargs):
        context = kwargs.pop("context", {})
        if tool_name:
            context["tool_name"] = tool_name
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", True)
        super().__init__(message, **kwargs)


# Memory Errors

class AntigravityMemoryError(AntigravityError):
    """
    Base class for memory/persistence errors.
    
    Raised when memory operations fail.
    Note: Named AntigravityMemoryError to avoid conflict with built-in MemoryError.
    """

    def __init__(
        self,
        message: str,
        file_path: Optional[Path] = None,
        **kwargs
    ):
        """
        Initialize memory error.
        
        Args:
            message: Error description
            file_path: Path to the memory file
            **kwargs: Additional arguments passed to AntigravityError
        """
        context = kwargs.pop("context", {})
        if file_path:
            context["file_path"] = str(file_path)
        
        kwargs["context"] = context
        kwargs.setdefault("recoverable", False)
        
        super().__init__(message, **kwargs)


class MemoryIOError(AntigravityMemoryError):
    """Raised when memory file I/O operations fail."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "Check file permissions and available disk space."
        )
        super().__init__(message, **kwargs)


class MemoryCorruptionError(AntigravityMemoryError):
    """Raised when memory data is corrupted or invalid."""

    def __init__(self, message: str, **kwargs):
        kwargs.setdefault("recoverable", True)
        kwargs.setdefault(
            "suggestion",
            "The memory file may be corrupted. Consider restoring from backup or creating a new one."
        )
        super().__init__(message, **kwargs)

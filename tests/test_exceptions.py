"""
Tests for custom exception hierarchy.

Tests the exception classes, error context, recoverability, and suggestions.
"""

import pytest
from pathlib import Path
from src.exceptions import (
    AntigravityError,
    ConfigurationError,
    APIError,
    APIConnectionError,
    APIAuthenticationError,
    APIRateLimitError,
    APITimeoutError,
    ToolExecutionError,
    ToolNotFoundError,
    ToolValidationError,
    ToolTimeoutError,
    MCPError,
    MCPConnectionError,
    MCPServerError,
    MCPToolError,
    AntigravityMemoryError,
    MemoryIOError,
    MemoryCorruptionError,
)


class TestAntigravityError:
    """Tests for base AntigravityError class."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = AntigravityError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.context == {}
        assert error.recoverable is False
        assert error.suggestion is None

    def test_error_with_context(self):
        """Test error with context data."""
        error = AntigravityError(
            "Test error",
            context={"key": "value", "code": 123}
        )
        assert error.context["key"] == "value"
        assert error.context["code"] == 123

    def test_error_with_suggestion(self):
        """Test error with suggestion."""
        error = AntigravityError(
            "Test error",
            suggestion="Try this fix"
        )
        assert error.suggestion == "Try this fix"
        error_str = str(super(AntigravityError, error).__str__())
        assert "Try this fix" in error_str

    def test_error_recoverable_flag(self):
        """Test recoverable flag."""
        error_recoverable = AntigravityError("Test", recoverable=True)
        error_fatal = AntigravityError("Test", recoverable=False)
        
        assert error_recoverable.recoverable is True
        assert error_fatal.recoverable is False

    def test_error_to_dict(self):
        """Test error serialization to dictionary."""
        error = AntigravityError(
            "Test error",
            context={"key": "value"},
            recoverable=True,
            suggestion="Fix it"
        )
        
        error_dict = error.to_dict()
        assert error_dict["type"] == "AntigravityError"
        assert error_dict["message"] == "Test error"
        assert error_dict["context"] == {"key": "value"}
        assert error_dict["recoverable"] is True
        assert error_dict["suggestion"] == "Fix it"


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error_basic(self):
        """Test basic configuration error."""
        error = ConfigurationError("Invalid config")
        assert isinstance(error, AntigravityError)
        assert str(error) == "Invalid config"

    def test_configuration_error_with_key(self):
        """Test configuration error with config key."""
        error = ConfigurationError(
            "Invalid value",
            config_key="GOOGLE_API_KEY"
        )
        assert error.context["config_key"] == "GOOGLE_API_KEY"

    def test_configuration_error_with_format(self):
        """Test configuration error with expected format."""
        error = ConfigurationError(
            "Invalid format",
            config_key="API_KEY",
            expected_format="AIza..."
        )
        assert error.context["expected_format"] == "AIza..."

    def test_configuration_error_recoverable(self):
        """Test that configuration errors are recoverable by default."""
        error = ConfigurationError("Test")
        assert error.recoverable is True


class TestAPIErrors:
    """Tests for API error hierarchy."""

    def test_api_error_basic(self):
        """Test basic API error."""
        error = APIError("API failed")
        assert isinstance(error, AntigravityError)
        assert str(error) == "API failed"

    def test_api_error_with_details(self):
        """Test API error with details."""
        error = APIError(
            "Request failed",
            api_name="Google Gemini",
            status_code=500,
            response="Server error"
        )
        assert error.context["api_name"] == "Google Gemini"
        assert error.context["status_code"] == 500
        assert error.context["response"] == "Server error"

    def test_api_connection_error(self):
        """Test API connection error."""
        error = APIConnectionError(
            "Cannot connect",
            api_name="OpenAI"
        )
        assert isinstance(error, APIError)
        assert error.recoverable is True
        assert "internet connection" in error.suggestion

    def test_api_authentication_error(self):
        """Test API authentication error."""
        error = APIAuthenticationError(
            "Invalid API key",
            api_name="Google"
        )
        assert isinstance(error, APIError)
        assert error.recoverable is True
        assert "API key" in error.suggestion

    def test_api_rate_limit_error(self):
        """Test API rate limit error."""
        error = APIRateLimitError(
            "Rate limit exceeded",
            retry_after=60
        )
        assert error.recoverable is True
        assert error.context["retry_after"] == 60
        assert "60 seconds" in error.suggestion

    def test_api_timeout_error(self):
        """Test API timeout error."""
        error = APITimeoutError(
            "Request timeout",
            timeout=30.0
        )
        assert error.recoverable is True
        assert error.context["timeout"] == 30.0


class TestToolErrors:
    """Tests for tool execution errors."""

    def test_tool_execution_error_basic(self):
        """Test basic tool execution error."""
        error = ToolExecutionError("Tool failed")
        assert isinstance(error, AntigravityError)

    def test_tool_execution_error_with_details(self):
        """Test tool error with details."""
        error = ToolExecutionError(
            "Execution failed",
            tool_name="web_search",
            tool_args={"query": "test"}
        )
        assert error.context["tool_name"] == "web_search"
        assert error.context["tool_args"] == {"query": "test"}

    def test_tool_not_found_error(self):
        """Test tool not found error."""
        error = ToolNotFoundError(
            "Tool not found",
            tool_name="missing_tool"
        )
        assert isinstance(error, ToolExecutionError)
        assert "tool name" in error.suggestion

    def test_tool_validation_error(self):
        """Test tool validation error."""
        error = ToolValidationError(
            "Invalid arguments",
            tool_name="calculate"
        )
        assert error.recoverable is True
        assert "documentation" in error.suggestion

    def test_tool_timeout_error(self):
        """Test tool timeout error."""
        error = ToolTimeoutError(
            "Tool timeout",
            tool_name="slow_tool",
            timeout=10.0
        )
        assert error.recoverable is True
        assert error.context["timeout"] == 10.0


class TestMCPErrors:
    """Tests for MCP-related errors."""

    def test_mcp_error_basic(self):
        """Test basic MCP error."""
        error = MCPError("MCP failed")
        assert isinstance(error, AntigravityError)

    def test_mcp_error_with_server(self):
        """Test MCP error with server name."""
        error = MCPError(
            "Connection failed",
            server_name="github-mcp-server"
        )
        assert error.context["server_name"] == "github-mcp-server"

    def test_mcp_connection_error(self):
        """Test MCP connection error."""
        error = MCPConnectionError(
            "Cannot connect to server",
            server_name="test-server"
        )
        assert isinstance(error, MCPError)
        assert error.recoverable is True
        assert "mcp_servers.json" in error.suggestion

    def test_mcp_server_error(self):
        """Test MCP server error."""
        error = MCPServerError(
            "Server error",
            server_name="test-server",
            error_code="ERR_500"
        )
        assert error.context["error_code"] == "ERR_500"

    def test_mcp_tool_error(self):
        """Test MCP tool error."""
        error = MCPToolError(
            "Tool execution failed",
            server_name="test-server",
            tool_name="test_tool"
        )
        assert error.context["tool_name"] == "test_tool"
        assert error.recoverable is True


class TestMemoryErrors:
    """Tests for memory-related errors."""

    def test_memory_error_basic(self):
        """Test basic memory error."""
        error = AntigravityMemoryError("Memory operation failed")
        assert isinstance(error, AntigravityError)

    def test_memory_error_with_path(self):
        """Test memory error with file path."""
        path = Path("/tmp/memory.json")
        error = AntigravityMemoryError(
            "Cannot read file",
            file_path=path
        )
        assert error.context["file_path"] == str(path)

    def test_memory_io_error(self):
        """Test memory I/O error."""
        error = MemoryIOError(
            "Cannot write to file",
            file_path=Path("/tmp/test.json")
        )
        assert isinstance(error, AntigravityMemoryError)
        assert error.recoverable is True
        assert "permissions" in error.suggestion

    def test_memory_corruption_error(self):
        """Test memory corruption error."""
        error = MemoryCorruptionError(
            "Invalid JSON data",
            file_path=Path("/tmp/corrupted.json")
        )
        assert error.recoverable is True
        assert "backup" in error.suggestion


class TestErrorInheritance:
    """Tests for error inheritance hierarchy."""

    def test_all_errors_inherit_from_base(self):
        """Test all custom errors inherit from AntigravityError."""
        error_classes = [
            ConfigurationError,
            APIError,
            APIConnectionError,
            ToolExecutionError,
            MCPError,
            AntigravityMemoryError,
        ]
        
        for error_class in error_classes:
            error = error_class("Test")
            assert isinstance(error, AntigravityError)

    def test_error_hierarchy(self):
        """Test specific error hierarchies."""
        # API errors
        assert issubclass(APIConnectionError, APIError)
        assert issubclass(APIAuthenticationError, APIError)
        
        # Tool errors
        assert issubclass(ToolNotFoundError, ToolExecutionError)
        assert issubclass(ToolValidationError, ToolExecutionError)
        
        # MCP errors
        assert issubclass(MCPConnectionError, MCPError)
        assert issubclass(MCPServerError, MCPError)
        
        # Memory errors
        assert issubclass(MemoryIOError, AntigravityMemoryError)
        assert issubclass(MemoryCorruptionError, AntigravityMemoryError)


class TestErrorCatching:
    """Tests for catching errors at different levels."""

    def test_catch_specific_error(self):
        """Test catching specific error type."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Test")

    def test_catch_base_error(self):
        """Test catching any Antigravity error."""
        with pytest.raises(AntigravityError):
            raise APIConnectionError("Test")

    def test_catch_category(self):
        """Test catching error category."""
        with pytest.raises(APIError):
            raise APIAuthenticationError("Test")

    def test_error_distinction(self):
        """Test different error types can be distinguished."""
        config_error = ConfigurationError("Config")
        api_error = APIError("API")
        
        assert isinstance(config_error, ConfigurationError)
        assert not isinstance(config_error, APIError)
        assert isinstance(api_error, APIError)
        assert not isinstance(api_error, ConfigurationError)

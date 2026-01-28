# Error Handling Guide

## Overview

The Antigravity Workspace uses a comprehensive custom exception hierarchy that provides clear error categorization, rich context, recovery strategies, and helpful error messages for both developers and end users.

## Exception Hierarchy

All custom exceptions inherit from `AntigravityError`, allowing for flexible error handling at different levels of specificity.

```
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
└── AntigravityMemoryError (memory/persistence failures)
    ├── MemoryIOError
    └── MemoryCorruptionError
```

## Core Concepts

### Error Attributes

All Antigravity errors include the following attributes:

- **`message`**: Human-readable error description
- **`context`**: Dictionary with additional debugging information
- **`recoverable`**: Boolean indicating if recovery is possible
- **`suggestion`**: Optional recommended action to resolve the error

### Error Context

Error context provides additional debugging information:

```python
from src.exceptions import APIError

try:
    # API call
    ...
except APIError as e:
    print(f"API: {e.context.get('api_name')}")
    print(f"Status: {e.context.get('status_code')}")
    print(f"Response: {e.context.get('response')}")
```

### Recoverability

Errors are marked as recoverable or fatal:

```python
from src.exceptions import APIConnectionError, MemoryCorruptionError

# Recoverable error - can retry
connection_error = APIConnectionError("Cannot connect")
if connection_error.recoverable:
    # Implement retry logic
    ...

# Fatal error - cannot recover
corruption_error = MemoryCorruptionError("Data corrupted")
if not corruption_error.recoverable:
    # Log and exit gracefully
    ...
```

## Exception Types

### ConfigurationError

**When to use:** Configuration validation failures, missing API keys, invalid settings

**Common causes:**
- Missing or invalid API keys
- Malformed configuration files
- Invalid environment variables
- Path validation failures

**Example:**

```python
from src.exceptions import ConfigurationError

raise ConfigurationError(
    "Invalid Google API key format",
    config_key="GOOGLE_API_KEY",
    expected_format="AIza...",
    suggestion="API keys should start with 'AIza'. Get your key from Google AI Studio."
)
```

**Handling:**

```python
from src.exceptions import ConfigurationError
from src.config import settings

try:
    settings.validate_configuration()
except ConfigurationError as e:
    print(f"Configuration error: {e.message}")
    print(f"Field: {e.context.get('config_key')}")
    if e.suggestion:
        print(f"Suggestion: {e.suggestion}")
    # Prompt user to fix configuration
```

### APIError Hierarchy

**When to use:** External API communication failures

#### APIConnectionError

Connection failures, network issues, unreachable endpoints.

```python
from src.exceptions import APIConnectionError

raise APIConnectionError(
    "Failed to connect to Google Gemini API",
    api_name="Google Gemini",
    suggestion="Check internet connection and API endpoint status"
)
```

#### APIAuthenticationError

Authentication failures, invalid API keys, expired tokens.

```python
from src.exceptions import APIAuthenticationError

raise APIAuthenticationError(
    "Invalid API key",
    api_name="OpenAI",
    status_code=401
)
```

#### APIRateLimitError

Rate limiting, quota exceeded.

```python
from src.exceptions import APIRateLimitError

raise APIRateLimitError(
    "API rate limit exceeded",
    api_name="Google Gemini",
    retry_after=60  # Retry after 60 seconds
)
```

#### APITimeoutError

Request timeouts, slow responses.

```python
from src.exceptions import APITimeoutError

raise APITimeoutError(
    "API request timed out",
    api_name="OpenAI",
    timeout=30.0
)
```

**Handling API Errors:**

```python
from src.exceptions import (
    APIError,
    APIConnectionError,
    APIRateLimitError,
    APITimeoutError
)
import time

def call_api_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            # Make API call
            return api_call()
        
        except APIRateLimitError as e:
            # Wait before retrying
            wait_time = e.context.get('retry_after', 60)
            print(f"Rate limited. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        
        except APITimeoutError as e:
            # Retry with exponential backoff
            if attempt < max_retries - 1:
                print(f"Timeout. Retrying ({attempt + 1}/{max_retries})...")
                time.sleep(2 ** attempt)
        
        except APIConnectionError as e:
            # Check connection and retry
            print(e.suggestion)
            if attempt < max_retries - 1:
                time.sleep(5)
        
        except APIError as e:
            # Fatal API error
            print(f"API error: {e.message}")
            raise
```

### ToolExecutionError Hierarchy

**When to use:** Tool/function execution failures

#### ToolNotFoundError

Requested tool doesn't exist.

```python
from src.exceptions import ToolNotFoundError

raise ToolNotFoundError(
    "Tool not found",
    tool_name="non_existent_tool"
)
```

#### ToolValidationError

Invalid tool arguments.

```python
from src.exceptions import ToolValidationError

raise ToolValidationError(
    "Invalid argument type",
    tool_name="calculate",
    tool_args={"x": "not_a_number"}
)
```

#### ToolTimeoutError

Tool execution timeout.

```python
from src.exceptions import ToolTimeoutError

raise ToolTimeoutError(
    "Tool execution timed out",
    tool_name="long_running_tool",
    timeout=10.0
)
```

**Handling Tool Errors:**

```python
from src.exceptions import ToolExecutionError, ToolValidationError

def execute_tool(tool_name, **kwargs):
    try:
        tool = get_tool(tool_name)
        return tool.execute(**kwargs)
    
    except ToolValidationError as e:
        # Log validation error and return user-friendly message
        print(f"Invalid arguments for {tool_name}: {e.message}")
        print(f"Suggestion: {e.suggestion}")
        return {"error": e.message, "suggestion": e.suggestion}
    
    except ToolExecutionError as e:
        # Log execution error
        print(f"Tool execution failed: {e.message}")
        if e.recoverable:
            # Attempt fallback
            return execute_fallback_tool()
        raise
```

### MCPError Hierarchy

**When to use:** Model Context Protocol integration failures

#### MCPConnectionError

Cannot connect to MCP server.

```python
from src.exceptions import MCPConnectionError

raise MCPConnectionError(
    "Cannot connect to MCP server",
    server_name="github-mcp-server"
)
```

#### MCPServerError

MCP server returned an error.

```python
from src.exceptions import MCPServerError

raise MCPServerError(
    "MCP server error",
    server_name="perplexity-ask",
    error_code="ERR_500"
)
```

#### MCPToolError

MCP tool execution failed.

```python
from src.exceptions import MCPToolError

raise MCPToolError(
    "MCP tool failed",
    server_name="github-mcp-server",
    tool_name="create_repository"
)
```

**Handling MCP Errors:**

```python
from src.exceptions import MCPConnectionError, MCPToolError

def execute_mcp_tool(server_name, tool_name, **kwargs):
    try:
        server = connect_to_mcp_server(server_name)
        return server.execute_tool(tool_name, **kwargs)
    
    except MCPConnectionError as e:
        # Graceful degradation - disable MCP for this session
        print(f"MCP connection failed: {e.message}")
        print("Continuing without MCP integration")
        return None
    
    except MCPToolError as e:
        # Log and return error to user
        print(f"MCP tool error: {e.message}")
        return {"error": e.message}
```

### AntigravityMemoryError Hierarchy

**When to use:** Memory/persistence failures

#### MemoryIOError

File I/O failures.

```python
from src.exceptions import MemoryIOError
from pathlib import Path

raise MemoryIOError(
    "Cannot write to memory file",
    file_path=Path("./data/memory.json")
)
```

#### MemoryCorruptionError

Corrupted or invalid data.

```python
from src.exceptions import MemoryCorruptionError

raise MemoryCorruptionError(
    "Memory file contains invalid JSON",
    file_path=Path("./data/memory.json")
)
```

**Handling Memory Errors:**

```python
from src.exceptions import MemoryIOError, MemoryCorruptionError
import json

def load_memory(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    
    except json.JSONDecodeError:
        raise MemoryCorruptionError(
            "Invalid JSON in memory file",
            file_path=path
        )
    
    except IOError as e:
        raise MemoryIOError(
            f"Cannot read memory file: {e}",
            file_path=path
        )

# Usage
try:
    memory = load_memory("./data/memory.json")
except MemoryCorruptionError as e:
    # Restore from backup
    print(f"Memory corrupted: {e.message}")
    print(e.suggestion)
    memory = restore_from_backup()
except MemoryIOError as e:
    # Create new file
    print(f"Cannot read memory: {e.message}")
    memory = create_new_memory()
```

## Best Practices

### 1. Use Specific Exceptions

Always use the most specific exception type:

```python
# ✅ Good - specific
raise APIAuthenticationError("Invalid API key", api_name="Google")

# ❌ Avoid - too generic
raise Exception("API error")
```

### 2. Provide Rich Context

Include relevant debugging information:

```python
# ✅ Good - includes context
raise ToolExecutionError(
    "Tool failed",
    tool_name="calculate",
    tool_args={"x": 10, "y": 0}
)

# ❌ Avoid - no context
raise ToolExecutionError("Tool failed")
```

### 3. Add Helpful Suggestions

Always provide actionable suggestions:

```python
# ✅ Good - helpful suggestion
raise ConfigurationError(
    "API key missing",
    config_key="GOOGLE_API_KEY",
    suggestion="Set GOOGLE_API_KEY in your .env file. See docs/security.md for setup instructions."
)
```

### 4. Handle Recoverable Errors

Implement retry logic for recoverable errors:

```python
def resilient_operation():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return risky_operation()
        except AntigravityError as e:
            if not e.recoverable or attempt == max_retries - 1:
                raise
            # Retry
            time.sleep(2 ** attempt)
```

### 5. Log Error Context

Always log error context for debugging:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

try:
    risky_operation()
except AntigravityError as e:
    logger.error(
        f"{e.__class__.__name__}: {e.message}",
        extra={"context": e.context, "recoverable": e.recoverable}
    )
    raise
```

### 6. Convert to User-Friendly Messages

Convert technical errors to user-friendly messages:

```python
def execute_user_request():
    try:
        return execute_complex_operation()
    except APIRateLimitError as e:
        return {
            "status": "error",
            "message": "Too many requests. Please try again in a minute.",
            "retry_after": e.context.get("retry_after")
        }
    except ConfigurationError as e:
        return {
            "status": "error",
            "message": "Configuration issue",
            "details": e.suggestion
        }
```

## Error Serialization

Errors can be serialized for logging or API responses:

```python
from src.exceptions import APIError

try:
    api_call()
except APIError as e:
    error_dict = e.to_dict()
    # {
    #     "type": "APIConnectionError",
    #     "message": "Cannot connect",
    #     "context": {"api_name": "Google"},
    #     "recoverable": True,
    #     "suggestion": "Check internet connection"
    # }
    
    # Log or return to API
    logger.error(json.dumps(error_dict))
```

## Migration Guide

To update existing code to use the new exception system:

1. **Replace generic exceptions:**
   ```python
   # Before
   raise Exception("Config invalid")
   
   # After
   raise ConfigurationError("Config invalid", config_key="API_KEY")
   ```

2. **Add error context:**
   ```python
   # Before
   raise ValueError("Tool not found")
   
   # After
   raise ToolNotFoundError("Tool not found", tool_name="missing_tool")
   ```

3. **Update exception handlers:**
   ```python
   # Before
   except Exception as e:
       print(f"Error: {e}")
   
   # After
   except AntigravityError as e:
       logger.error(f"{e.message}", extra=e.context)
       if e.suggestion:
           print(f"Suggestion: {e.suggestion}")
   ```

## Reference

- **Exception module:** `src/exceptions.py`
- **Tests:** `tests/test_exceptions.py`
- **Configuration validation:** `src/config_validator.py`

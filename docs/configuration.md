# Configuration Schema Documentation

## Overview

The Antigravity Workspace uses a hierarchical configuration system that supports environment-specific settings, validation, and flexible deployment scenarios.

## Configuration Files

### Primary Configuration: `.env`

The `.env` file contains environment variables that configure the application. This file should **never** be committed to version control.

```bash
# Environment
ENV=development  # Options: development, testing, production

# Google Gemini API
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash

# Agent Settings
AGENT_NAME=AntigravityAgent
DEBUG_MODE=false

# OpenAI-Compatible API (Optional)
OPENAI_BASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# File Paths
MEMORY_FILE=./data/agent_memory.json
MCP_SERVERS_CONFIG=./data/mcp_servers.json
WORKSPACE_DIR=./workspace

# MCP Configuration
MCP_ENABLED=false
MCP_CONNECTION_TIMEOUT=30
MCP_TOOL_PREFIX=mcp_
```

### Template: `.env.example`

Provides a template for creating your `.env` file. Contains placeholder values and documentation.

## Configuration Schema

### Environment Settings

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ENV` | string | `development` | Deployment environment: `development`, `testing`, or `production` |

### Google Gemini API

| Field | Type | Default | Required | Description |
|-------|------|---------|----------|-------------|
| `GOOGLE_API_KEY` | string | `""` | Yes* | Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `GEMINI_MODEL_NAME` | string | `gemini-2.5-flash` | No | Gemini model to use for generation |

*Required if using Gemini as the LLM provider

### Agent Configuration

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `AGENT_NAME` | string | `AntigravityAgent` | Name identifier for the agent |
| `DEBUG_MODE` | boolean | `false` | Enable debug output and verbose logging |

### OpenAI-Compatible API (Optional)

| Field | Type | Default | Required | Description |
|-------|------|---------|----------|-------------|
| `OPENAI_BASE_URL` | string | `""` | No | Base URL for OpenAI-compatible endpoint |
| `OPENAI_API_KEY` | string | `""` | No | API key for the endpoint |
| `OPENAI_MODEL` | string | `gpt-4o-mini` | No | Model name for chat completions |

### File Paths

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `MEMORY_FILE` | string | `./data/agent_memory.json` | Path to agent memory storage file |
| `MCP_SERVERS_CONFIG` | string | `./data/mcp_servers.json` | Path to MCP servers configuration |
| `WORKSPACE_DIR` | string | `./workspace` | Working directory for agent operations |

### Model Context Protocol (MCP)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `MCP_ENABLED` | boolean | `false` | Enable MCP integration for external tools |
| `MCP_CONNECTION_TIMEOUT` | integer | `30` | Timeout (seconds) for MCP server connections |
| `MCP_TOOL_PREFIX` | string | `mcp_` | Prefix for MCP tool names to avoid conflicts |

## Environment-Specific Configurations

The system supports three deployment environments with optimized defaults:

### Development Environment (`ENV=development`)

Optimized for local development with maximum visibility and debugging capabilities.

```python
LOG_LEVEL = "DEBUG"
LOG_TO_FILE = True
LOG_TO_CONSOLE = True
DEBUG_MODE = True
VERBOSE_OUTPUT = True
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
MEMORY_AUTO_SAVE = True
MCP_ENABLED = True
STRICT_MODE = False
```

**Use case:** Local development, debugging, feature implementation

### Testing Environment (`ENV=testing`)

Optimized for unit/integration testing with minimal external dependencies.

```python
LOG_LEVEL = "WARNING"
LOG_TO_FILE = False
LOG_TO_CONSOLE = False
DEBUG_MODE = False
VERBOSE_OUTPUT = False
MAX_RETRIES = 1
REQUEST_TIMEOUT = 5
MEMORY_AUTO_SAVE = False
MCP_ENABLED = False
STRICT_MODE = True
```

**Use case:** CI/CD pipelines, automated testing, test suites

### Production Environment (`ENV=production`)

Optimized for production deployment with security and reliability.

```python
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
LOG_TO_CONSOLE = True
DEBUG_MODE = False
VERBOSE_OUTPUT = False
MAX_RETRIES = 5
REQUEST_TIMEOUT = 60
MEMORY_AUTO_SAVE = True
MCP_ENABLED = True
STRICT_MODE = True
```

**Use case:** Production deployments, live services, end-user applications

## Configuration Validation

Configuration values are validated at runtime using `src/config_validator.py`. The following validations are performed:

### API Key Validation

- **Google API Keys:** Must start with `AIza` and be 39+ characters
- **OpenAI API Keys:** Must start with `sk-` and be 40+ characters
- Placeholder values (e.g., `your_api_key_here`) are rejected

### URL Validation

- Must be valid HTTP/HTTPS URLs
- Scheme and netloc must be present
- Used for `OPENAI_BASE_URL`

### File Path Validation

- Prevents path traversal attacks (`../`, absolute paths outside workspace)
- Automatically creates parent directories if they don't exist
- Validates workspace directory is accessible

### Model Name Validation

- Google: Must start with `gemini-` or `models/gemini-`
- Ensures valid model identifiers

## Usage Examples

### Basic Setup

```bash
# 1. Copy the example configuration
cp .env.example .env

# 2. Add your API key
# Edit .env and set GOOGLE_API_KEY

# 3. The application will automatically load settings
python agent.py
```

### Environment-Specific Setup

```bash
# Development
export ENV=development
python agent.py

# Testing
export ENV=testing
pytest tests/

# Production
export ENV=production
python agent.py
```

### Programmatic Access

```python
from src.config import settings

# Access configuration values
api_key = settings.GOOGLE_API_KEY
model = settings.GEMINI_MODEL_NAME
debug = settings.DEBUG_MODE

# Validate configuration
try:
    settings.validate_configuration()
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

### Environment Detection

```python
from src.config import settings
from src.env_config import get_env_config

# Get current environment
current_env = settings.ENV

# Get environment-specific configuration class
env_config = get_env_config(current_env)
log_level = env_config.LOG_LEVEL
```

## Security Best Practices

1. **Never commit `.env`** - Always in `.gitignore`
2. **Use `.env.example`** - Template without sensitive data
3. **Rotate API keys** - When exposed or compromised
4. **Use environment variables** - For secrets in production
5. **Validate inputs** - Call `validate_configuration()` at startup
6. **Restrict file access** - Keep config files with proper permissions

## Troubleshooting

### Configuration Not Loading

1. Verify `.env` file exists in project root
2. Check file permissions (should be readable)
3. Verify no syntax errors in `.env`
4. Check for environment variable conflicts

### Validation Errors

```python
# Example error
ConfigurationError: Invalid Google API key format. Expected key starting with 'AIza'

# Solution
1. Verify API key is correctly copied
2. No extra spaces or quotes
3. Key is from correct provider (Google AI Studio)
```

### Environment Not Applied

```python
# Verify environment is set
from src.config import settings
print(f"Current environment: {settings.ENV}")

# Check environment config
from src.env_config import get_env_config
env_config = get_env_config(settings.ENV)
print(f"Log level: {env_config.LOG_LEVEL}")
```

## Reference

- **Configuration file:** `src/config.py`
- **Validation module:** `src/config_validator.py`
- **Environment configs:** `src/env_config.py`
- **Security guide:** `docs/security.md`

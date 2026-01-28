# Component-05: Manejo de Errores

## Prioridad: 🟠 ALTO
## Tiempo Estimado: 2 horas
## Dependencias: Component-03 (usa logging)

---

## Issues a Resolver

| ID | Issue | Archivo | Línea |
|----|-------|---------|-------|
| ERR-01 | Broad exception catch | `src/agent.py` | 105, 205 |
| ERR-02 | Broad exception catch | `src/sandbox/docker_exec.py` | 26-29 |
| ERR-03 | Broad exception catch | `src/mcp_client.py` | 301, 384, 444, 460 |
| ERR-04 | Exception silenciada | `src/sandbox/docker_exec.py` | 96-101 |
| ERR-05 | Sin manejo de OSError | `src/memory.py` | 45 |
| ERR-06 | Variable posiblemente unbound | `src/tools/openai_proxy.py` | 73 |
| ERR-07 | Atributo de None | `src/agent.py` | 278 |

---

## Interface / Cambios Esperados

### Nuevo Archivo: `src/exceptions.py`
```python
"""
Custom exceptions for Antigravity Workspace.

Provides specific exception types for better error handling
and debugging across the application.
"""

class AntigravityError(Exception):
    """Base exception for all Antigravity errors."""
    pass


class ConfigurationError(AntigravityError):
    """Raised when configuration is invalid or missing."""
    pass


class ToolExecutionError(AntigravityError):
    """Raised when a tool fails to execute."""
    pass


class MCPConnectionError(AntigravityError):
    """Raised when MCP server connection fails."""
    pass


class SandboxError(AntigravityError):
    """Raised when sandbox execution fails."""
    pass


class MemoryError(AntigravityError):
    """Raised when memory operations fail."""
    pass


class APIError(AntigravityError):
    """Raised when API calls fail."""
    pass
```

### Patrón de Corrección: Excepciones Específicas
```python
# ANTES
try:
    result = some_operation()
except Exception as e:
    print(f"Error: {e}")

# DESPUÉS
from src.exceptions import ToolExecutionError
from src.logging_config import get_logger

logger = get_logger(__name__)

try:
    result = some_operation()
except FileNotFoundError as e:
    logger.error("File not found: %s", e)
    raise ConfigurationError(f"Required file missing: {e}") from e
except ConnectionError as e:
    logger.error("Connection failed: %s", e)
    raise MCPConnectionError(f"Failed to connect: {e}") from e
except Exception as e:
    logger.exception("Unexpected error during operation")
    raise AntigravityError(f"Unexpected error: {e}") from e
```

### Fix: `src/agent.py` línea 278
```python
# ANTES
response_obj = self.client.models.generate_content(...)

# DESPUÉS
if self.client is None:
    raise ConfigurationError("Client not initialized")
response_obj = self.client.models.generate_content(...)
```

### Fix: `src/tools/openai_proxy.py` línea 73
```python
# ANTES
try:
    response = client.chat.completions.create(...)
except Exception:
    pass
return response.choices[0].message.content  # response puede no existir

# DESPUÉS
response = None
try:
    response = client.chat.completions.create(...)
except OpenAIError as e:
    logger.error("OpenAI API error: %s", e)
    raise APIError(f"OpenAI call failed: {e}") from e

if response is None or not response.choices:
    raise APIError("Empty response from OpenAI API")
    
return response.choices[0].message.content
```

### Fix: `src/sandbox/docker_exec.py` línea 96-101
```python
# ANTES
try:
    container.kill()
except:
    pass  # Silenciado completamente

# DESPUÉS
try:
    container.kill()
except docker.errors.NotFound:
    logger.debug("Container already stopped")
except docker.errors.APIError as e:
    logger.warning("Failed to kill container: %s", e)
```

---

## Tasks

- [ ] **05.1** Crear `src/exceptions.py` con excepciones custom
- [ ] **05.2** Fix null check en `src/agent.py:278`
- [ ] **05.3** Fix variable unbound en `src/tools/openai_proxy.py:73`
- [ ] **05.4** Refactorizar excepciones en `src/agent.py`
- [ ] **05.5** Refactorizar excepciones en `src/sandbox/docker_exec.py`
- [ ] **05.6** Refactorizar excepciones en `src/mcp_client.py`
- [ ] **05.7** Agregar manejo de OSError en `src/memory.py`
- [ ] **05.8** Agregar tests para excepciones custom
- [ ] **05.9** Verificar que errores LSP se resuelvan

---

## Verificación (Acceptance Criteria)

```bash
# 1. Sin errores LSP
# Verificar en IDE que los 4 errores LSP desaparezcan

# 2. Excepciones deben importarse correctamente
python -c "from src.exceptions import AntigravityError, ConfigurationError"

# 3. Tests deben pasar
pytest tests/ -v

# 4. No deben quedar bare except
grep -rn "except:" src/ --include="*.py" | wc -l
# Debe ser 0
```

# Component-07: Refactorización de Duplicados

## Prioridad: 🟡 MEDIO
## Tiempo Estimado: 2 horas
## Dependencias: Component-06 (types definidos)

---

## Issues a Resolver

| ID | Issue | Archivo | Líneas |
|----|-------|---------|--------|
| DUP-01 | `_DummyClient` duplicado (1) | `src/agent.py` | 76-87 |
| DUP-02 | `_DummyClient` duplicado (2) | `src/agent.py` | 108-119 |
| DUP-03 | `_DummyClient` duplicado (3) | `src/agents/base_agent.py` | 38-46, 53-61 |
| DUP-04 | Lógica duplicada en `_call_gemini` | `src/agent.py` | 267-299 |
| DUP-05 | Import no usado | `src/tools/example_tool.py` | 1 |
| DUP-06 | TODOs en producción | `src/config.py` | 56, 64-65, 68-69, 73-74, 78 |

---

## Interface / Cambios Esperados

### Nuevo Archivo: `src/clients.py`
```python
"""
Client abstractions for Antigravity Workspace.

Provides client implementations for different LLM backends,
including a dummy client for testing environments.
"""
from typing import Any, Optional, Protocol


class LLMResponse(Protocol):
    """Protocol for LLM response objects."""
    text: str


class LLMClient(Protocol):
    """Protocol for LLM client implementations."""
    
    def generate(self, model: str, contents: str) -> LLMResponse:
        """Generate content using the LLM."""
        ...


class DummyResponse:
    """Mock response for testing environments."""
    
    def __init__(self, text: str = "I have completed the task"):
        self.text = text
        self.content = text


class DummyModels:
    """Mock models interface for testing."""
    
    def generate_content(
        self, 
        model: str, 
        contents: str
    ) -> DummyResponse:
        """Return a canned response for testing."""
        return DummyResponse()


class DummyClient:
    """
    Lightweight dummy client for testing environments.
    
    Used when:
    - Running under pytest
    - No API key is configured
    - Network access is unavailable
    
    Provides deterministic responses for testing purposes.
    """
    
    def __init__(self):
        self.models = DummyModels()


def create_dummy_client() -> DummyClient:
    """
    Factory function to create a DummyClient instance.
    
    Returns:
        Configured DummyClient for testing.
    """
    return DummyClient()


def is_test_environment() -> bool:
    """
    Check if running in a test environment.
    
    Returns:
        True if running under pytest or test markers present.
    """
    import os
    import sys
    return (
        "PYTEST_CURRENT_TEST" in os.environ 
        or "pytest" in sys.modules
    )
```

### Actualización: `src/agent.py`
```python
# ANTES (líneas 74-119 con dos _DummyClient)

# DESPUÉS
from src.clients import DummyClient, is_test_environment

# En __init__:
if is_test_environment():
    self.client = DummyClient()
else:
    # ... resto de la lógica de inicialización
```

### Actualización: `src/agents/base_agent.py`
```python
# ANTES (dos definiciones de _DummyClient)

# DESPUÉS  
from src.clients import DummyClient, is_test_environment

class BaseAgent:
    def __init__(self):
        if is_test_environment():
            self.client = DummyClient()
        # ...
```

### Fix: `src/tools/example_tool.py`
```python
# ANTES
import requests  # No usado

# DESPUÉS
# Eliminar import no usado
```

### Fix: `src/config.py` - Mover TODOs a Issues
```python
# ANTES
MEMORY_FILE: str = "./agent_memory.json"  # TODO: Implement a more robust memory system

# DESPUÉS
MEMORY_FILE: str = "./agent_memory.json"
# Los TODOs se mueven a GitHub Issues con labels apropiados
```

---

## Tasks

- [ ] **07.1** Crear `src/clients.py` con `DummyClient` y helpers
- [ ] **07.2** Refactorizar `src/agent.py` para usar `src/clients.py`
- [ ] **07.3** Refactorizar `src/agents/base_agent.py` para usar `src/clients.py`
- [ ] **07.4** Simplificar lógica en `_call_gemini` usando early returns
- [ ] **07.5** Eliminar import no usado en `src/tools/example_tool.py`
- [ ] **07.6** Crear GitHub Issues para cada TODO en `src/config.py`
- [ ] **07.7** Eliminar TODOs de `src/config.py`
- [ ] **07.8** Agregar tests para `src/clients.py`
- [ ] **07.9** Verificar que error LSP de `_DummyClient` se resuelva

---

## GitHub Issues a Crear (de TODOs)

1. **Issue**: "Implement robust memory system with persistence options"
   - Labels: `enhancement`, `memory`
   - Body: Current system uses simple JSON file. Consider: SQLite, Redis, vector DB.

2. **Issue**: "Implement configurable MCP connection timeout"
   - Labels: `enhancement`, `mcp`
   - Body: Add retry logic and exponential backoff.

3. **Issue**: "Implement MCP tool prefix configuration"
   - Labels: `enhancement`, `mcp`
   - Body: Allow customization of tool name prefixes.

4. **Issue**: "Implement workspace isolation"
   - Labels: `enhancement`, `security`
   - Body: Sandbox workspace access per agent session.

5. **Issue**: "Implement dynamic model configuration"
   - Labels: `enhancement`, `config`
   - Body: Support model switching at runtime, model aliases.

---

## Verificación (Acceptance Criteria)

```bash
# 1. DummyClient debe estar en un solo lugar
grep -rn "class _DummyClient\|class DummyClient" src/ --include="*.py"
# Debe mostrar solo src/clients.py

# 2. Sin imports no usados
python -m py_compile src/tools/example_tool.py

# 3. Sin TODOs en config
grep -n "TODO" src/config.py
# Debe retornar vacío

# 4. Error LSP resuelto
# Verificar en IDE

# 5. Tests pasan
pytest tests/ -v
```

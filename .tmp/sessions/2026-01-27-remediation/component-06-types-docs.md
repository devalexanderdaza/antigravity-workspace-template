# Component-06: Type Hints y Docstrings

## Prioridad: 🟡 MEDIO
## Tiempo Estimado: 2.5 horas
## Dependencias: Component-05 (tipos de excepciones definidos)

---

## Issues a Resolver

| ID | Issue | Archivo | Ubicación |
|----|-------|---------|-----------|
| TYP-01 | Return type faltante | `src/memory.py` | `_load_memory()` línea 16 |
| TYP-02 | Return type faltante | `src/memory.py` | `save_memory()` línea 39 |
| TYP-03 | Sintaxis moderna sin import | `src/sandbox/docker_exec.py` | línea 17 |
| TYP-04 | Return type faltante | `src/skills/research/tools.py` | `deep_research` línea 3 |
| TYP-05 | Type hints incompletos | `src/tools/mcp_tools.py` | líneas 260-268 |
| DOC-01 | Module docstring faltante | `src/sandbox/__init__.py` | - |
| DOC-02 | Docstrings faltantes | `tests/conftest.py` | fixtures |
| DOC-03 | Docstrings faltantes | `tests/test_execution_tool.py` | tests |
| DOC-04 | Docstrings faltantes | `tests/test_local_sandbox.py` | tests |
| DOC-05 | Docstrings faltantes | `tests/test_factory.py` | tests |

---

## Interface / Cambios Esperados

### Archivo: `src/memory.py`
```python
from typing import Any, Dict, List

def _load_memory(self) -> Dict[str, Any]:
    """
    Load memory from persistent storage.
    
    Returns:
        Dictionary containing conversation history and summary.
        Returns empty structure if file doesn't exist.
        
    Raises:
        MemoryError: If file exists but cannot be parsed.
    """
    ...

def save_memory(self) -> None:
    """
    Persist current memory state to disk.
    
    Raises:
        MemoryError: If file cannot be written.
    """
    ...
```

### Archivo: `src/sandbox/docker_exec.py`
```python
from __future__ import annotations  # Agregar al inicio
from typing import Optional

def execute(self, code: str, timeout: int = 30) -> tuple[bool, Optional[str]]:
    ...
```

### Archivo: `src/skills/research/tools.py`
```python
def deep_research(query: str) -> str:
    """
    Perform deep research on a given query.
    
    Args:
        query: The research question or topic.
        
    Returns:
        Research findings as formatted string.
    """
    ...
```

### Archivo: `src/tools/mcp_tools.py`
```python
from typing import Any, Optional
from src.mcp_client import MCPClientManager

_mcp_manager: Optional[MCPClientManager] = None

def _set_mcp_manager(manager: MCPClientManager) -> None:
    """
    Set the global MCP manager reference.
    
    Args:
        manager: MCPClientManager instance to use globally.
    """
    global _mcp_manager
    _mcp_manager = manager

def _get_mcp_manager() -> Optional[MCPClientManager]:
    """
    Get the global MCP manager reference.
    
    Returns:
        Current MCPClientManager instance or None if not set.
    """
    return _mcp_manager
```

### Archivo: `src/sandbox/__init__.py`
```python
"""
Sandbox execution module for Antigravity Workspace.

Provides secure code execution environments including:
- LocalSandbox: Process-based isolation for development
- DockerSandbox: Container-based isolation for production
- SandboxFactory: Automatic sandbox selection based on environment

Usage:
    from src.sandbox import create_sandbox
    
    sandbox = create_sandbox()
    success, output = sandbox.execute("print('Hello')")
"""
from src.sandbox.factory import create_sandbox
from src.sandbox.base import CodeSandbox
from src.sandbox.local import LocalSandbox
from src.sandbox.docker_exec import DockerSandbox

__all__ = ["create_sandbox", "CodeSandbox", "LocalSandbox", "DockerSandbox"]
```

### Patrón para Tests
```python
def test_example_function():
    """
    Test that example_function returns expected output.
    
    Verifies:
        - Function handles valid input correctly
        - Return type matches specification
    """
    # Arrange
    input_value = "test"
    
    # Act
    result = example_function(input_value)
    
    # Assert
    assert result == "expected"
```

---

## Tasks

- [ ] **06.1** Agregar type hints a `src/memory.py`
- [ ] **06.2** Agregar `from __future__ import annotations` a `src/sandbox/docker_exec.py`
- [ ] **06.3** Agregar return type a `src/skills/research/tools.py`
- [ ] **06.4** Completar type hints en `src/tools/mcp_tools.py`
- [ ] **06.5** Agregar module docstring a `src/sandbox/__init__.py`
- [ ] **06.6** Agregar docstrings a fixtures en `tests/conftest.py`
- [ ] **06.7** Agregar docstrings a `tests/test_execution_tool.py`
- [ ] **06.8** Agregar docstrings a `tests/test_local_sandbox.py`
- [ ] **06.9** Agregar docstrings a `tests/test_factory.py`
- [ ] **06.10** Verificar con mypy (opcional)

---

## Verificación (Acceptance Criteria)

```bash
# 1. Sin errores de tipo en archivos modificados
python -m py_compile src/memory.py src/sandbox/*.py src/skills/research/tools.py

# 2. Docstrings presentes
python -c "from src.sandbox import create_sandbox; print(create_sandbox.__doc__)"

# 3. Tests siguen pasando
pytest tests/ -v
```

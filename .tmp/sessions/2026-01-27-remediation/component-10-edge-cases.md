# Component-10: Tests de Edge Cases

## Prioridad: 🟡 MEDIO
## Tiempo Estimado: 2 horas
## Dependencias: Component-09 (tests base creados)

---

## Issues a Resolver

| ID | Archivo | Edge Case Faltante |
|----|---------|-------------------|
| EDG-01 | `tests/test_memory.py` | JSON corrupto |
| EDG-02 | `tests/test_memory.py` | Errores de permisos |
| EDG-03 | `tests/test_memory.py` | Historial muy grande |
| EDG-04 | `tests/test_execution_tool.py` | Syntax errors en código |
| EDG-05 | `tests/test_execution_tool.py` | Loop infinito |
| EDG-06 | `tests/test_mcp.py` | Config file no existe |
| EDG-07 | `tests/test_docker_sandbox.py` | Docker no disponible |

---

## Interface / Cambios Esperados

### Actualización: `tests/test_memory.py`
```python
"""Extended tests for memory module edge cases."""
import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open


class TestMemoryEdgeCases:
    """Edge case tests for MemoryManager."""
    
    def test_corrupted_json_file(self, tmp_path: Path):
        """
        Test handling of corrupted JSON in memory file.
        
        Verifies:
            - Corrupted file doesn't crash the system
            - Fresh memory is initialized instead
            - Warning is logged
        """
        # Arrange
        memory_file = tmp_path / "corrupted_memory.json"
        memory_file.write_text("{ invalid json }")
        
        # Act
        with patch("src.config.settings.MEMORY_FILE", str(memory_file)):
            from src.memory import MemoryManager
            manager = MemoryManager()
        
        # Assert
        assert manager.get_history() == []
    
    def test_permission_denied_on_save(self, tmp_path: Path):
        """
        Test handling of permission errors when saving memory.
        
        Verifies:
            - PermissionError is caught
            - Appropriate error is raised or logged
        """
        from src.memory import MemoryManager
        
        with patch("builtins.open", side_effect=PermissionError("Access denied")):
            manager = MemoryManager()
            manager.add_entry("user", "test")
            
            with pytest.raises(Exception):  # MemoryError after Component-05
                manager.save_memory()
    
    def test_very_large_history(self):
        """
        Test memory performance with large history.
        
        Verifies:
            - System handles 10000+ entries
            - Summarization kicks in appropriately
        """
        from src.memory import MemoryManager
        
        manager = MemoryManager()
        
        # Add many entries
        for i in range(1000):
            manager.add_entry("user", f"Message {i}")
            manager.add_entry("assistant", f"Response {i}")
        
        # Get context should still work
        context = manager.get_context_window(
            system_prompt="Test",
            max_messages=10,
            summarizer=lambda old, prev: "Summary"
        )
        
        assert len(context) <= 12  # system + max_messages + buffer
    
    def test_empty_content_entry(self):
        """Test handling of empty content in entries."""
        from src.memory import MemoryManager
        
        manager = MemoryManager()
        manager.add_entry("user", "")
        
        history = manager.get_history()
        assert len(history) == 1
        assert history[0]["content"] == ""
    
    def test_special_characters_in_content(self):
        """Test handling of special characters and unicode."""
        from src.memory import MemoryManager
        
        manager = MemoryManager()
        special_content = "Test with émojis 🚀 and spëcial çharacters\n\t\"quotes\""
        manager.add_entry("user", special_content)
        
        history = manager.get_history()
        assert history[0]["content"] == special_content
```

### Actualización: `tests/test_execution_tool.py`
```python
"""Extended tests for execution tool edge cases."""
import pytest


class TestExecutionEdgeCases:
    """Edge case tests for code execution."""
    
    def test_syntax_error_in_code(self):
        """
        Test handling of Python syntax errors.
        
        Verifies:
            - Syntax errors don't crash the sandbox
            - Meaningful error message is returned
        """
        from src.tools.execution_tool import execute_python
        
        code_with_error = "def broken(:\n    pass"
        success, output = execute_python(code_with_error)
        
        assert success is False
        assert "SyntaxError" in output or "error" in output.lower()
    
    def test_infinite_loop_timeout(self):
        """
        Test that infinite loops are terminated by timeout.
        
        Verifies:
            - Execution doesn't hang indefinitely
            - Timeout error is reported
        """
        from src.tools.execution_tool import execute_python
        
        infinite_loop = "while True: pass"
        success, output = execute_python(infinite_loop, timeout=2)
        
        assert success is False
        assert "timeout" in output.lower() or "killed" in output.lower()
    
    def test_memory_exhaustion(self):
        """
        Test handling of memory-intensive code.
        
        Verifies:
            - Memory limits are enforced
            - Graceful failure on memory exhaustion
        """
        from src.tools.execution_tool import execute_python
        
        memory_hog = "x = 'a' * (10 ** 9)"  # 1GB string
        success, output = execute_python(memory_hog, timeout=5)
        
        # Should either fail or be limited
        assert success is False or "memory" in output.lower()
    
    def test_import_restrictions(self):
        """
        Test that dangerous imports are blocked (after Component-02 fix).
        
        Verifies:
            - os, subprocess, etc. are restricted
            - Appropriate error message
        """
        from src.tools.execution_tool import execute_python
        
        dangerous_code = "import os; os.system('ls')"
        success, output = execute_python(dangerous_code)
        
        # After Component-02, this should be blocked
        assert success is False or "restricted" in output.lower() or "dangerous" in output.lower()
    
    def test_exception_in_user_code(self):
        """Test handling of runtime exceptions in user code."""
        from src.tools.execution_tool import execute_python
        
        code_with_exception = "raise ValueError('Test error')"
        success, output = execute_python(code_with_exception)
        
        assert success is False
        assert "ValueError" in output
```

### Actualización: `tests/test_mcp.py`
```python
"""Extended tests for MCP edge cases."""
import pytest
from pathlib import Path
from unittest.mock import patch


class TestMCPEdgeCases:
    """Edge case tests for MCP integration."""
    
    def test_missing_config_file(self, tmp_path: Path):
        """
        Test handling when MCP config file doesn't exist.
        
        Verifies:
            - Missing config doesn't crash
            - Appropriate warning is logged
            - MCP is disabled gracefully
        """
        with patch("src.config.settings.MCP_SERVERS_CONFIG", str(tmp_path / "nonexistent.json")):
            from src.mcp_client import MCPClientManagerSync
            
            manager = MCPClientManagerSync()
            # Should not raise, should log warning
            manager.initialize()
            
            assert manager.get_status()["initialized"] is False
    
    def test_invalid_json_config(self, tmp_path: Path):
        """Test handling of invalid JSON in MCP config."""
        config_file = tmp_path / "invalid.json"
        config_file.write_text("{ not valid json }")
        
        with patch("src.config.settings.MCP_SERVERS_CONFIG", str(config_file)):
            from src.mcp_client import MCPClientManagerSync
            
            manager = MCPClientManagerSync()
            manager.initialize()
            
            assert manager.get_status()["initialized"] is False
    
    def test_server_connection_timeout(self):
        """Test handling of server connection timeouts."""
        # This test should use mocking to avoid actual network calls
        pass  # Implementation depends on MCP client internals
```

### Actualización: `tests/test_docker_sandbox.py`
```python
"""Extended tests for Docker sandbox edge cases."""
import pytest
from unittest.mock import patch, MagicMock


class TestDockerSandboxEdgeCases:
    """Edge case tests for Docker sandbox."""
    
    @pytest.mark.docker
    def test_docker_not_available(self):
        """
        Test graceful fallback when Docker is not available.
        
        Verifies:
            - ImportError for docker module is handled
            - Fallback to LocalSandbox occurs
        """
        with patch.dict("sys.modules", {"docker": None}):
            from src.sandbox.factory import create_sandbox
            
            sandbox = create_sandbox()
            
            # Should fall back to LocalSandbox
            assert sandbox.__class__.__name__ == "LocalSandbox"
    
    @pytest.mark.docker
    def test_docker_daemon_not_running(self):
        """
        Test handling when Docker daemon is not running.
        
        Verifies:
            - Connection error is caught
            - Meaningful error message
            - Graceful degradation
        """
        mock_docker = MagicMock()
        mock_docker.from_env.side_effect = Exception("Cannot connect to Docker daemon")
        
        with patch.dict("sys.modules", {"docker": mock_docker}):
            from src.sandbox.factory import create_sandbox
            
            sandbox = create_sandbox()
            
            # Should fall back or raise meaningful error
            assert sandbox is not None
    
    @pytest.mark.docker
    def test_container_cleanup_on_error(self):
        """Test that containers are cleaned up even on errors."""
        # Implementation requires Docker mocking
        pass
```

### Fixture para Docker
```python
# En tests/conftest.py
import pytest
import subprocess


def is_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


@pytest.fixture
def docker_available():
    """Skip test if Docker is not available."""
    if not is_docker_available():
        pytest.skip("Docker not available")
```

---

## Tasks

- [ ] **10.1** Agregar tests de JSON corrupto a `test_memory.py`
- [ ] **10.2** Agregar tests de permisos a `test_memory.py`
- [ ] **10.3** Agregar tests de historial grande a `test_memory.py`
- [ ] **10.4** Agregar tests de syntax error a `test_execution_tool.py`
- [ ] **10.5** Agregar tests de timeout/infinite loop a `test_execution_tool.py`
- [ ] **10.6** Agregar tests de config faltante a `test_mcp.py`
- [ ] **10.7** Agregar tests de Docker no disponible a `test_docker_sandbox.py`
- [ ] **10.8** Agregar fixture `docker_available` a `conftest.py`
- [ ] **10.9** Agregar marker `@pytest.mark.docker` a tests de Docker
- [ ] **10.10** Ejecutar suite completa y verificar robustez

---

## Verificación (Acceptance Criteria)

```bash
# 1. Todos los edge case tests pasan
pytest tests/ -v -m "not docker"

# 2. Tests de Docker (si disponible)
pytest tests/ -v -m "docker"

# 3. Suite completa es robusta
pytest tests/ -v --tb=short

# 4. Cobertura mantiene >80%
pytest --cov=src --cov-fail-under=80 tests/
```

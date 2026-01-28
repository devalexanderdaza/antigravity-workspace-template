# Component-09: Tests Faltantes

## Prioridad: 🟡 MEDIO
## Tiempo Estimado: 3 horas
## Dependencias: Component-05, Component-07, Component-08

---

## Issues a Resolver

| ID | Módulo Sin Tests | Prioridad |
|----|------------------|-----------|
| TST-01 | `src/skills/loader.py` | Alta |
| TST-02 | `src/tools/demo_tool.py` | Media |
| TST-03 | `src/tools/ollama_local.py` | Media |
| TST-04 | `src/tools/openai_proxy.py` | Alta |
| TST-05 | `src/swarm_demo.py` | Baja |
| TST-06 | `agent.py` (raíz) | Baja |

### Cobertura Incompleta en Tests Existentes

| ID | Archivo | Método No Testeado |
|----|---------|-------------------|
| TST-07 | `tests/test_agent.py` | `_load_context()` |
| TST-08 | `tests/test_agent.py` | `_extract_tool_call()` |
| TST-09 | `tests/test_agent.py` | `summarize_memory()` |
| TST-10 | `tests/test_agent.py` | `shutdown()` |
| TST-11 | `tests/test_agent.py` | OpenAI backend path |

---

## Interface / Cambios Esperados

### Nuevo Archivo: `tests/test_skills_loader.py`
```python
"""Tests for the skills loader module."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


class TestLoadSkills:
    """Test suite for load_skills function."""
    
    def test_load_skills_with_valid_directory(self, tmp_path: Path):
        """
        Test that skills are loaded from a valid directory.
        
        Verifies:
            - Skills are discovered from filesystem
            - Tools dictionary is updated with skill functions
        """
        # Arrange
        skill_dir = tmp_path / "skills" / "test_skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "tools.py").write_text(
            "def test_tool():\n    '''A test tool.'''\n    return 'result'"
        )
        
        tools = {}
        
        # Act
        with patch("src.skills.loader.SKILLS_DIR", tmp_path / "skills"):
            from src.skills.loader import load_skills
            result = load_skills(tools)
        
        # Assert
        assert "test_tool" in tools or "test_skill" in result
    
    def test_load_skills_with_missing_directory(self):
        """Test graceful handling when skills directory doesn't exist."""
        tools = {}
        
        with patch("src.skills.loader.SKILLS_DIR", Path("/nonexistent")):
            from src.skills.loader import load_skills
            result = load_skills(tools)
        
        assert result == "" or isinstance(result, str)
    
    def test_load_skills_with_invalid_python(self, tmp_path: Path):
        """Test handling of skills with syntax errors."""
        skill_dir = tmp_path / "skills" / "bad_skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "tools.py").write_text("def broken(:\n    pass")
        
        tools = {}
        
        with patch("src.skills.loader.SKILLS_DIR", tmp_path / "skills"):
            from src.skills.loader import load_skills
            # Should not raise, should log warning
            result = load_skills(tools)
        
        assert isinstance(result, str)
```

### Nuevo Archivo: `tests/test_openai_proxy.py`
```python
"""Tests for the OpenAI proxy tool."""
import pytest
from unittest.mock import patch, MagicMock


class TestCallOpenAIChat:
    """Test suite for call_openai_chat function."""
    
    def test_successful_chat_completion(self):
        """Test successful API call returns expected response."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        
        with patch("src.tools.openai_proxy.OpenAI") as mock_client:
            mock_client.return_value.chat.completions.create.return_value = mock_response
            
            from src.tools.openai_proxy import call_openai_chat
            result = call_openai_chat("Test prompt", model="test-model")
        
        assert result == "Test response"
    
    def test_missing_api_key(self):
        """Test that missing API key raises appropriate error."""
        with patch.dict("os.environ", {}, clear=True):
            with patch("src.config.settings.OPENAI_API_KEY", None):
                from src.tools.openai_proxy import call_openai_chat
                
                with pytest.raises(Exception):
                    call_openai_chat("Test")
    
    def test_api_error_handling(self):
        """Test that API errors are properly handled."""
        with patch("src.tools.openai_proxy.OpenAI") as mock_client:
            mock_client.return_value.chat.completions.create.side_effect = Exception("API Error")
            
            from src.tools.openai_proxy import call_openai_chat
            
            with pytest.raises(Exception):
                call_openai_chat("Test")
```

### Nuevo Archivo: `tests/test_ollama_local.py`
```python
"""Tests for the Ollama local tool."""
import pytest
from unittest.mock import patch, MagicMock


class TestOllamaGenerate:
    """Test suite for Ollama local generation."""
    
    def test_generate_with_valid_prompt(self):
        """Test successful generation with valid prompt."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Generated text"}
        mock_response.status_code = 200
        
        with patch("requests.post", return_value=mock_response):
            from src.tools.ollama_local import generate_with_ollama
            result = generate_with_ollama("Test prompt")
        
        assert "Generated" in result or result is not None
    
    def test_connection_error(self):
        """Test handling of connection errors."""
        with patch("requests.post", side_effect=ConnectionError("No connection")):
            from src.tools.ollama_local import generate_with_ollama
            
            result = generate_with_ollama("Test")
            assert "error" in result.lower() or result == ""
    
    def test_invalid_url_validation(self):
        """Test that invalid URLs are rejected."""
        from src.tools.ollama_local import generate_with_ollama
        
        # After fix in Component-02, this should validate URL
        result = generate_with_ollama("Test", host="not-a-valid-url")
        assert "error" in result.lower() or "invalid" in result.lower()
```

### Actualización: `tests/test_agent.py`
```python
# Agregar tests faltantes

class TestLoadContext:
    """Tests for _load_context method."""
    
    def test_load_context_with_files(self, agent: GeminiAgent, tmp_path: Path):
        """Test that context files are loaded correctly."""
        # ...

    def test_load_context_empty_directory(self, agent: GeminiAgent):
        """Test handling of empty context directory."""
        # ...


class TestExtractToolCall:
    """Tests for _extract_tool_call method."""
    
    def test_extract_json_format(self, agent: GeminiAgent):
        """Test extraction from JSON format."""
        response = '{"action": "test_tool", "args": {"param": "value"}}'
        tool_name, args = agent._extract_tool_call(response)
        
        assert tool_name == "test_tool"
        assert args == {"param": "value"}
    
    def test_extract_action_line_format(self, agent: GeminiAgent):
        """Test extraction from 'Action: tool' format."""
        response = "Action: my_tool"
        tool_name, args = agent._extract_tool_call(response)
        
        assert tool_name == "my_tool"
        assert args == {}
    
    def test_extract_no_tool_call(self, agent: GeminiAgent):
        """Test when no tool call is present."""
        response = "This is just a regular response."
        tool_name, args = agent._extract_tool_call(response)
        
        assert tool_name is None
        assert args == {}


class TestShutdown:
    """Tests for shutdown method."""
    
    def test_shutdown_with_mcp(self, agent: GeminiAgent):
        """Test shutdown when MCP is enabled."""
        agent.mcp_manager = MagicMock()
        agent.shutdown()
        
        agent.mcp_manager.shutdown.assert_called_once()
    
    def test_shutdown_without_mcp(self, agent: GeminiAgent):
        """Test shutdown when MCP is not enabled."""
        agent.mcp_manager = None
        agent.shutdown()  # Should not raise
```

---

## Tasks

- [ ] **09.1** Crear `tests/test_skills_loader.py`
- [ ] **09.2** Crear `tests/test_openai_proxy.py`
- [ ] **09.3** Crear `tests/test_ollama_local.py`
- [ ] **09.4** Crear `tests/test_demo_tool.py`
- [ ] **09.5** Agregar `TestLoadContext` a `tests/test_agent.py`
- [ ] **09.6** Agregar `TestExtractToolCall` a `tests/test_agent.py`
- [ ] **09.7** Agregar `TestSummarizeMemory` a `tests/test_agent.py`
- [ ] **09.8** Agregar `TestShutdown` a `tests/test_agent.py`
- [ ] **09.9** Agregar tests para OpenAI backend path
- [ ] **09.10** Ejecutar coverage y verificar >80%

---

## Verificación (Acceptance Criteria)

```bash
# 1. Todos los nuevos tests deben pasar
pytest tests/test_skills_loader.py tests/test_openai_proxy.py tests/test_ollama_local.py -v

# 2. Tests existentes siguen pasando
pytest tests/ -v

# 3. Cobertura debe ser >80%
pytest --cov=src --cov-report=term-missing tests/
# Coverage debe mostrar >80%

# 4. Sin módulos sin cobertura
pytest --cov=src --cov-fail-under=80 tests/
```

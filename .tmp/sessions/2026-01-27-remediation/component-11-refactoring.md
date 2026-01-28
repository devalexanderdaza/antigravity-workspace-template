# Component-11: Refactorización de Métodos Grandes

## Prioridad: 🟢 BAJO
## Tiempo Estimado: 1.5 horas
## Dependencias: Component-07 (duplicados eliminados)

---

## Issues a Resolver

| ID | Issue | Archivo | Líneas | Tamaño |
|----|-------|---------|--------|--------|
| REF-01 | Método `act()` muy grande | `src/agent.py` | 389-467 | 78 líneas |
| REF-02 | Lógica duplicada en `_call_gemini` | `src/agent.py` | 267-299 | 32 líneas |
| REF-03 | Sin ABC para agents | `src/agents/base_agent.py` | - | - |
| REF-04 | `__all__` vacío/faltante | `src/__init__.py`, `src/agents/__init__.py`, `src/tools/__init__.py` | - | - |

---

## Interface / Cambios Esperados

### Refactorización: `src/agent.py` - Método `act()`

```python
# ANTES: act() hace todo (78 líneas)
def act(self, task: str) -> str:
    # Record input
    # Think
    # Build prompt
    # Call API
    # Extract tool
    # Execute tool
    # Call API again
    # Return

# DESPUÉS: Separado en métodos pequeños (<50 líneas cada uno)

def act(self, task: str) -> str:
    """
    Execute the task using available tools and generate a response.
    
    This is the main execution method following the Think-Act-Reflect loop.
    
    Args:
        task: The user's task or question.
        
    Returns:
        The agent's response after processing.
    """
    self.memory.add_entry("user", task)
    
    thought_process = self._think_and_plan(task)
    context = self._build_execution_context(thought_process)
    
    initial_response = self._generate_initial_response(task, context)
    tool_result = self._execute_tool_if_needed(initial_response)
    
    final_response = self._generate_final_response(
        task, context, tool_result
    )
    
    self.memory.add_entry("assistant", final_response)
    return final_response


def _think_and_plan(self, task: str) -> str:
    """
    Generate thought process and plan for the task.
    
    Args:
        task: The user's task.
        
    Returns:
        Thought process string from the thinking phase.
    """
    thought_process = self.think(task)
    self.memory.add_entry("assistant", f"Thinking Process:\n{thought_process}")
    return thought_process


def _build_execution_context(self, thought_process: str) -> str:
    """
    Build the system prompt and context for execution.
    
    Args:
        thought_process: The planning output.
        
    Returns:
        Formatted system prompt with tool descriptions.
    """
    tool_list = self._get_tool_descriptions()
    return (
        "You are an expert AI agent following the Think-Act-Reflect loop.\n"
        f"You have access to the following tools:\n{tool_list}\n\n"
        f"Relevant Context/Plan:\n{thought_process}\n\n"
        "If you need a tool, respond ONLY with a JSON object using the schema:\n"
        '{"action": "<tool_name>", "args": {"param": "value"}}\n'
        "If no tool is needed, reply directly with the final answer."
    )


def _generate_initial_response(
    self, 
    task: str, 
    system_prompt: str
) -> str:
    """
    Generate the initial response from the LLM.
    
    Args:
        task: The user's task.
        system_prompt: The system context.
        
    Returns:
        Raw response from the LLM.
    """
    context_messages = self.memory.get_context_window(
        system_prompt=system_prompt,
        max_messages=self.settings.MAX_CONTEXT_MESSAGES,
        summarizer=self.summarize_memory,
    )
    formatted = self._format_context_messages(context_messages)
    prompt = f"{formatted}\n\nCurrent Task: {task}"
    
    logger.debug("Sending request to LLM")
    return self._call_gemini(prompt)


def _execute_tool_if_needed(
    self, 
    response: str
) -> Optional[ToolResult]:
    """
    Check if response requests a tool and execute it.
    
    Args:
        response: The LLM's response.
        
    Returns:
        ToolResult if a tool was executed, None otherwise.
    """
    tool_name, tool_args = self._extract_tool_call(response)
    
    if not tool_name:
        return None
    
    return self._execute_tool(tool_name, tool_args, response)


def _execute_tool(
    self,
    tool_name: str,
    tool_args: Dict[str, Any],
    original_response: str
) -> ToolResult:
    """
    Execute a specific tool with given arguments.
    
    Args:
        tool_name: Name of the tool to execute.
        tool_args: Arguments for the tool.
        original_response: The response that triggered the tool.
        
    Returns:
        ToolResult with execution outcome.
    """
    tool_fn = self.available_tools.get(tool_name)
    
    if not tool_fn:
        observation = f"Requested tool '{tool_name}' is not registered."
    else:
        try:
            observation = tool_fn(**tool_args)
        except TypeError as e:
            observation = f"Error executing tool '{tool_name}': {e}"
        except Exception as e:
            observation = f"Unexpected error in tool '{tool_name}': {e}"
    
    self.memory.add_entry("assistant", original_response)
    self.memory.add_entry("tool", f"{tool_name} output: {observation}")
    
    return ToolResult(name=tool_name, observation=observation)
```

### Refactorización: `src/agents/base_agent.py`

```python
"""
Base agent module providing abstract base class for all agents.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.clients import DummyClient, is_test_environment
from src.logging_config import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all Antigravity agents.
    
    Provides common functionality and enforces interface contract
    for agent implementations.
    """
    
    def __init__(self, name: str = "BaseAgent"):
        """
        Initialize the base agent.
        
        Args:
            name: Display name for the agent.
        """
        self.name = name
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on environment."""
        if is_test_environment():
            logger.debug("Using DummyClient for testing")
            return DummyClient()
        return self._create_production_client()
    
    @abstractmethod
    def _create_production_client(self):
        """Create the production LLM client. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def execute(self, task: str) -> str:
        """
        Execute a task. Must be implemented by subclasses.
        
        Args:
            task: The task to execute.
            
        Returns:
            The result of task execution.
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary with agent status information.
        """
        return {
            "name": self.name,
            "client_type": self.client.__class__.__name__,
        }
```

### Actualización: `src/__init__.py`
```python
"""
Antigravity Workspace - Zero-Config AI Agent Framework.

This package provides tools for building autonomous AI agents
powered by Google Gemini and the Antigravity platform.
"""
from src.agent import GeminiAgent
from src.memory import MemoryManager
from src.config import settings

__all__ = [
    "GeminiAgent",
    "MemoryManager",
    "settings",
]

__version__ = "0.1.0"
```

### Actualización: `src/agents/__init__.py`
```python
"""
Specialist agents for the Antigravity swarm system.

This module provides specialized agents for different tasks:
- RouterAgent: Task routing and orchestration
- CoderAgent: Code generation and modification
- ResearcherAgent: Information gathering
- ReviewerAgent: Code review and quality assurance
"""
from src.agents.base_agent import BaseAgent
from src.agents.router_agent import RouterAgent
from src.agents.coder_agent import CoderAgent
from src.agents.researcher_agent import ResearcherAgent
from src.agents.reviewer_agent import ReviewerAgent

__all__ = [
    "BaseAgent",
    "RouterAgent",
    "CoderAgent",
    "ResearcherAgent",
    "ReviewerAgent",
]
```

---

## Tasks

- [ ] **11.1** Extraer `_think_and_plan()` de `act()`
- [ ] **11.2** Extraer `_build_execution_context()` de `act()`
- [ ] **11.3** Extraer `_generate_initial_response()` de `act()`
- [ ] **11.4** Extraer `_execute_tool_if_needed()` de `act()`
- [ ] **11.5** Extraer `_execute_tool()` de `act()`
- [ ] **11.6** Crear dataclass `ToolResult` para retorno estructurado
- [ ] **11.7** Convertir `BaseAgent` a ABC con métodos abstractos
- [ ] **11.8** Actualizar subclases para implementar métodos abstractos
- [ ] **11.9** Agregar `__all__` a `src/__init__.py`
- [ ] **11.10** Agregar `__all__` a `src/agents/__init__.py`
- [ ] **11.11** Agregar `__all__` a `src/tools/__init__.py`
- [ ] **11.12** Verificar que todos los tests pasen

---

## Verificación (Acceptance Criteria)

```bash
# 1. Método act() debe ser <50 líneas
wc -l < <(sed -n '/def act/,/^    def /p' src/agent.py)
# Debe ser <50

# 2. Nuevos métodos deben ser <50 líneas cada uno
# Verificación manual

# 3. BaseAgent debe ser ABC
python -c "from src.agents.base_agent import BaseAgent; from abc import ABC; print(issubclass(BaseAgent, ABC))"
# Debe ser True

# 4. __all__ debe estar definido
python -c "from src import __all__; print(__all__)"
# Debe mostrar lista de exports

# 5. Tests pasan
pytest tests/ -v
```

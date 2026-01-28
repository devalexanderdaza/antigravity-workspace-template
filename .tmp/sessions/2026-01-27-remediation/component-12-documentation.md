# Component-12: Mejoras de Documentación

## Prioridad: 🟢 BAJO
## Tiempo Estimado: 1 hora
## Dependencias: Ninguna (puede ejecutarse en paralelo)

---

## Issues a Resolver

| ID | Issue | Archivo | Descripción |
|----|-------|---------|-------------|
| DOC-06 | `.env.example` incompleto | `.env.example` | Variables MCP faltantes |
| DOC-07 | Comentario engañoso | `agent.py` (raíz) | "Example:" sin ejemplo |
| DOC-08 | Documentación inconsistente | `AGENTS.md`, `Dockerfile` | Entry point diferente |
| DOC-09 | Sleep hardcodeado | `src/skills/research/tools.py` | Documentar o configurar |

---

## Interface / Cambios Esperados

### Actualización: `.env.example`
```bash
# =============================================================================
# Antigravity Workspace Configuration
# =============================================================================
# Copy this file to .env and configure your settings.
# NEVER commit .env to version control!

# =============================================================================
# REQUIRED: Google Gemini API
# =============================================================================
# Get your API key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash

# =============================================================================
# OPTIONAL: OpenAI Compatible Backend (e.g., Ollama, LocalAI)
# =============================================================================
# Uncomment these to use an OpenAI-compatible API instead of Gemini
# OPENAI_API_KEY=your_openai_key_here
# OPENAI_BASE_URL=http://localhost:11434/v1
# OPENAI_MODEL=llama2

# =============================================================================
# OPTIONAL: MCP (Model Context Protocol) Configuration
# =============================================================================
# Enable MCP to connect external tools and services
MCP_ENABLED=false
MCP_SERVERS_CONFIG=./mcp_servers.json
MCP_CONNECTION_TIMEOUT=30
MCP_TOOL_PREFIX=mcp_

# =============================================================================
# OPTIONAL: Logging Configuration
# =============================================================================
# Available levels: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# =============================================================================
# OPTIONAL: Agent Configuration
# =============================================================================
AGENT_NAME=Antigravity Agent
MAX_CONTEXT_MESSAGES=10
WORKSPACE_DIR=./
```

### Actualización: `agent.py` (raíz)
```python
#!/usr/bin/env python3
"""
Antigravity Workspace - CLI Entry Point.

This script provides the command-line interface for running the Antigravity agent.

Usage:
    python agent.py "Your task here"
    python agent.py --help

Examples:
    # Simple query
    python agent.py "What is the capital of France?"
    
    # Code generation
    python agent.py "Write a Python function to calculate fibonacci numbers"
    
    # Research task
    python agent.py "Research the latest developments in AI agents"

Environment:
    Requires GOOGLE_API_KEY to be set in .env file or environment.
    See .env.example for all configuration options.
"""
import sys
import argparse

from src.agent import GeminiAgent


def main():
    """Main entry point for the Antigravity agent CLI."""
    parser = argparse.ArgumentParser(
        description="Antigravity Agent - Zero-Config AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="The task or question for the agent"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    
    if not args.task and not args.interactive:
        parser.print_help()
        sys.exit(1)
    
    agent = GeminiAgent()
    
    try:
        if args.interactive:
            run_interactive(agent)
        else:
            agent.run(args.task)
    finally:
        agent.shutdown()


def run_interactive(agent: GeminiAgent):
    """Run the agent in interactive mode."""
    print("🚀 Antigravity Agent - Interactive Mode")
    print("Type 'exit' or 'quit' to end the session.\n")
    
    while True:
        try:
            task = input("You: ").strip()
            if task.lower() in ("exit", "quit"):
                print("👋 Goodbye!")
                break
            if not task:
                continue
            agent.run(task)
            print()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
```

### Actualización: `Dockerfile`
```dockerfile
# ... existing content ...

# Entry point with proper documentation
# Run with: docker run antigravity-agent "Your task here"
# Or interactive: docker run -it antigravity-agent --interactive
CMD ["python", "agent.py", "--help"]
```

### Actualización: `AGENTS.md`
```markdown
## Run Agent

### Single Task
```bash
python agent.py "Your task here"
```

### Interactive Mode
```bash
python agent.py --interactive
```

### Docker
```bash
# Build
docker-compose build

# Run single task
docker-compose run agent python agent.py "Your task here"

# Run interactive
docker-compose run -it agent python agent.py --interactive
```
```

### Actualización: `src/skills/research/tools.py`
```python
"""
Research tools for deep information gathering.

These tools provide research capabilities with configurable
rate limiting to respect API quotas.
"""
import time
from typing import Optional

from src.config import settings
from src.logging_config import get_logger

logger = get_logger(__name__)

# Rate limiting configuration (seconds between requests)
RESEARCH_RATE_LIMIT = float(getattr(settings, 'RESEARCH_RATE_LIMIT', 1.0))


def deep_research(query: str, delay: Optional[float] = None) -> str:
    """
    Perform deep research on a given query.
    
    Args:
        query: The research question or topic.
        delay: Optional delay in seconds between API calls.
               Defaults to RESEARCH_RATE_LIMIT setting.
    
    Returns:
        Research findings as formatted string.
        
    Note:
        This function includes rate limiting to prevent API abuse.
        Configure RESEARCH_RATE_LIMIT in settings to adjust.
    """
    rate_limit = delay if delay is not None else RESEARCH_RATE_LIMIT
    
    if rate_limit > 0:
        logger.debug("Rate limiting: waiting %.1f seconds", rate_limit)
        time.sleep(rate_limit)
    
    # ... rest of implementation ...
```

---

## Tasks

- [ ] **12.1** Actualizar `.env.example` con todas las variables
- [ ] **12.2** Agregar secciones y comentarios descriptivos a `.env.example`
- [ ] **12.3** Reescribir docstring de `agent.py` (raíz) con ejemplos
- [ ] **12.4** Agregar argparse con `--help` y `--interactive`
- [ ] **12.5** Actualizar `Dockerfile` CMD con documentación
- [ ] **12.6** Alinear documentación en `AGENTS.md`
- [ ] **12.7** Hacer configurable el sleep en `research/tools.py`
- [ ] **12.8** Agregar docstring explicando rate limiting
- [ ] **12.9** Verificar que `--help` funcione correctamente

---

## Verificación (Acceptance Criteria)

```bash
# 1. .env.example debe tener todas las variables
grep "MCP_ENABLED" .env.example
grep "LOG_LEVEL" .env.example
# Ambos deben retornar líneas

# 2. Help debe funcionar
python agent.py --help
# Debe mostrar documentación completa

# 3. Interactive mode debe funcionar
echo "exit" | python agent.py --interactive
# Debe iniciar y salir limpiamente

# 4. Docker CMD debe mostrar help
docker build -t test .
docker run test
# Debe mostrar help
```

# Component-03: Sistema de Logging

## Prioridad: 🟠 ALTO
## Tiempo Estimado: 2 horas
## Dependencias: Component-01, Component-02

---

## Issues a Resolver

| ID | Issue | Archivo | Cantidad |
|----|-------|---------|----------|
| LOG-01 | Print statements en lugar de logging | `src/agent.py` | 15+ |
| LOG-02 | Print statements en lugar de logging | `src/tools/example_tool.py` | 4 |
| LOG-03 | Print statements en lugar de logging | `src/skills/loader.py` | 7 |
| LOG-04 | Print statements en lugar de logging | `src/mcp_client.py` | 10+ |

---

## Interface / Cambios Esperados

### Nuevo Archivo: `src/logging_config.py`
```python
"""
Centralized logging configuration for Antigravity Workspace.

This module provides a consistent logging setup across all components,
following the project's coding standards for observability.
"""
import logging
import sys
from typing import Optional

from src.config import settings


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return the root logger for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR). 
               Defaults to settings.LOG_LEVEL.
        format_string: Custom format string. Uses default if None.
        
    Returns:
        Configured root logger instance.
    """
    log_level = level or getattr(settings, 'LOG_LEVEL', 'INFO')
    
    default_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    )
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=format_string or default_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    return logging.getLogger("antigravity")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name for the logger, typically __name__.
        
    Returns:
        Logger instance configured for the module.
    """
    return logging.getLogger(f"antigravity.{name}")
```

### Actualización: `src/config.py`
```python
# Agregar a Settings class
LOG_LEVEL: str = "INFO"
```

### Patrón de Migración
```python
# ANTES (print)
print(f"🤖 Initializing {self.settings.AGENT_NAME}...")
print(f"⚠️ Failed to load: {e}")

# DESPUÉS (logging)
from src.logging_config import get_logger
logger = get_logger(__name__)

logger.info("Initializing %s with model %s", self.settings.AGENT_NAME, self.settings.GEMINI_MODEL_NAME)
logger.warning("Failed to load: %s", e)
```

---

## Mapeo de Print → Logging

| Símbolo | Nivel de Log |
|---------|--------------|
| 🤖 🚀 📦 ✓ | `logger.info()` |
| ⚠️ | `logger.warning()` |
| ❌ | `logger.error()` |
| 🔌 💬 🔄 | `logger.debug()` |

---

## Tasks

- [ ] **03.1** Crear `src/logging_config.py` con setup centralizado
- [ ] **03.2** Agregar `LOG_LEVEL` a `src/config.py`
- [ ] **03.3** Migrar prints en `src/agent.py` a logging
- [ ] **03.4** Migrar prints en `src/tools/example_tool.py` a logging
- [ ] **03.5** Migrar prints en `src/skills/loader.py` a logging
- [ ] **03.6** Migrar prints en `src/mcp_client.py` a logging
- [ ] **03.7** Migrar prints en archivos restantes
- [ ] **03.8** Agregar test para logging_config
- [ ] **03.9** Actualizar `.env.example` con `LOG_LEVEL`

---

## Verificación (Acceptance Criteria)

```bash
# 1. No deben quedar print statements (excepto en tools que lo necesiten)
grep -rn "print(" src/ --include="*.py" | grep -v "logging_config" | wc -l
# Debe ser 0 o cercano a 0

# 2. Logging debe funcionar
python -c "from src.logging_config import setup_logging, get_logger; setup_logging(); get_logger('test').info('Test')"
# Debe mostrar log formateado

# 3. Tests deben pasar
pytest tests/ -v
```

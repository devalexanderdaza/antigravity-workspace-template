# Component-02: Seguridad de Runtime

## Prioridad: 🔴 CRÍTICO
## Tiempo Estimado: 45 minutos
## Dependencias: Ninguna (paralelo con Component-01)

---

## Issues a Resolver

| ID | Issue | Archivo | Línea |
|----|-------|---------|-------|
| SEC-04 | Dockerfile ejecuta como root | `Dockerfile` | - |
| SEC-05 | Sin sanitización de input para ejecución de código | `src/tools/execution_tool.py` | - |
| SEC-06 | Sin validación de email en send_email | `src/tools/example_tool.py` | 139-155 |
| SEC-07 | Sin validación de URL en ollama_local | `src/tools/ollama_local.py` | 7-50 |

---

## Interface / Cambios Esperados

### Archivo: `Dockerfile`
```dockerfile
# Agregar después de COPY
RUN useradd --create-home --shell /bin/bash agent
USER agent
WORKDIR /home/agent/app
```

### Archivo: `src/tools/execution_tool.py`
```python
# Agregar función de validación
DANGEROUS_PATTERNS = [
    r'\bimport\s+os\b',
    r'\bimport\s+subprocess\b',
    r'\bopen\s*\(',
    r'\beval\s*\(',
    r'\bexec\s*\(',
    r'__import__',
    r'\bsystem\s*\(',
]

def validate_code_safety(code: str) -> tuple[bool, str]:
    """
    Validate code for potentially dangerous patterns.
    
    Args:
        code: Python code string to validate.
        
    Returns:
        Tuple of (is_safe, reason).
    """
    import re
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return False, f"Potentially dangerous pattern detected: {pattern}"
    return True, ""
```

### Archivo: `src/tools/example_tool.py`
```python
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### Archivo: `src/tools/ollama_local.py`
```python
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """Validate URL format and scheme."""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False
```

---

## Tasks

- [ ] **02.1** Agregar usuario non-root a `Dockerfile`
- [ ] **02.2** Crear función `validate_code_safety()` en `execution_tool.py`
- [ ] **02.3** Integrar validación antes de ejecutar código
- [ ] **02.4** Crear función `validate_email()` en `example_tool.py`
- [ ] **02.5** Integrar validación en función `send_email()`
- [ ] **02.6** Crear función `validate_url()` en `ollama_local.py`
- [ ] **02.7** Integrar validación en funciones que usen URLs
- [ ] **02.8** Agregar tests para funciones de validación

---

## Verificación (Acceptance Criteria)

```bash
# 1. Dockerfile debe tener USER directive
grep "^USER " Dockerfile  # Debe retornar "USER agent"

# 2. Tests de validación deben pasar
pytest tests/test_execution_tool.py -v -k "validation"

# 3. Build de Docker debe funcionar
docker build -t antigravity-test .
```

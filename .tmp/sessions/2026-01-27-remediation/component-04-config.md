# Component-04: Configuración Consistente

## Prioridad: 🟠 ALTO
## Tiempo Estimado: 1.5 horas
## Dependencias: Ninguna (paralelo con Component-03)

---

## Issues a Resolver

| ID | Issue | Archivo | Descripción |
|----|-------|---------|-------------|
| CFG-01 | Path inconsistente MCP config | `src/config.py:61-62` | Default `./data/mcp_servers.json`, real en raíz |
| CFG-02 | Path inconsistente memory file | `src/config.py:57`, `docker-compose.yml:12` | Mismatch entre config y Docker |
| CFG-03 | Directorio `data/` no existe | `src/config.py` | FileNotFoundError potencial |
| CFG-04 | docker-compose version deprecado | `docker-compose.yml:1` | `version: '3.8'` obsoleto |
| CFG-05 | GitHub Actions desactualizado | `.github/workflows/test.yml:14,16` | Usar v4/v5 |

---

## Interface / Cambios Esperados

### Archivo: `src/config.py`
```python
class Settings(BaseSettings):
    # ... existing fields ...
    
    # Memory Configuration
    MEMORY_FILE: str = "./agent_memory.json"  # Cambiar de ./data/
    
    # MCP Configuration  
    MCP_SERVERS_CONFIG: str = "./mcp_servers.json"  # Cambiar de ./data/
    
    # Workspace
    WORKSPACE_DIR: str = "./"
```

### Archivo: `docker-compose.yml`
```yaml
# Eliminar línea version (deprecado en Compose V2+)
services:
  agent:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - GEMINI_MODEL_NAME=${GEMINI_MODEL_NAME:-gemini-2.5-flash}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./agent_memory.json:/app/agent_memory.json
      - ./mcp_servers.json:/app/mcp_servers.json
    # ... rest ...
```

### Archivo: `.github/workflows/test.yml`
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4  # Actualizar de v3
      - name: Set up Python
        uses: actions/setup-python@v5  # Actualizar de v4
        with:
          python-version: '3.11'
```

### Archivo: `src/memory.py` (mejora)
```python
def _ensure_directory_exists(file_path: str) -> None:
    """Create parent directory if it doesn't exist."""
    from pathlib import Path
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
```

---

## Tasks

- [ ] **04.1** Actualizar `MEMORY_FILE` default en `src/config.py`
- [ ] **04.2** Actualizar `MCP_SERVERS_CONFIG` default en `src/config.py`
- [ ] **04.3** Agregar función `_ensure_directory_exists()` en `src/memory.py`
- [ ] **04.4** Llamar función antes de guardar memoria
- [ ] **04.5** Eliminar `version:` de `docker-compose.yml`
- [ ] **04.6** Alinear volúmenes en `docker-compose.yml`
- [ ] **04.7** Actualizar `actions/checkout` a `@v4`
- [ ] **04.8** Actualizar `actions/setup-python` a `@v5`
- [ ] **04.9** Actualizar tests que dependan de paths antiguos

---

## Verificación (Acceptance Criteria)

```bash
# 1. Config debe apuntar a archivos en raíz
python -c "from src.config import settings; print(settings.MCP_SERVERS_CONFIG)"
# Debe mostrar "./mcp_servers.json"

# 2. docker-compose debe ser válido
docker-compose config

# 3. GitHub workflow debe ser válido
# (Se verifica en PR/push)

# 4. Memory debe crear directorio si no existe
python -c "from src.memory import MemoryManager; m = MemoryManager()"
# No debe fallar
```

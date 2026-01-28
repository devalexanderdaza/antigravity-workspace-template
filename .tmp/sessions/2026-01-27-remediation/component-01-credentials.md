# Component-01: Credenciales y Secrets

## Prioridad: 🔴 CRÍTICO
## Tiempo Estimado: 30 minutos
## Dependencias: Ninguna (ejecutar primero)

---

## Issues a Resolver

| ID | Issue | Archivo | Línea |
|----|-------|---------|-------|
| SEC-01 | API Key hardcodeada expuesta | `.env` | 5 |
| SEC-02 | `.env` posiblemente en control de versiones | `.gitignore` | - |
| SEC-03 | Variables de entorno faltantes en `.env.example` | `.env.example` | - |

---

## Interface / Cambios Esperados

### Archivo: `.env` (ELIMINAR/LIMPIAR)
```bash
# Después del fix - SIN valores reales
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash
```

### Archivo: `.gitignore` (VERIFICAR/AGREGAR)
```gitignore
# Environment
.env
.env.local
.env.*.local
```

### Archivo: `.env.example` (COMPLETAR)
```bash
# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash

# OpenAI Compatible Backend (Optional)
# OPENAI_API_KEY=your_openai_key_here
# OPENAI_BASE_URL=http://localhost:11434/v1
# OPENAI_MODEL=llama2

# MCP Configuration (Optional)
MCP_ENABLED=false
MCP_SERVERS_CONFIG=./mcp_servers.json
MCP_CONNECTION_TIMEOUT=30
MCP_TOOL_PREFIX=mcp_
```

---

## Tasks

- [ ] **01.1** Verificar si `.env` está en `.gitignore`
- [ ] **01.2** Agregar `.env` a `.gitignore` si falta
- [ ] **01.3** Eliminar el valor real de API key de `.env`
- [ ] **01.4** Actualizar `.env.example` con todas las variables
- [ ] **01.5** Verificar historial de git para commits con secrets
- [ ] **01.6** Documentar proceso de rotación de API key en README

---

## Verificación (Acceptance Criteria)

```bash
# 1. .env no debe contener keys reales
grep -E "AIza[0-9A-Za-z_-]{35}" .env  # Debe retornar vacío

# 2. .gitignore debe tener .env
grep "^\.env$" .gitignore  # Debe retornar ".env"

# 3. .env.example debe tener todas las variables
grep "MCP_ENABLED" .env.example  # Debe retornar la línea
```

---

## Notas de Seguridad

⚠️ **ACCIÓN REQUERIDA FUERA DEL CÓDIGO:**
1. Ir a Google Cloud Console
2. Revocar/rotar la API key expuesta: `AIzaSyAoIDZ5p0ALVr-lzcSihQVpkWJmTuBdMNk`
3. Generar nueva API key
4. Actualizar sistemas que usen esta key

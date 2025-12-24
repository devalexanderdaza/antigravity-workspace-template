# 🪐 Plantilla Workspace de Google Antigravity

**Starter kit de nivel producción para agentes autónomos de IA en Google Antigravity.**

Idioma: [English](/docs/en/) | [中文](README_CN.md) | [Español](/docs/es/)

![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/AI-Gemini_2.0_Flash-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event_Driven-purple)
![Memory](https://img.shields.io/badge/Context-Infinite-orange)

## ⚡ Inicio Rápido

```bash
# 1. Clona la plantilla
git clone https://github.com/study8677/antigravity-workspace-template.git mi-proyecto
cd mi-proyecto

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Ejecuta el agente
python src/agent.py
```

**¡Eso es todo!** El IDE auto-carga la configuración via `.cursorrules` + `.antigravity/rules.md`. Estás listo para solicitar.

## 🎯 ¿Qué es Esto?

Esto **no** es otro wrapper de LangChain. Es un workspace mínimo y transparente para construir agentes de IA que:

- 🧠 Tengan memoria infinita (resumización recursiva)
- 🛠️ Auto-descubran herramientas desde `src/tools/`
- 📚 Auto-inyecten contexto desde `.context/`
- 🔌 Se conecten a servidores MCP sin problemas
- 🤖 Coordinen múltiples agentes especialistas
- 📦 Guarden outputs como artefactos (planes, logs, evidencia)

**Clonar → Renombrar → Solicitar. Ese es el flujo de trabajo.**

## 🚀 Características Principales

| Característica | Descripción |
|---|---|
| 🧠 **Memoria Infinita** | La resumización recursiva comprime contexto automáticamente |
| 🛠️ **Herramientas Universales** | Coloca funciones Python en `src/tools/` → auto-descubiertas |
| 📚 **Contexto Automático** | Agrega archivos a `.context/` → auto-inyectados en prompts |
| 🔌 **Soporte MCP** | Conecta GitHub, bases de datos, sistemas de archivos, servidores personalizados |
| 🤖 **Agentes Swarm** | Orquestación multi-agente con patrón Router-Worker |
| ⚡ **Nativo de Gemini** | Optimizado para Gemini 2.0 Flash |
| 🌐 **Agnóstico de LLM** | Usa OpenAI, Azure, Ollama o cualquier API compatible con OpenAI |
| 📂 **Artifact-First** | Cada tarea produce planes, logs y evidencia |

## 📚 Documentación

**Documentación completa disponible en `/docs/es/`:**

- **[Inicio Rápido](docs/es/QUICK_START.md)** — Instalación y despliegue
- **[Filosofía](docs/es/PHILOSOPHY.md)** — Conceptos centrales y arquitectura
- **[Zero-Config](docs/es/ZERO_CONFIG.md)** — Descubrimiento automático de herramientas y contexto
- **[Integración de MCP](docs/es/MCP_INTEGRATION.md)** — Conectividad de herramientas externas
- **[Protocolo de Swarm](docs/es/SWARM_PROTOCOL.md)** — Coordinación multi-agente
- **[Hoja de Ruta](docs/es/ROADMAP.md)** — Fases futuras y visión

## 🏗️ Estructura del Proyecto

```
src/
├── agent.py           # Bucle principal del agente
├── memory.py          # Gestor de memoria JSON
├── mcp_client.py      # Integración de MCP
├── swarm.py           # Orquestación multi-agente
├── agents/            # Agentes especialistas
└── tools/             # Tus herramientas personalizadas

.context/             # Base de conocimiento (auto-inyectada)
.antigravity/         # Reglas de Antigravity
artifacts/            # Outputs y evidencia
```

## 💡 Ejemplo: Construir una Herramienta en 30 Segundos

```python
# src/tools/mi_herramienta.py
def analyze_sentiment(text: str) -> str:
    """Analiza el sentimiento del texto dado."""
    return "positivo" if len(text) > 10 else "neutral"
```

**Reinicia el agente.** ¡Hecho! La herramienta está disponible.

## 🔌 Integración de MCP

Conecta a herramientas externas:

```json
{
  "servers": [
    {
      "name": "github",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "enabled": true
    }
  ]
}
```

El agente automáticamente descubre y usa todas las herramientas MCP.

## 🤖 Swarm Multi-Agente

Descompón tareas complejas:

```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()
result = swarm.execute("Construye y revisa una calculadora")
```

El swarm automáticamente:
- 📤 Enruta a agentes Coder, Reviewer, Researcher
- 🧩 Sintetiza resultados
- 📂 Guarda artefactos

## ✅ Qué Está Completado

- ✅ Fases 1-7: Foundation, DevOps, Memory, Tools, Swarm, Discovery
- ✅ Fase 8: Integración de MCP (totalmente implementada)
- 🚀 Fase 9: Enterprise Core (en progreso)

Ver [Hoja de Ruta](docs/es/ROADMAP.md) para detalles.

## 🤝 Contribuyendo

¡Las ideas también son contribuciones! Abre un [issue](https://github.com/study8677/antigravity-workspace-template/issues) para:
- Reportar bugs
- Sugerir características
- Proponer arquitectura (Fase 9)

O envía un PR para mejorar documentación o código.

## 👥 Contribuidores

- [@devalexanderdaza](https://github.com/devalexanderdaza) — Primer contribuidor. Implementó herramientas de demo, mejoró la funcionalidad del agente, propuso la hoja de ruta "Agent OS" y completó la integración MCP.
- [@Subham-KRLX](https://github.com/Subham-KRLX) — Añadió carga dinámica de herramientas y contexto (Fixes #4) y el protocolo de clúster multi‑agente (Fixes #6).

## ⭐ Star History

[![Gráfico de Estrellas](https://api.star-history.com/svg?repos=study8677/antigravity-workspace-template&type=Date)](https://star-history.com/#study8677/antigravity-workspace-template&Date)

## 📄 Licencia

Licencia MIT. Ver [LICENSE](LICENSE) para detalles.

---

**[Explorar Documentación Completa →](docs/es/)**


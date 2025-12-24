# 🪐 Google Antigravity Workspace Template

**Production-grade starter kit for autonomous AI agents on Google Antigravity.**

Language: [English](/docs/en/) | [中文](README_CN.md) | [Español](/docs/es/)

![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/AI-Gemini_2.0_Flash-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event_Driven-purple)
![Memory](https://img.shields.io/badge/Context-Infinite-orange)

## ⚡ Quick Start

```bash
# 1. Clone the template
git clone https://github.com/study8677/antigravity-workspace-template.git my-project
cd my-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the agent
python src/agent.py
```

**That's it!** The IDE auto-loads configuration via `.cursorrules` + `.antigravity/rules.md`. You're ready to prompt.

## 🎯 What Is This?

This is **not** another LangChain wrapper. It's a minimal, transparent workspace for building AI agents that:

- 🧠 Have infinite memory (recursive summarization)
- 🛠️ Auto-discover tools from `src/tools/`
- 📚 Auto-inject context from `.context/`
- 🔌 Connect to MCP servers seamlessly
- 🤖 Coordinate multiple specialist agents
- 📦 Save outputs as artifacts (plans, logs, evidence)

**Clone → Rename → Prompt. That's the workflow.**

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Infinite Memory** | Recursive summarization compresses context automatically |
| 🛠️ **Universal Tools** | Drop Python functions in `src/tools/` → auto-discovered |
| 📚 **Auto Context** | Add files to `.context/` → auto-injected into prompts |
| 🔌 **MCP Support** | Connect GitHub, databases, filesystems, custom servers |
| 🤖 **Swarm Agents** | Multi-agent orchestration with Router-Worker pattern |
| ⚡ **Gemini Native** | Optimized for Gemini 2.0 Flash |
| 🌐 **LLM Agnostic** | Use OpenAI, Azure, Ollama, or any OpenAI-compatible API |
| 📂 **Artifact-First** | Every task produces plans, logs, and evidence |

## 📚 Documentation

**Full documentation available in `/docs/en/`:**

- **[Quick Start](docs/en/QUICK_START.md)** — Installation & deployment
- **[Philosophy](docs/en/PHILOSOPHY.md)** — Core concepts & architecture
- **[Zero-Config](docs/en/ZERO_CONFIG.md)** — Auto tool & context loading
- **[MCP Integration](docs/en/MCP_INTEGRATION.md)** — External tool connectivity
- **[Swarm Protocol](docs/en/SWARM_PROTOCOL.md)** — Multi-agent coordination
- **[Roadmap](docs/en/ROADMAP.md)** — Future phases & vision

## 🏗️ Project Structure

```
src/
├── agent.py           # Main agent loop
├── memory.py          # JSON memory manager
├── mcp_client.py      # MCP integration
├── swarm.py           # Multi-agent orchestration
├── agents/            # Specialist agents
└── tools/             # Your custom tools

.context/             # Knowledge base (auto-injected)
.antigravity/         # Antigravity rules
artifacts/            # Outputs & evidence
```

## 💡 Example: Build a Tool in 30 Seconds

```python
# src/tools/my_tool.py
def analyze_sentiment(text: str) -> str:
    """Analyzes the sentiment of given text."""
    return "positive" if len(text) > 10 else "neutral"
```

**Restart agent.** Done! The tool is now available.

## 🔌 MCP Integration

Connect to external tools:

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

Agent automatically discovers and uses all MCP tools.

## 🤖 Multi-Agent Swarm

Decompose complex tasks:

```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()
result = swarm.execute("Build and review a calculator")
```

The swarm automatically:
- 📤 Routes to Coder, Reviewer, Researcher agents
- 🧩 Synthesizes results
- 📂 Saves artifacts

## ✅ What's Complete

- ✅ Phase 1-7: Foundation, DevOps, Memory, Tools, Swarm, Discovery
- ✅ Phase 8: MCP Integration (fully implemented)
- 🚀 Phase 9: Enterprise Core (in progress)

See [Roadmap](docs/en/ROADMAP.md) for details.

## 🤝 Contributing

Ideas are contributions too! Open an [issue](https://github.com/study8677/antigravity-workspace-template/issues) to:
- Report bugs
- Suggest features
- Propose architecture (Phase 9)

Or submit a PR to improve docs or code.

## 👥 Contributors

- [@devalexanderdaza](https://github.com/devalexanderdaza) — First contributor. Implemented demo tools, enhanced agent functionality, proposed the "Agent OS" roadmap, and completed MCP integration.
- [@Subham-KRLX](https://github.com/Subham-KRLX) — Added dynamic tools and context loading (Fixes #4) and the multi-agent cluster protocol (Fixes #6).

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=study8677/antigravity-workspace-template&type=Date)](https://star-history.com/#study8677/antigravity-workspace-template&Date)

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**[Explore Full Documentation →](docs/en/)**

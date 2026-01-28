# Component-08: Dependencias y Build

## Prioridad: 🟡 MEDIO
## Tiempo Estimado: 1.5 horas
## Dependencias: Component-04 (config actualizado)

---

## Issues a Resolver

| ID | Issue | Archivo | Descripción |
|----|-------|---------|-------------|
| DEP-01 | `pytest-cov` faltante | `requirements.txt` | Documentado en AGENTS.md pero no instalado |
| DEP-02 | `docker` SDK faltante | `requirements.txt` | Necesario para DockerSandbox |
| DEP-03 | Sin version pinning | `requirements.txt` | Riesgo de builds rotos |
| DEP-04 | `pyproject.toml` faltante | - | Estándar moderno de Python |
| DEP-05 | Sin configuración pytest | - | No hay pytest.ini ni [tool.pytest] |

---

## Interface / Cambios Esperados

### Nuevo Archivo: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "antigravity-workspace"
version = "0.1.0"
description = "Zero-Config AI Agent Workspace powered by Google Gemini"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Antigravity Team"}
]
keywords = ["ai", "agent", "gemini", "llm", "workspace"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "google-genai>=0.5.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    "requests>=2.31.0",
    "mcp[cli]>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]
docker = [
    "docker>=6.1.0",
]
all = [
    "antigravity-workspace[dev,docker]",
]

[project.urls]
Homepage = "https://github.com/your-org/antigravity-workspace"
Repository = "https://github.com/your-org/antigravity-workspace.git"
Issues = "https://github.com/your-org/antigravity-workspace/issues"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "docker: marks tests that require Docker",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "src/__init__.py",
    "src/tools/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
fail_under = 80
show_missing = true

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true

[tool.ruff]
target-version = "py310"
line-length = 88
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.isort]
known-first-party = ["src"]
```

### Actualización: `requirements.txt`
```txt
# Core Dependencies
google-genai>=0.5.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0

# MCP (Model Context Protocol) Integration
mcp[cli]>=1.0.0

# Optional: Docker SDK for container-based sandbox
docker>=6.1.0

# Development Dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0
```

---

## Tasks

- [ ] **08.1** Crear `pyproject.toml` con metadatos del proyecto
- [ ] **08.2** Agregar sección `[tool.pytest.ini_options]`
- [ ] **08.3** Agregar sección `[tool.coverage]`
- [ ] **08.4** Agregar sección `[tool.mypy]`
- [ ] **08.5** Agregar sección `[tool.ruff]` para linting
- [ ] **08.6** Actualizar `requirements.txt` con versiones pinneadas
- [ ] **08.7** Agregar `pytest-cov` a dependencias
- [ ] **08.8** Agregar `docker` SDK a dependencias (opcional)
- [ ] **08.9** Verificar instalación con `pip install -e .[dev]`
- [ ] **08.10** Actualizar CI para usar `pyproject.toml`

---

## Verificación (Acceptance Criteria)

```bash
# 1. pyproject.toml debe ser válido
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"

# 2. Instalación debe funcionar
pip install -e .[dev]

# 3. pytest debe leer config de pyproject.toml
pytest --collect-only

# 4. Coverage debe funcionar
pytest --cov=src tests/

# 5. mypy debe ejecutarse
mypy src/ --ignore-missing-imports
```

---
tags: [meta, portability, git]
aliases: [PORTABILITY, portable, repo]
---

# ¿Talaria es portable y se puede instalar en cualquier PC?

**Sí.** El corazón (Markdown + grafo AXON + memoria + CLI) viaja con el repo. Lo que no viaja son rutas absolutas de *esta* máquina y secretos.

## Instalación en máquina nueva

```bash
git clone https://github.com/Raikadier/talaria.git
cd talaria
```

| SO | Comando |
|----|---------|
| Windows | `powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1` |
| macOS/Linux | `./scripts/install.sh` |
| Cualquiera | `pip install -e . && python bootstrap.py` |

Luego:

1. Abrir la carpeta clonada como vault en Obsidian (opcional).
2. `talaria connect --client cursor|hermes|claude --json` y aplicar el snippet MCP.
3. Si corres fuera del clone: `TALARIA_VAULT=/ruta/al/clone`.

## Qué SÍ subir al repo

| Contenido | Portable |
|-----------|----------|
| `Home.md`, `AGENTS.md`, `README.md`, `LICENSE` | Sí |
| `src/talaria_cli/` | Sí |
| `scripts/`, `bootstrap.py`, `pyproject.toml` | Sí |
| `skills/` (notas del grafo) | Sí — texto plano |
| `memory/` (conversaciones, decisiones, proyectos) | Sí (revisar secretos) |
| `tools/`, `_tools/`, `_META/`, `_templates/` | Sí |
| `.obsidian/` básico | Sí |
| `apps/docs-web/` (sin `node_modules`) | Sí |
| `build_axon_graph.py` | Sí (fuentes vía env) |

## Qué NO subir (o sanitizar)

| Contenido | Motivo |
|-----------|--------|
| `.env`, API keys, tokens | Secretos |
| `.talaria.local.json` / `.skillgraph.local.json` | Rutas de la máquina |
| `memory/context/**/settings*.json` sensibles | Puede tener claves |
| `node_modules/`, `.venv/`, `*.egg-info/`, caches | Regenerables |
| Rutas absolutas en chats importados | Historial, no config viva |

Usa el `.gitignore` del repo.

## Limitaciones honestas

1. **Skills origen** (Hermes / carpetas locales) no van dentro del repo — solo el **índice** Markdown. Para regenerar AXON: `TALARIA_SKILL_SOURCES=... python build_axon_graph.py`.
2. **MCP del cliente** (`~/.cursor/mcp.json`, etc.) se reconfigura una vez con `talaria connect`.
3. **Obsidian MCP** es opcional; el vault funciona abriendo la carpeta en Obsidian o vía CLI.

## Respuesta corta

Clone → `scripts/install.*` o `pip install -e .` → `talaria boot` → cualquier agente se pone el traje. El conocimiento (notas) viaja entero; binarios y secrets se reinstalan/reconfiguran.

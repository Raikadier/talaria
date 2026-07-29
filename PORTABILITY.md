---
tags: [meta, portability, git]
aliases: [PORTABILITY, portable, repo]
---

# ¿El vault es portable y se puede subir a un repositorio?

**Sí, con matices.** El corazón del segundo cerebro (Markdown + grafo de skills + memoria + tools) **sí es portable**. Lo que no viaja bien son rutas absolutas de *esta* máquina y secretos.

## Qué SÍ subir al repo

| Contenido | Portable |
|-----------|----------|
| `Home.md`, `AGENTS.md`, `README.md` | Sí |
| `skills/` (notas del grafo) | Sí — texto plano |
| `memory/` (conversaciones, decisiones, proyectos) | Sí (revisar secretos) |
| `tools/`, `bootstrap.py`, `_tools/` | Sí — autoinstalación |
| `_META/`, `_templates/`, `.obsidian/` básico | Sí |
| `build_axon_graph.py` | Sí (reasigna `SOURCES` al nuevo PC) |

## Qué NO subir (o sanitizar)

| Contenido | Motivo |
|-----------|--------|
| `.env`, API keys, tokens | Secretos |
| `.skillgraph.local.json` | Rutas de la máquina |
| `memory/context/hermes/config.yaml` (si se copió) | Puede tener claves |
| Rutas absolutas en notas importadas | Funcionan como historial, no como config viva |
| `node_modules/`, `.venv/`, caches | Regenerables vía bootstrap |

Usa el `.gitignore` del vault.

## Flujo en otra máquina / otro agente

```bash
git clone <repo-skillgraph>
cd SkillGraph
python bootstrap.py          # instala markitdown, graphifyy, obsidian-mcp si faltan
```

Luego:

1. Abrir la carpeta como vault en Obsidian (opcional).
2. Configurar MCP `obsidian` apuntando a **esta** ruta clonada (ver [[mcp-obsidian]]).
3. Ingestar docs/proyectos:
   - `python _tools/ingest_document.py archivo.pdf`
   - `python _tools/ingest_project.py ./mi-repo`

## Limitaciones honestas

1. **Skills origen** (Hermes/Skills de David) no van dentro del repo — solo el **índice** Markdown ya generado. Para regenerar el grafo en otro PC hace falta volver a apuntar `build_axon_graph.py` a las rutas locales de skills, o versionar solo las notas.
2. **MCP Cursor/Hermes** fuera del vault (`~/.cursor/mcp.json`, `hermes/config.yaml`) hay que reconfigurarlos una vez (plantilla en [[mcp-obsidian]]).
3. **Chats importados** conservan `source_path` absolutos de la máquina original; son evidencia, no dependencias.

## Respuesta corta

Sí: puedes subir el vault a Git y cualquier agente, tras `python bootstrap.py`, obtiene las herramientas de consumo (MarkItDown + Graphify + MCP Obsidian) automáticamente si no están. El conocimiento (notas) viaja entero; los binarios y secrets no — se reinstalan/reconfiguran.

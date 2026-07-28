---
date: 2026-07-28
type: conversation
tags: [conversation, tools, portability, skillgraph]
---

# MarkItDown + Graphify + portabilidad del vault

**Fecha:** 2026-07-28
**Agente:** Cursor
**Proyecto:** [[SkillGraph]]

## Resumen
Se añadieron MarkItDown (documentos→MD) y Graphify (proyectos→grafo) al vault, con `bootstrap.py` para autoinstalar dependencias. Se documentó portabilidad a Git.

## Artefactos
- [[markitdown]] · [[graphify]] · [[tools-index]]
- [[PORTABILITY]]
- `bootstrap.py`, `tools/manifest.json`, `tools/requirements.txt`
- `_tools/ingest_document.py`, `_tools/ingest_project.py`

## Decisión de portabilidad
El vault **sí** se puede versionar y clonar; el conocimiento viaja. Tras clone: `python bootstrap.py` instala tools. MCP y rutas de máquina se reconfiguran una vez (plantilla en `tools/mcp-obsidian.template.json`).

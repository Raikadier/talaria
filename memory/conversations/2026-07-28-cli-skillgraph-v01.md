---
date: 2026-07-28
type: conversation
pipeline: ironman
layer: memorize
tags: [conversation, cli, skillgraph, ironman]
projects: [SkillGraph]
---

# CLI skillgraph v0.1 construida

**Piloto:** Cursor · **Proyecto:** [[SkillGraph]]

## Hecho
- Diseño: [[cli-design]]
- Arquitectura: [[cli-architecture]]
- Paquete: `skillgraph_cli/` + `pyproject.toml` (`pip install -e .`)
- Comandos: boot, doctor, status, vault, ingest doc/project, import chats
- Docs: [[cli]]

## Uso
```bash
pip install -e .
skillgraph doctor
skillgraph status
```

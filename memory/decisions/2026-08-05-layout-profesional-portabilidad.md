---
tags: [decision, structure, portability]
date: 2026-08-05
status: active
---

# Decisión — layout profesional + portabilidad Talaria

## Contexto

El organismo vivía como vault Obsidian + CLI mezclados, con restos SkillGraph, rutas absolutas Windows y un README regenerado por `build_axon_graph.py`. Cursor aún apuntaba al workspace fantasma `SkillGraph`.

## Decisión

1. **Vault en la raíz** (sin mover `memory/`, `skills/`, `_META/`) para no romper Obsidian.
2. **Código en `src/talaria_cli/`** (layout Python estándar, `pip install -e .`).
3. **Web en `apps/docs-web/`** — fuera del tejido Markdown.
4. **`scripts/install.ps1` + `scripts/install.sh`** para instalar en cualquier PC.
5. **Local config** → `.talaria.local.json` (legacy `.skillgraph.*` se elimina en boot).
6. **Informe AXON** → `_META/axon-build-report.md` (ya no pisa README).
7. Workspace recomendado: `Talaria.code-workspace` en esta carpeta.

## Consecuencias

- `talaria verify` / `doctor` esperan `src/talaria_cli`.
- MCP env usa `PYTHONPATH=<vault>/src`.
- Clone en otra máquina: `scripts/install.*` o `pip install -e . && python bootstrap.py`.

## Refs

[[architecture]] · [[PORTABILITY]] · [[Talaria]]

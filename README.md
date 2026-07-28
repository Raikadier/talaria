# Talaria — SkillGraph Cognitive Operating System (SGCOS)

**Marca comercial:** Talaria  
**Nombre técnico:** SkillGraph Cognitive Operating System (**SGCOS**)  
**Qué es:** un traje + API para que cualquier agente (Cursor, Hermes, Claude Code, …) multiplique capacidad con memoria durable, skills interconectadas, perfiles elite y gates verificables.

> Mitología: las *Talaria* son las sandalias aladas de Hermes. Este proyecto es ese calzado — el agente las “calza” y opera entre vault, tools y mundos MCP.

## Arranque en 60 segundos

```bash
cd SkillGraph
pip install -e .
python -m skillgraph_cli describe --json
python -m skillgraph_cli verify boot --json
python -m skillgraph_cli smoke --json
```

MCP: servidores `skillgraph` + `obsidian` (ver `_META/agent-connect.md`).

## Órganos

| Órgano | Función | Dónde |
|--------|---------|-------|
| **Memoria** | Chats, decisiones, proyectos | `memory/` |
| **AXON** | Skills interconectadas | `skills/` · `axon search` |
| **FORGE** | Perfiles de rol (Leyes I/II) | `_META/forge/` |
| **SPINE** | Protocolo 7 capas | `_META/spine-framework.md` |
| **API** | CLI + MCP | `skillgraph_cli/` |
| **Tools** | Ingest (MarkItDown, Graphify, …) | `tools/` · `bootstrap.py` |

Mapa: `_META/organism.md` · Arquitectura: `_META/architecture.md` · Marca: `_META/brand.md`

## Garantías (A→F)

| Fase | Comando | Estado |
|------|---------|--------|
| A | `verify boot\|close` + scorecard | ✅ |
| B | `doctor` + `smoke` | ✅ |
| C | `forge list\|show\|check\|run` | ✅ |
| D | `axon search\|for-profile` | ✅ |
| E | `eval list\|run` (5 gold tasks) | ✅ |
| F | `mode get\|set` strict/draft | ✅ |

## Documentación web

**Sitio:** [talaria-docs.vercel.app](https://talaria-docs.vercel.app)  
Código estático en `docs-web/public/` (qué es, órganos, SPINE, FORGE, AXON, CLI, garantías A–F, quickstart, futuro).

## Licencia / uso

Vault personal + grafo de skills. No subas secretos (`.gitignore` los excluye).

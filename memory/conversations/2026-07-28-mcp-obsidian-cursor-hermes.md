---
date: 2026-07-28
type: conversation
tags: [conversation, mcp, obsidian, skillgraph]
---

# MCP Obsidian conectado (Cursor + Hermes)

**Fecha:** 2026-07-28
**Agente:** Cursor
**Proyecto:** [[SkillGraph]]

## Resumen
Se configuró el MCP `obsidian-mcp` (filesystem) apuntando al vault SkillGraph en Cursor y Hermes. No requiere plugin Local REST API ni Obsidian abierto.

## Hechos
- Cursor: `C:\Users\david\.cursor\mcp.json` → `obsidian`
- Hermes: `config.yaml` → `mcp_servers.obsidian` + launcher en `mcp\obsidian-mcp\`
- Docs: [[mcp-obsidian]]

## Pendientes usuario
- [ ] Recargar MCP en Cursor Settings → MCP
- [ ] Reiniciar gateway/CLI de Hermes

---
tags: [meta, mcp, obsidian, agent]
aliases: [mcp-obsidian, obsidian-mcp]
---

# MCP Obsidian ↔ Cursor + Hermes

Puente MCP al vault **SkillGraph** (segundo cerebro).

## Vault

`D:\OneDrive - unicesar.edu.co\davidbarcelo0411@g\Business Ideas\SkillGraph`

## Paquete

`obsidian-mcp` (filesystem) — lee/escribe notas Markdown **sin** plugin Local REST API y **sin** tener Obsidian abierto.

## Cursor

Configurado en `C:\Users\david\.cursor\mcp.json` como servidor `obsidian`.

1. Abre **Cursor Settings → MCP**
2. Activa / recarga el servidor `obsidian`
3. Si no aparece, reinicia Cursor

## Claude Code

Configurado en `C:\Users\david\.claude\settings.json` como servidor `obsidian`.  
Al abrir el vault, Claude Code lee `CLAUDE.md` (adaptador IRONMAN).  
Reinicia Claude Code tras cambiar MCP.

## Hermes

Configurado en `config.yaml` → `mcp_servers.obsidian`  
Launcher: `C:\Users\david\AppData\Local\hermes\mcp\obsidian-mcp\run-obsidian-mcp.cmd`  
Addendum: `memories\SKILLGRAPH_IRONMAN.md` + puntero en `SOUL.md`

1. Reinicia el gateway / CLI de Hermes
2. Verifica que el toolset MCP liste `obsidian`

Ver adaptadores: [[pilots]] · [[hermes-adapter]] · [[claude-adapter]] · [[cursor-adapter]]

## Herramientas típicas

`search-vault`, `read-note`, `create-note`, `edit-note`, tags, directorios…

## Protocolo

Los agentes deben seguir [[agent-protocol]] al escribir memoria.

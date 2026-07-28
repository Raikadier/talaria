---
tags: [meta, adapter, cursor, spine]
aliases: [cursor-adapter, piloto-cursor]
---

# Adaptador SPINE → Cursor

Cursor ya es un agente con tools (edición, terminal, MCP, subagentes, browser…).  
SkillGraph es la armadura; Cursor es un piloto de primera clase.

## Mapa

| Capacidad Cursor | Capa SPINE |
|------------------|--------------|
| Edición / terminal | Act |
| MCP `obsidian` | Retrieve + Memorize |
| MCP otros (Supabase, YouTube…) | Act / Ingest según dominio |
| Subagentes Task | Act (heredan AGENTS.md) |
| Agent transcripts | Efímero → import periódico a `memory/conversations/` |

## Boot

1. Workspace = vault **o** MCP obsidian configurado en `~/.cursor/mcp.json`  
2. Leer [[AGENTS]] / [[spine-framework]]  
3. Operar; cerrar con Memorize  

## Alcance global (todos los chats)

- **User Rule Cursor:** `SPINE SkillGraph (todos los chats)` (Settings → Rules, id `17018872`)
- **Project rule:** `.cursor/rules/spine.mdc` (`alwaysApply: true`) en este vault
- Aunque el workspace sea otro proyecto: Act ahí; **Memorize** durable en SkillGraph

## Estado SPINE (Cursor)

- **SUIT ONLINE** — Mk.2 — [[2026-07-28-ironman-activado-cursor]]
- Global: [[2026-07-28-ironman-global-todos-los-chats]]
- Probado: bootstrap + MCP search/read/create-note

## Enlaces

- [[spine-framework]] · [[mcp-obsidian]] · [[pilots]] · [[SPINE-STATUS-CURSOR]]

---
tags: [meta, mcp, api, parity, agent-connect]
aliases: [mcp-parity, talaria-mcp, mcp-general]
version: 1.0
status: active
---

# Talaria MCP — API general del organismo

**Regla de parity:** si un agente puede hacerlo con `talaria <cmd>`, debe existir un tool MCP `talaria_*` equivalente.

Server: `talaria mcp` / `python -m talaria_cli.mcp_server`  
Onboarding: `talaria describe --json` → `talaria connect --client cursor --apply --yes`  
Companion: MCP Obsidian para notas finas (no reemplaza este server).

## Plan ejecutado

1. Auditar CLI vs MCP  
2. Cerrar gap: session · mode · axon feedback/quality · eval · connect  
3. `describe` lista el catálogo completo  
4. Tests de registro de tools  

## Mapa CLI → MCP

| CLI | MCP tool |
|-----|----------|
| `describe` | `talaria_describe` **(primero)** |
| `connect` / `--apply --yes` | `talaria_connect` (`apply`+`confirm`) |
| `doctor` / `boot` / `status` / `vault` | `talaria_doctor` … `talaria_vault_path` |
| `mode get\|set` | `talaria_mode_get` / `talaria_mode_set` |
| `session start\|status\|close` | `talaria_session_*` |
| `verify boot\|close` | `talaria_verify_*` |
| `smoke` | `talaria_smoke` |
| `forge list\|show\|check\|run\|build\|invoke\|graph` | `talaria_forge_*` |
| `axon *` | `talaria_axon_*` |
| `eval *` | `talaria_eval_*` |
| `ingest *` / `import chats` | `talaria_ingest_*` / `talaria_import_chats` |

## Anti-patrones

- No tool “do_anything”  
- No segunda memoria canónica fuera del vault  
- `apply` sin `confirm` = dry-run / rechazo  
- Strict: session + forge_critical siguen vigentes vía scorecard  

## Refs

[[agent-connect]] · [[cli]] · [[architecture]] · [[organism]]

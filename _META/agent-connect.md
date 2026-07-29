---
tags: [meta, agent, connect, cli, mcp]
aliases: [agent-connect, conectar-agentes]
---

# Cómo se conecta cualquier agente a Talaria

Dos vías (preferida → fallback):

## 1) MCP (preferida)

Servidor stdio `talaria` con tools `talaria_*`.

```bash
talaria connect --client cursor --json --write
talaria connect --client hermes --json --write
talaria connect --client claude --json --write
```

O ejecutar el server:

```bash
talaria mcp
# = talaria.mcp_server --vault <path>
```

Ya cableado en:
- Cursor `~/.cursor/mcp.json` → `talaria`
- Hermes `config.yaml` → `mcp_servers.talaria`
- Claude Code `~/.claude/settings.json` → `mcpServers.talaria`

Companion: MCP `obsidian` para CRUD de notas.

## 2) CLI + JSON (fallback universal)

Cualquier agente con shell:

```bash
talaria describe --json
talaria status --json
talaria ingest doc <src> --json
```

## Descubrimiento en 1 comando

```bash
talaria describe --json
```

Devuelve vault, comandos, bloque MCP, constitución SPINE y reglas.

## Protocolo del piloto

1. `talaria_describe` / `describe --json`  
2. `talaria_status` / `doctor`  
3. Trabajar (Act nativo)  
4. Ingest si hace falta  
5. Memorize vía obsidian MCP o escribiendo en `memory/`

Ver [[cli]] · [[pilots]] · [[spine-framework]]

---
tags: [meta, agent, connect, cli, mcp]
aliases: [agent-connect, conectar-agentes]
---

# Cómo se conecta cualquier agente a SkillGraph

Dos vías (preferida → fallback):

## 1) MCP (preferida)

Servidor stdio `skillgraph` con tools `skillgraph_*`.

```bash
skillgraph connect --client cursor --json --write
skillgraph connect --client hermes --json --write
skillgraph connect --client claude --json --write
```

O ejecutar el server:

```bash
skillgraph mcp
# = python -m skillgraph_cli.mcp_server --vault <path>
```

Ya cableado en:
- Cursor `~/.cursor/mcp.json` → `skillgraph`
- Hermes `config.yaml` → `mcp_servers.skillgraph`
- Claude Code `~/.claude/settings.json` → `mcpServers.skillgraph`

Companion: MCP `obsidian` para CRUD de notas.

## 2) CLI + JSON (fallback universal)

Cualquier agente con shell:

```bash
python -m skillgraph_cli describe --json
python -m skillgraph_cli status --json
python -m skillgraph_cli ingest doc <src> --json
```

## Descubrimiento en 1 comando

```bash
skillgraph describe --json
```

Devuelve vault, comandos, bloque MCP, constitución SPINE y reglas.

## Protocolo del piloto

1. `skillgraph_describe` / `describe --json`  
2. `skillgraph_status` / `doctor`  
3. Trabajar (Act nativo)  
4. Ingest si hace falta  
5. Memorize vía obsidian MCP o escribiendo en `memory/`

Ver [[cli]] · [[pilots]] · [[spine-framework]]

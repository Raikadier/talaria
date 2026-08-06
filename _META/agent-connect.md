---
tags: [meta, agent, connect, cli, mcp]
aliases: [agent-connect, conectar-agentes]
---

# Cómo se conecta cualquier agente a Talaria

**Un cuerpo, una API:** el MCP `talaria` es la puerta máquina completa. El CLI es el mismo traje por terminal. Parity: [[mcp-parity]].

## 1) MCP general (preferida)

```bash
talaria describe --json
talaria connect --client cursor --apply --yes
# Claude: talaria connect --client claude --apply --yes  → escribe vault/.mcp.json
talaria mcp   # stdio server
```

Tool **#1 obligatorio:** `talaria_describe`.

Órganos vía tools `talaria_*`: SPINE session · verify · FORGE · AXON (+ feedback/quality) · eval · ingest · mode · connect.

Companion: MCP `obsidian` para CRUD fino de notas (no es otra memoria canónica).

## 2) CLI + JSON (fallback)

```bash
talaria describe --json
talaria session start --objective "..." --forge sw-architect --json
talaria status --json
```

## Protocolo del piloto (MCP o CLI)

1. `talaria_describe`  
2. `talaria_session_start` (strict)  
3. `talaria_verify_boot`  
4. Retrieve: `talaria_axon_*` / vault  
5. Act: `talaria_forge_run` + playbook  
6. Memorize + `forge_critical` en scorecard  
7. `talaria_session_close` (o `talaria_verify_close`)  

## Crear un agente / perfil (Builder 2.0)

Cuando el usuario pida **crear un agente usando Talaria** (desde Claude Code, Cursor, etc.):

```bash
talaria forge build --brief "crea un agente que sepa responder correos" --json
# MCP: talaria_forge_build
# Grafo user-owned: --kind / --invokes / --invocable-by → forge invoke / forge graph
```

1. Llamar `forge build` / `talaria_forge_build`  
2. Ejecutar el `pilot_playbook` del resultado (corpus C1–C5 → `forge check` → `active`)  
3. Para la tarea real: `session start --forge <id>` → `forge run` → (opcional) `forge invoke` → `session close`  

No inventar un perfil solo en el chat: el artefacto canónico vive en el vault ([[forge-builder]] · [[forge-delegation]]).

## Anti-patrones

- Cablear solo Obsidian y saltarse `talaria`  
- Inventar tools fuera del contrato `describe`  
- `apply` sin confirmación  
- Crear un “agente” como prompt efímero sin `forge build`  

Ver [[cli]] · [[pilots]] · [[spine-framework]] · [[mcp-parity]] · [[architecture]] · [[forge-builder]]

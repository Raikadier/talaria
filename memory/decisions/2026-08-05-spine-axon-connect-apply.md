---
tags: [decision, spine, axon, connect]
date: 2026-08-05
status: active
---

# Decisión — SPINE session + AXON quality + connect --apply

## Hecho

1. **SPINE enforcement:** `talaria session start|status|close` crea scorecard, marca `.talaria.session.json`, y cierra vía `verify close` (con `forge_critical` si hay perfil). `verify boot` y `forge run` recomiendan/exigen partitura de sesión.
2. **AXON quality loop:** búsquedas registran `shown` en `memory/context/axon-quality.json`; `axon feedback --signal useful|noise`; `axon quality` ranking; score de search boost/penaliza.
3. **connect --apply --yes:** mergea fragmento MCP en `~/.cursor/mcp.json` (backup `.bak`) o `vault/.mcp.json` para Claude.

## Uso mínimo

```bash
talaria session start --objective "ADR API/worker" --forge sw-architect --json
talaria axon for-profile sw-architect --json
talaria axon feedback --path skills/.../x.md --signal useful --json
talaria connect --client cursor --apply --yes
talaria session close --json
```

## Refs

[[spine-framework]] · [[axon]] · [[agent-connect]] · [[2026-08-05-forge-catalog-v2-completo]]

---
tags: [decision, forge, builder, mcp, pilots]
date: 2026-08-05
status: active
---

# Decisión — FORGE build desde cualquier piloto (NL → draft)

## Contexto
El usuario quiere que desde Claude Code / Cursor (u otro piloto) pueda decir:
«crea un agente que sepa responder correos usando talaria» y que el piloto **ejecute Talaria** para construirlo, no un system prompt efímero.

## Decisión
- CLI: `talaria forge build --brief "…" [--id|--specialty|--deliverable|--force] --json`
- MCP: `talaria_forge_build`
- Scaffold Builder 2.0: perfil `draft` + corpus + `pilot_playbook`
- Constitución: `AGENTS.md`, `CLAUDE.md`, `agent-connect`, adaptadores Claude/Cursor, `forge/builder.md`

## Consecuencia
El piloto es el brazo ejecutor; Talaria FORGE es la fábrica canónica del agente.

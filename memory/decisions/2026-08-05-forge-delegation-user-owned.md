---
tags: [decision, forge, delegation, user-owned]
date: 2026-08-05
status: active
---

# Decisión — Grafo de delegación user-owned (no organigrama producto)

## Contexto
Se exploró jerarquía tipo “software developer → subordinados”. Se rechazó como contenido canónico: Talaria debe permitir que **el usuario cree sus propios agentes**.

## Decisión
- Schema: `role_kind`, `invocable_by_mode`, `invocable_by`, `invokes`
- CLI/MCP: `forge build` flags + `forge invoke` + `forge graph`
- Default `invocable_by_mode=open` (dueño siempre puede `forge run`)
- Ensembles de ejemplo (`software-triad`) siguen siendo *samples*, no el grafo personal

## Consecuencia
Fábrica + protocolo de composición; el organigrama vive en el vault del usuario.

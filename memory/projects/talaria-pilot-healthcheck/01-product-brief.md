---
date: 2026-08-05
type: forge-deliverable
forge_profile: product-manager
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
tags: [forge, deliverable, pilot]
---

# Product brief — Healthcheck

## Outcome
Operadores saben si la API responde sin abrir logs.

## Usuario
SRE / on-call.

## Métrica
`GET /health` → 200 + JSON `{status: ok}` en <100ms local.

## No-goals
UI, auth, métricas de negocio, multi-región.

## Crítica
Pedido pequeño; riesgo de inflarlo a observabilidad completa — rechazado.

## Memorize
`memory/projects/talaria-pilot-healthcheck/01-product-brief.md`

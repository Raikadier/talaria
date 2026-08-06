---
tags: [decision, forge, instruct]
date: 2026-08-05
status: active
---

# Decisión — Auto-instruct al crear agente

## Problema
`forge build` dejaba corpus vacío; los agentes no estaban instruidos.

## Decisión
`forge build` siempre ejecuta `forge instruct` (doctrina + ≥5 fuentes + métodos).  
Seeds ricos para roles de equipo software; genérico profesional para briefs desconocidos.  
Status sigue `draft` hasta calibración → `active`. CLI: `forge instruct [--all-drafts]`.

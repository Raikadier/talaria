---
tags: [decision, forge, builder]
date: 2026-08-05
status: active
---

# Decisión — Catálogo FORGE completo en Builder 2.0

## Hecho

Todos los perfiles activos migrados a **Builder 2.0** (corpus + learn loop + crítica + Gcrit/Gmem):

| Perfil | Eval A/B | Resultado fixture |
|--------|----------|-------------------|
| `sw-architect` | `adr-boundaries-v2` | PASS (0→100) |
| `researcher` | `research-brief-v2` | PASS |
| `sw-engineer` | `engineering-plan-v2` | PASS |
| `programmer` | `atomic-impl-v2` | PASS |
| `social-advisor` | `growth-counsel-v2` | PASS (0→100) |

Enforcement: `verify close` con `forge_profile` exige `forge_critical: pass`.

## Pendiente hacia 10 “de combate”

- Evals con entregables de sesiones reales (LLM vivo), no solo fixtures  
- Calibración humana externa  
- Más oficios según demanda  

## Refs

[[2026-08-05-forge-builder-2]] · [[2026-08-05-sw-architect-v2-eval-ab]] · [[forge-catalog]]

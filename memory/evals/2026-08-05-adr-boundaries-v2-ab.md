---
tags: [eval, forge, ley-II]
date: 2026-08-05
forge_profile: sw-architect
eval_id: adr-boundaries-v2
---

# Eval A/B report — adr-boundaries-v2

## Setup

- Baseline fixture: `_META/evals/fixtures/adr-boundaries-baseline-fail.md`  
- FORGE fixture: `_META/evals/fixtures/adr-boundaries-forge-pass.md`  
- Comando: `talaria eval run adr-boundaries-v2 --ab --json`

## Resultado esperado

| Lado | Esperado |
|------|----------|
| Baseline | FAIL (salto a stack/código) |
| FORGE | PASS (fuerzas, opciones, ADR, boundaries, crítica, memorize) |
| Ley II hold | baseline fail AND forge pass |

## Interpretación

No sustituye evals con LLM en vivo; sí fija una **regresión medible** del contrato del perfil. Ampliar con entregables reales de sesiones FORGE.

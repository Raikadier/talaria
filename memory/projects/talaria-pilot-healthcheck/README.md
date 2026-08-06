---
tags: [project, pilot, forge, software-delivery]
status: active
date: 2026-08-05
ensemble: software-delivery
eval: software-delivery-v1
---

# Piloto — Healthcheck endpoint (software-delivery vertical)

Feature de medición: añadir `GET /health` a un servicio HTTP de ejemplo.

## Protocolo de medición (vs Opus/Claude Code)

1. **Baseline:** mismo brief sin FORGE (un solo hilo genérico) → guardar entregable.  
2. **FORGE:** ensemble `software-delivery` + `forge invoke … --require-deliverable`.  
3. **Score:** `talaria eval run software-delivery-v1 --deliverable <path> --json` y/o `--ab` fixtures.  
4. **Humano:** rúbrica de corrección del código real (tests verdes) — fuera del fixture.

Este repo de notas es el **Memorize** del piloto; el código de demo puede vivir fuera del vault.

## Cadena de artefactos

| Paso | Perfil | Artefacto |
|------|--------|-----------|
| 1 | product-manager | [[01-product-brief]] |
| 2 | software-architect | [[02-adr]] |
| 3 | tech-lead | [[03-tech-plan]] |
| 4 | backend-developer | [[04-backend]] |
| 5 | code-reviewer | [[05-review]] |
| 6 | qa-engineer | [[06-qa]] |
| 7 | devops-sre | [[07-ops]] |
| 8 | tech-lead | [[08-delivery-rollups]] + scorecard |

```bash
talaria forge invoke product-manager software-architect \
  --artifact-in memory/projects/talaria-pilot-healthcheck/01-product-brief.md \
  --deliverable memory/projects/talaria-pilot-healthcheck/02-adr.md \
  --require-deliverable --json
```

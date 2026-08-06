---
date: 2026-08-05
type: forge-deliverable
forge_profile: devops-sre
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
tags: [forge, deliverable, pilot]
---

# Ops / release — Healthcheck

## CI
Job smoke: curl -f "$BASE_URL/health" post-deploy.

## Rollback
Revert commit del handler.

## SLO ligero
Health success durante ventana de deploy.

## Crítica
No sustituye readiness; follow-up explícito.

## Memorize
`memory/projects/talaria-pilot-healthcheck/07-ops.md`

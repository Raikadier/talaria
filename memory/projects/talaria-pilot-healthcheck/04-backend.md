---
date: 2026-08-05
type: forge-deliverable
forge_profile: backend-developer
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
tags: [forge, deliverable, pilot]
---

# Backend — GET /health

## Implementación (especificación ejecutable)
```
GET /health
→ 200 application/json
→ {"status":"ok"}
```
Idempotente; sin I/O; log nivel debug opcional.

## Test
Assert status code 200 y body status=ok.

## Crítica
Sin chequear deps — alineado al ADR (liveness).

## Memorize
`memory/projects/talaria-pilot-healthcheck/04-backend.md`

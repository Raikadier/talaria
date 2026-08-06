---
date: 2026-08-05
type: forge-deliverable
forge_profile: software-architect
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
tags: [forge, deliverable, pilot, adr]
---

# ADR — Health endpoint in-process

## Fuerzas / contexto
Brief: liveness simple. Constraint: sin nuevos runtimes.

## Opciones
1. Handler en el mismo proceso HTTP  
2. Sidecar / separate probe process  

## Decisión
Opción 1. Contrato: `GET /health` → `{"status":"ok"}`. Sin DB. Boundary: no mezclar readiness.

## Trade-offs
Simple vs ceguera a deps — mitigar con `/ready` luego.

## Crítica
Podría estar mal si LB usa health como readiness — documentado.

## Memorize
`memory/projects/talaria-pilot-healthcheck/02-adr.md`

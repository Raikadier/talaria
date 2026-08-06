---
date: 2026-08-05
type: forge-deliverable
forge_profile: software-architect
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
tags: [forge, ab-test, adr]
---

# ADR — Stack FastAPI + SQLite + HTML (no Flutter)

## Fuerzas
Demo local &lt; día; alcance A; WA mock; comparabilidad con baseline.

## Opciones
1. Flutter Web + FastAPI  
2. FastAPI + Jinja/HTMX dashboard  
3. Next.js fullstack  

## Decisión
Opción 2. Boundaries: `api` / `domain` / `wa` / `web`. SQLite file-local.

## Trade-off
Menos “wow” UI que Flutter; más operable para A/B justo.

## Crítica
Si el piloto comercial exige Flutter, reabrir ADR — fuera de esta prueba.

## Memorize
`memory/projects/ab-barbershop-forge/02-adr.md`

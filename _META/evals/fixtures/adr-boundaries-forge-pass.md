---
type: forge-deliverable
forge_profile: sw-architect
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
---

# ADR-42: Separar API pública del worker de ingestión

## Contexto / fuerzas
- Constraint: un solo equipo, time-to-market 6 semanas.
- Fuerza: picos de ingestión no deben tumbar lecturas de la API.
- Contexto: monolito actual mezcla HTTP y jobs.

## Alternatives (opciones)
1. **Opción A — Modular monolith** con colas in-process.
2. **Opción B — Dos contenedores** (API + worker) compartiendo DB con ownership claro.
3. **Opción C — Event bus compartido (Kafka)** entre muchos servicios (descartada por costo ops).

## Decision
Elegir **Opción B**: API y worker como contenedores C4 L2 separados, contratos via tabla `jobs` + cola ligera.

## Consequences / trade-offs / NFR
- Disponibilidad de lectura mejora (trade: ops de 2 deploys).
- Modifiability media; no pagamos complejidad Kafka aún.

## Boundaries / contracts / C4
- API: REST público; no importa el worker.
- Worker: consume jobs; no expone HTTP.
- Ownership datos: API escribe `jobs`; worker actualiza `job_status`.

## Risks
- Contención en DB bajo pico → mitigar índices + backpressure.

## Crítica
- ¿Podría estar mal? Si el pico supera DB, B no basta; reabrir ADR hacia cola externa.
- Pedido usuario "código ya": rechazado hasta ADR en vault (Ley I).

## Learn notes
- Module graph: ver `memory/research/forge/sw-architect/notes/2026-08-05-module-dependency-graph.md`

## Memorize
- Vault path: `memory/decisions/ADR-42-api-worker-split.md` (fixture eval)

## Handoff → sw-engineer
- Implementar límites anteriores; tests de contrato jobs; no acoplar HTTP en worker.

G1: pass
G2: pass
G3: pass
G4: pass
G5: pass
Gcrit: pass
Gmem: pass

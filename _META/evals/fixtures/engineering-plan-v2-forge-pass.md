---
type: forge-deliverable
forge_profile: sw-engineer
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
---

# Engineering plan: API/worker split

## ADR refs
ADR-42 boundaries API vs worker.

## Module map
- api-http
- worker-ingest
- shared-jobs contract

## Sequence / orden
1. Contract jobs
2. API write path
3. Worker consume
4. Integration test

## Contracts
API escribe `jobs`; worker actualiza `job_status`; errores tipados.

## Test strategy
Unit contratos + integration cola/DB.

## Tasks → programmer
### T1 — goal / files / DoD / tests
Implementar contrato jobs; test unitario.

## Crítica
¿Podría estar mal? Contención DB bajo pico — monitorear.

## Memorize
`memory/projects/example/engineering-plan-api-worker.md`

G1: pass
G2: pass
G3: pass
G4: pass
G5: pass
Gcrit: pass
Gmem: pass

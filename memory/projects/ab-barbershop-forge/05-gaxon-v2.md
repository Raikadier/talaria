---
date: 2026-08-05
type: forge-deliverable
forge_profile: tech-lead
skill_pack: software-delivery
require_axon: true
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, Gcrit: pass, Gmem: pass}
axon_skills:
  - skills/community/api-design-principles.md
  - skills/community/api-design-reviewer.md
  - skills/agensi/api-contract-tester.md
  - skills/community/openapi-spec-generation.md
  - skills/community/web-component-design.md
memory_used:
  - memory/evals/2026-08-05-ab-barbershop-protocol.md
  - memory/evals/2026-08-05-ab-barbershop-booking.md
tags: [forge, ab-test, gaxon, hydrate]
---

# A/B v2 — FORGE arm con hidratación AXON

## Qué se aplicó (skills_hydrated → código)

| Skill | Cambio en `sandbox/.../forge` |
|-------|-------------------------------|
| api-design-principles | `Idempotency-Key` + `ErrorBody` shape |
| api-design-reviewer | Security headers + CORS acotado |
| api-contract-tester | Tests 422/401/idempotency/OpenAPI tags |
| openapi-spec-generation | tags + description + examples en schemas |
| web-component-design | (paridad UI; no rediseño visual en v2) |

## Gates
Gcrit: mejoras trazables a skills, no improvisación.  
Gmem: este archivo + informe eval v2.

## Check
```bash
talaria forge check --profile tech-lead --deliverable memory/projects/ab-barbershop-forge/05-gaxon-v2.md --require-axon --json
cd sandbox/ab-barbershop-booking/forge && pytest -q
```

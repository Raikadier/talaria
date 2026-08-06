---
tags: [forge, ensemble, software, user-owned]
aliases: [forge-ensemble-software-delivery, software-delivery]
forge_id: software-delivery
forge_version: 1.0
status: active
laws: [I, II]
profiles:
  - product-manager
  - software-architect
  - tech-lead
  - backend-developer
  - frontend-developer
  - code-reviewer
  - qa-engineer
  - devops-sre
vertical: software-delivery
eval: software-delivery-v1
---

# FORGE Ensemble — Software Delivery (vertical calibrado)

Objetivo: entregar una feature E2E con handoffs por **artefacto obligatorio**.  
No es el organigrama canónico de Talaria: es un vertical **user-owned** calibrado para medición Ley II.

## Secuencia

```
product-manager
      │  product brief
      ▼
software-architect
      │  ADR + boundaries
      ▼
tech-lead
      │  tech plan / slices
      ├──────────────┬──────────────┐
      ▼              ▼              ▼
backend-dev    frontend-dev    devops-sre
      │              │              │
      └──────► code-reviewer ◄──────┘
                    │
                    ▼
               qa-engineer
                    │
                    ▼
            release notes / verify
```

## Contratos (artefacto obligatorio)

| De → A | Artefacto | Comando |
|--------|-----------|---------|
| PM → Architect | Product brief | `forge invoke product-manager software-architect --deliverable … --require-deliverable` |
| Architect → Tech Lead | ADR + boundaries | idem |
| Tech Lead → Backend/Frontend/DevOps | Task pack | idem |
| * → Code Reviewer | Diff summary + riesgos | idem |
| * → QA | Test plan / reporte | idem |

Sin `--deliverable` + `--require-deliverable`, el handoff **no cierra**.

## DoD del conjunto

- [ ] Brief de producto con outcomes  
- [ ] ADR aceptado  
- [ ] Plan técnico con slices  
- [ ] Impl backend + frontend (o justificación N/A)  
- [ ] Review con riesgos  
- [ ] QA plan/reporte  
- [ ] Notas de release/ops  
- [ ] Memorize en vault + scorecard  

## Activación

```text
FORGE ensemble=software-delivery | laws=I+II | spine=on
start_role=product-manager
eval=software-delivery-v1
```

```bash
talaria eval run software-delivery-v1 --ab --json
```

Perfiles del vertical: todos `status: active` con corpus auto-instruct + calibración vertical.

---
tags: [meta, forge, catalog]
aliases: [forge-catalog, perfiles-forge]
version: 2.0
status: active
---

# FORGE — Catálogo de perfiles

Hub: [[forge]] · Builder: [[forge-builder]] (v2) · Leyes: [[forge-two-laws]] · Corpus: [[forge-corpus]] · Delegación: [[forge-delegation]]

> Semilla del repo. **Tus** agentes (creados con `forge build`) también viven en `profiles/` — este catálogo no es el organigrama del producto.

## Perfiles activos (semilla)

| ID | Nombre | Builder | Corpus | Eval A/B |
|----|--------|---------|--------|----------|
| `researcher` | Investigador profesional | **2.0** | `memory/research/forge/researcher/` | `research-brief-v2` |
| `social-advisor` | Asesor de redes sociales | **2.0** | `memory/research/forge/social-advisor/` | `growth-counsel-v2` |
| `sw-architect` | Arquitecto de software | **2.0** | `memory/research/forge/sw-architect/` | `adr-boundaries-v2` |
| `sw-engineer` | Ingeniero de software | **2.0** | `memory/research/forge/sw-engineer/` | `engineering-plan-v2` |
| `programmer` | Programador | **2.0** | `memory/research/forge/programmer/` | `atomic-impl-v2` |

## Ensembles activos

| ID | Nota |
|----|------|
| `software-triad` | [[forge-ensemble-software]] — architect → engineer → programmer (todos v2) |

## Cómo añadir (Builder 2.0)

Preferido (cualquier piloto):

```bash
talaria forge build --brief "…" --json
# opcional grafo: --kind --invokes --invocable-by
```

Manual:
1. Corpus en `memory/research/forge/<id>/` (C1–C5)  
2. Perfil `_META/forge/profiles/<id>.md`  
3. `talaria forge check --profile <id> --json`  
4. Eval A/B en `_META/evals/<id>-v2.json` + fixtures (si quieres Ley II medible)  
5. Fila aquí (opcional — tu vault, tu índice)  

Tutorial grafo: [[forge-example-user-graph]]

## Agentes usuario — equipo software (draft)

> Grafo **tuyos** (industria estándar). Semilla del repo sigue arriba. Completar corpus C1–C5 antes de `active`. Ver [[forge-delegation]].

| ID | kind | Nota |
|----|------|------|
| `product-manager` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `product-owner` | specialist | draft Builder 2.0 — equipo software estándar |
| `business-analyst` | specialist | draft Builder 2.0 — equipo software estándar |
| `product-designer` | both | draft Builder 2.0 — equipo software estándar |
| `ux-designer` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `ui-designer` | specialist | draft Builder 2.0 — equipo software estándar |
| `ux-researcher` | specialist | draft Builder 2.0 — equipo software estándar |
| `ux-writer` | specialist | draft Builder 2.0 — equipo software estándar |
| `software-architect` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `tech-lead` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `engineering-manager` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `backend-developer` | specialist | draft Builder 2.0 — equipo software estándar |
| `frontend-developer` | specialist | draft Builder 2.0 — equipo software estándar |
| `mobile-developer` | specialist | draft Builder 2.0 — equipo software estándar |
| `fullstack-developer` | both | draft Builder 2.0 — equipo software estándar |
| `platform-engineer` | specialist | draft Builder 2.0 — equipo software estándar |
| `devops-sre` | specialist | draft Builder 2.0 — equipo software estándar |
| `data-engineer` | specialist | draft Builder 2.0 — equipo software estándar |
| `security-engineer` | specialist | draft Builder 2.0 — equipo software estándar |
| `qa-engineer` | orchestrator | draft Builder 2.0 — equipo software estándar |
| `automation-qa` | specialist | draft Builder 2.0 — equipo software estándar |
| `scrum-master` | specialist | draft Builder 2.0 — equipo software estándar |
| `code-reviewer` | specialist | draft Builder 2.0 — equipo software estándar |
| `data-analyst` | specialist | draft Builder 2.0 — equipo software estándar |
| `ml-engineer` | specialist | draft Builder 2.0 — equipo software estándar |
| `technical-writer` | specialist | draft Builder 2.0 — equipo software estándar |
| `release-manager` | specialist | draft Builder 2.0 — equipo software estándar |
| `support-engineer` | specialist | draft Builder 2.0 — equipo software estándar |
| `compliance-privacy` | specialist | draft Builder 2.0 — equipo software estándar |

## Ensembles — vertical calibrado

| ID | Nota |
|----|------|
| `software-delivery` | [[forge-ensemble-software-delivery]] — 8 agentes active + eval `software-delivery-v1` |

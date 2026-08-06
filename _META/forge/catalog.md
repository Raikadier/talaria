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

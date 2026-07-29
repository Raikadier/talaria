---
tags: [meta, forge, ensemble]
aliases: [forge-ensembles, ensembles-forge]
version: 1.0
status: active
---

# FORGE — Ensembles

Un **ensemble** es un equipo de perfiles con contratos de handoff. Sirve cuando un solo rol (o un solo modelo de corrido) diluye especialidades.

## Reglas de ensemble

1. **Un rol activo a la vez** (salvo review adversarial explícita)  
2. **Handoff solo con artefacto** (ADR, plan, task, research note)  
3. **No pisar ownership** — architect no codea producto; programmer no redefine boundaries  
4. Ley I/II aplican a **cada** rol y al **resultado conjunto**  
5. Todo artefacto canónico → vault Talaria (SPINE)  

## Catálogo de ensembles

| ID | Perfiles | Para qué |
|----|----------|----------|
| `software-triad` | [[forge-ensemble-software]] | Software que un solo hilo no sostiene |

## Cómo activar

```text
FORGE ensemble=<id> | laws=I+II | spine=on
start_role=<forge_id>
```

Builder de ensembles nuevos: definir secuencia, contratos I/O, criterios de done del conjunto, y modos de escalada. Indexar aquí.

---
date: {{date}}
type: scorecard
tags: [scorecard, spine, verify]
status: open
mode: strict
objective: ""
organs_used: []
evidence: []
gates: n/a
forge_profile: ""
forge_builder: ""
forge_critical: ""
forge_learned: false
forge_memorize: []
delta_vs_generic: []
done: false
projects: []
---

# Scorecard de sesión

Copia a `memory/conversations/` o `memory/projects/` al cerrar trabajo útil.  
Cierre: `talaria verify close --scorecard <esta-nota> --json`

Si usaste FORGE (`forge_profile` no vacío) en modo strict:
- `forge_critical: pass` — pensaste críticamente (fuentes/resultado/pedido)
- evidencia / `forge_memorize` — paths o wiki-links al vault
- si hubo learn loop: `forge_learned: true` + paths en `forge_memorize`

## Objetivo
(qué se pidió)

## Órganos usados
- [ ] memory
- [ ] axon
- [ ] forge
- [ ] spine
- [ ] api / cli
- [ ] tools

## Evidencia (wiki-links obligatorios)
- [[...]]

## Gates
| Gate | Resultado |
|------|-----------|
| Memorize | pass / fail |
| FORGE crítica | pass / fail / n/a |
| FORGE (resto) | pass / fail / n/a |

## Delta vs chat genérico
1.
2.
3.

## Cierre
- [ ] `done: true` en frontmatter cuando verify close deba pasar en modo strict

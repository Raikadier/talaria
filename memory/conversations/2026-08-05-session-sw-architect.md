---
date: 2026-08-05
type: scorecard
tags: [scorecard, spine, verify, session]
status: open
mode: strict
objective: "Test SPINE enforcement"
organs_used: [spine, memory, forge]
evidence: []
gates: n/a
forge_profile: sw-architect
forge_builder: 2.0
forge_critical: ""
forge_learned: false
forge_memorize: []
delta_vs_generic: []
done: false
projects: []
---

# Scorecard de sesión — 2026-08-05

## Objetivo
Test SPINE enforcement

## Partitura SPINE
1. Verify boot (si mode=strict)
2. Retrieve (vault / AXON / corpus FORGE)
3. Act (playbook del perfil si aplica)
4. Memorize evidencia (wiki-links)
5. Crítica (si FORGE) → `forge_critical: pass`
6. Verify close — este scorecard

## Evidencia
- 

## Gates
| Gate | Resultado |
|------|-----------|
| Memorize | |
| FORGE crítica | required |
| FORGE resto | required |

## Delta vs chat genérico
1.

## Cierre
- [ ] `done: true` cuando verify close deba pasar en strict

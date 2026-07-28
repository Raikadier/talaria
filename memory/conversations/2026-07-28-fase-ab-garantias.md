---
date: 2026-07-28
type: conversation
tags: [conversation, skillgraph, verify, guarantees]
projects: [SkillGraph]
agents: [cursor]
---

# Conversación: Fase A+B garantías implementadas

**Resumen:** CLI **0.3.0** — `verify boot/close`, scorecard, `doctor` organismo, `smoke`. Smoke **10/10 PASS**. Doctor falla honestamente si falta MarkItDown (`skillgraph boot`).

## Comandos
```bash
python -m skillgraph_cli verify boot --json
python -m skillgraph_cli verify close --scorecard <path> --json
python -m skillgraph_cli doctor --json
python -m skillgraph_cli smoke --json
```

## Artefactos
- `_templates/scorecard.md`
- `skillgraph_cli/cmds/verify.py` · `smoke.py`
- Plan: [[2026-07-28-garantias-skillgraph]]

## Siguiente
Fase C: `forge list/show/check` — **hecho** (0.4.0).  
Fase D: `axon search` — **hecho** (0.5.0). Siguiente: Fase E eval harness.

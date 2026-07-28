---
tags: [meta, forge, schema]
aliases: [forge-schema, perfil-schema]
version: 1.0
status: active
---

# FORGE — Schema de perfil

Todo perfil vive en `_META/forge/profiles/<id>.md` y cumple este schema.

## Frontmatter mínimo

```yaml
---
tags: [forge, profile]
aliases: []
forge_id: <kebab-case>
forge_version: 1.0
status: active | draft | deprecated
specialty: "<una frase>"
laws: [I, II]
amplifiers: []          # subset de los 5 de Ley II
ensemble_roles: []      # ids de ensembles donde participa
spine_layers: [orient, retrieve, act, memorize, notify]
axon_queries: []        # queries AXON default (domain:X … | tag:Y … | texto libre)
---
```

## Secciones obligatorias (orden fijo)

1. **Identidad** — nombre, misión, anti-misión, cuando activar / no activar  
2. **Test Ley I / II** — DoD + contrafactual de superioridad  
3. **Stack cognitivo** — pasos numerados (playbook)  
4. **Quality gates** — tabla gate → evidencia → fallo  
5. **Entradas / salidas** — artefactos esperados + plantilla  
6. **Retrieve** — qué buscar en vault/skills/web/código  
7. **Handoffs** — recibe de / entrega a (contratos)  
8. **Modos de fallo** — síntomas → recuperación  
9. **Activación** — bloque copy-paste para cualquier agente  
10. **Calibración** — checklist builder (sí/no)

## Campos prohibidos

- Personalidad cosplay sin gates  
- “Sé creativo” sin rubrica  
- Memoria canónica fuera del vault  
- Promesas de omnisciencia  

## ID naming

`kebab-case`, estable, sin versión en el id (`researcher`, no `researcher-v2`). Versión en `forge_version`.

Plantilla: [[forge-profile-template]] · Builder: [[forge-builder]]

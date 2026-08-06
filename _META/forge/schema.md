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
forge_version: 1.0 | 2.0
status: active | draft | deprecated | example
specialty: "<una frase>"
laws: [I, II]
amplifiers: []          # subset de los 5 de Ley II
ensemble_roles: []      # ids de ensembles donde participa
spine_layers: [orient, retrieve, act, memorize, notify]
axon_queries: []        # queries AXON default
corpus_path: memory/research/forge/<id>   # Builder 2.0 (obligatorio para active v2)
builder: 1.0 | 2.0      # protocolo usado al fabricar
# --- Delegación user-owned (opcional; ver [[forge-delegation]]) ---
role_kind: both         # orchestrator | specialist | both
invocable_by_mode: open # open | allowlist | deny_direct
invocable_by: []        # forge_ids que pueden invocar este perfil
invokes: []             # forge_ids a los que este perfil puede delegar
---
```

Talaria **no** define el organigrama: el usuario crea agentes con `forge build` y opcionalmente declara el grafo.

## Secciones obligatorias (orden fijo)

### Contrato (todas las versiones)
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

### Oficio (Builder 2.0 — obligatorio para `builder: 2.0` + `status: active`)
11. **Corpus refs** — `corpus_path` + link a `00-doctrine.md`  
12. **Learn loop** — cuándo investigar, dónde Memorize, qué está prohibido  
13. **Pensamiento crítico** — tablas/preguntas sobre fuentes, resultados y pedidos del usuario  
14. **Relación de conocimientos** — cómo usa ADRs/notas previas (puede vivir dentro del stack)  

Contrafactual Ley II en v2 debe **citar** amplificadores anclados al corpus.

## Campos prohibidos

- Personalidad cosplay sin gates  
- “Sé creativo” sin rubrica  
- Memoria canónica fuera del vault  
- Promesas de omnisciencia  
- Corpus dump sin síntesis doctrinal  

## ID naming

`kebab-case`, estable, sin versión en el id (`researcher`, no `researcher-v2`). Versión en `forge_version`.

Plantilla perfil: [[forge-profile-template]] · Corpus: [[forge-corpus]] · Builder: [[forge-builder]] · Delegación: [[forge-delegation]]

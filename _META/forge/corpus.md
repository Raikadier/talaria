---
tags: [meta, forge, corpus]
aliases: [forge-corpus, corpus-oficio, doctrina-forge]
version: 1.1
status: active
---

# FORGE Corpus — doctrina verificada del oficio

El **corpus** es el conocimiento del rol, separado del **perfil ejecutable**.

Builder: [[forge-builder]] · Schema: [[forge-schema]] · Catálogo: [[forge-catalog]]

## Layout canónico

```
memory/research/forge/<forge_id>/
├── README.md · 00-doctrine.md · 01-role-purpose.md
├── 02-methods.md · 03-antipatterns.md · 04-deliverables.md
├── 05-sources.md
└── notes/YYYY-MM-DD-*.md
```

## Inventario

| forge_id | Estado | Eval A/B |
|----------|--------|----------|
| `researcher` | active v2 | `research-brief-v2` |
| `social-advisor` | active v2 | `growth-counsel-v2` |
| `sw-architect` | active v2 | `adr-boundaries-v2` |
| `sw-engineer` | active v2 | `engineering-plan-v2` |
| `programmer` | active v2 | `atomic-impl-v2` |

Plantilla: [[forge-corpus-template]]

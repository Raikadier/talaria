---
tags: [meta, axon, packs, curation]
aliases: [axon-packs, skill-packs]
status: active
---

# AXON Skill Packs

**Curar ≠ borrar.** Un pack define qué entra al **Act** para una misión. El banco completo sigue en `skills/`; el noise se degrada con `axon feedback --signal noise`, no se borra por defecto.

## Uso

```bash
talaria axon pack list --json
talaria forge run tech-lead --pack software-delivery --json
# hydrate on by default: skills bodies + memory retrieve
talaria memory retrieve "youtube thumbnail" --json
```

## Packs semilla
| ID | Misión |
|----|--------|
| `software-delivery` | Features E2E / vertical software |
| `youtube-channel` | Canal YouTube (guion, SEO, retención…) |

Añadir: `_META/axon/packs/<id>.json` con `queries` y/o `skills` (paths).

## Gate Gaxon
Entregables deben listar skills usadas:

```yaml
axon_skills:
  - skills/…/….md
```

`talaria forge check` valida Gaxon si el perfil declara `require_axon: true` o el check se corre con `--require-axon`.

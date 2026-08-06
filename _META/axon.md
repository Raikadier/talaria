---
tags: [meta, axon, organ, skills, graph]
aliases: [AXON, axon, skill-web, skillweb, grafo-skills]
version: 1.0
status: active
---

# AXON — Ability Crosslink & Operational Network

**Órgano:** red de capacidades de [[organism|Talaria]]  
**Nombre técnico:** *Ability Crosslink & Operational Network*  
**Nombre de uso:** **AXON**  
**Antes llamado:** “skill web” / grafo de skills  

> AXON es el tejido de **skills interconectadas** listas para Retrieve y activación. No es memoria de chats ni perfiles FORGE: es el mapa de *qué sabe hacer* el organismo.

## Dónde vive

| Pieza | Ruta |
|-------|------|
| Notas de skill | `skills/<dominio>/` |
| Hubs de dominio | `_META/domains/` |
| Ejes transversales | `_META/axes/` |
| Taxonomía | [[taxonomy]] |
| Generador | `build_axon_graph.py` |

## Función en el cuerpo

```
SPINE (Retrieve) ──consulta──► AXON (skills + enlaces)
FORGE (perfil)   ──enruta───► AXON (qué skills usar en el rol)
Memoria          ──no sustituye──► AXON (capacidades ≠ episodios)
```

## Cómo usar (cualquier agente)

1. Empezar por [[taxonomy]] o un eje (`[[coding]]`, `[[research]]`, …)  
2. Seguir wiki-links a skills concretas  
3. Bajo un perfil [[forge]], Retrieve solo el subconjunto relevante  
4. **CLI (preferido para agentes):**
   ```bash
   talaria axon search "refactor testing" --json
   talaria axon search "architecture" --domain software-development --json
   talaria axon for-profile researcher --json
   talaria axon feedback --path skills/.../skill.md --signal useful --json
   talaria axon quality --json
   talaria axon stats --json
   ```
5. **Quality loop:** cada search/for-profile registra `shown` en `memory/context/axon-quality.json`. Feedback `useful|noise` reordena futuros hits.
6. Regenerar el grafo si cambian los bancos: `python build_axon_graph.py`

## Relación con hermanos

| Órgano | Relación |
|--------|----------|
| [[spine-framework\|SPINE]] | Coordina cuándo Retrieve sobre AXON |
| [[forge\|FORGE]] | Perfiles declaran qué tipos de skill enrutar |
| Memoria (`memory/`) | Episodios/decisiones; AXON no las almacena |
| CLI / MCP | Descubrimiento e ingest; no reemplazan el grafo |

## Métricas (orden de magnitud)

~1463 skills únicas · ~70 dominios · decenas de miles de enlaces

## Referencias

- [[organism]] · [[taxonomy]] · [[Home]] · [[spine-framework]] · [[forge]]

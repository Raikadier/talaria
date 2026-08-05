---
type: project
status: active
tags: [project, talaria, second-brain, obsidian, organism]
started: 2026-07-28
updated: 2026-08-05
aliases: [SkillGraph]
---

# Proyecto: Talaria

**Estado:** active  
**Qué es:** el **único** proyecto unificado — organismo completo.  
**Ruta vault:** `D:\OneDrive - unicesar.edu.co\Business Ideas\Talaria`  
**Repo:** https://github.com/Raikadier/talaria

Mapa de órganos: [[organism]] · Layout: [[architecture]] · Install: [[PORTABILITY]]

## Objetivo
Un cuerpo vital: Memoria + **AXON** + **FORGE** + **SPINE** + CLI/MCP + tools — instalable en cualquier PC (`pip install -e .` / `scripts/install.*`).

## Órganos

| Órgano | Función | Estado |
|--------|---------|--------|
| Memoria | `memory/` | activo |
| **AXON** | skills interconectadas (`skills/`) | activo |
| **SPINE** | protocolo (antes IRONMAN) | activo |
| **FORGE** | perfiles de rol | activo |
| CLI / MCP | `src/talaria_cli/` → `talaria` | activo v1.1 |
| Tools | MarkItDown, Graphify, … | Mk.2+ |
| Web | `apps/docs-web/` | separado del vault |

## Decisiones clave
- [[2026-08-05-layout-profesional-portabilidad]] — `src/` + scripts install
- [[2026-07-28-spine-axon-organ-names]] — SPINE + AXON
- [[2026-07-28-forge-naming-y-leyes]] — FORGE
- [[2026-07-28-vault-en-onedrive]] · [[2026-07-28-memoria-ademas-de-skills]]

## Próximos pasos
- [x] Layout profesional + packaging portable
- [ ] Push a `origin` tras revisar diff
- [ ] Abrir Cursor con `Talaria.code-workspace`
- [ ] Regenerar AXON con `build_axon_graph.py` al cambiar bancos

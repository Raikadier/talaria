---
tags: [meta, skillgraph, architecture, organism]
aliases: [organismo-skillgraph, skillgraph-organs, cuerpo-skillgraph]
version: 1.1
status: active
---

# SkillGraph — un solo organismo

**SkillGraph es un único proyecto.** Memoria, AXON, FORGE, SPINE, CLI/MCP y tools no son productos separados: son **órganos** del mismo cuerpo.

```
                    ┌─────────────────────────┐
                    │   PILOTO (Cursor /      │
                    │   Hermes / Claude / …)  │
                    └───────────┬─────────────┘
                                │ se conecta vía
                                ▼
┌───────────────────────────────────────────────────────────┐
│                     SKILLGRAPH (el cuerpo)                │
│                                                           │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  MEMORIA    │  │  AXON        │  │  FORGE          │ │
│  │  (episodios)│  │  (skills     │  │  (roles /       │ │
│  │             │  │   enlazadas) │  │   especialidad) │ │
│  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘ │
│         │                │                    │          │
│         └────────────────┼────────────────────┘          │
│                          ▼                               │
│                 ┌─────────────────┐                      │
│                 │    SPINE        │  sistema nervioso    │
│                 │  (protocolo)    │  7 capas operativas  │
│                 └────────┬────────┘                      │
│                          ▼                               │
│         ┌────────────────┴────────────────┐              │
│         │  CLI + MCP (`skillgraph`)       │  interfaz    │
│         │  + tools (MarkItDown, …)        │  / músculos  │
│         └─────────────────────────────────┘              │
│                                                           │
│  Tejido: Markdown en este vault (OneDrive / Obsidian)     │
└───────────────────────────────────────────────────────────┘
```

## Órganos y función

| Órgano | Nombre técnico | Función vital | Dónde |
|--------|----------------|---------------|-------|
| **Memoria** | — | Chats, decisiones, proyectos, aprendizajes | `memory/` |
| **AXON** | Ability Crosslink & Operational Network | Skills interconectadas listas para usar | `skills/` + `_META/domains\|axes` · [[axon]] |
| **FORGE** | Framework for Operational Role Generation & Excellence | Perfiles de rol elite | `_META/forge/` · [[forge]] |
| **SPINE** | Structured Protocol for Integrated Neural Execution | Protocolo que coordina órganos (antes IRONMAN) | [[spine-framework]] |
| **CLI / MCP** | — | Cómo cualquier agente entra y opera | `skillgraph_cli/` · [[cli]] |
| **Tools** | — | Ingest/normalize/act | `tools/` · [[tools-index]] |
| **Adaptadores** | — | Encaje de cada piloto | `_META/adapters/` |

## Reglas del organismo

1. **Un cuerpo, una verdad** — el vault Markdown es canónico.  
2. **Órganos no rivalizan** — memoria ≠ AXON ≠ FORGE; CLI no es otra memoria.  
3. **SPINE coordina** — sin protocolo, los órganos se pisan.  
4. **El piloto no es el cuerpo** — chat/mem0 = caché; SkillGraph = organismo.

## Mapa rápido

- Estructura completa: [[architecture]]  
- Entrada: [[Home]]  
- Nervioso: [[spine-framework]]  
- Capacidades: [[axon]] · [[taxonomy]]  
- Roles: [[forge]]  
- Memoria: [[memory-index]]  
- Interfaz: [[cli]] · [[agent-connect]]  
- Proyecto unificado: [[SkillGraph]]

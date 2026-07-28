---
date: 2026-07-28
type: decision
tags: [decision, ironman, framework, skillgraph]
status: decided
projects: [SkillGraph]
---

# Decisión: Marco IRONMAN como estándar del cerebro

**Fecha:** 2026-07-28
**Estado:** decided

## Contexto
Con MarkItDown, Graphify y candidatas (Docling, Crawl4AI, Whisper, engraph, Nexus…) había riesgo de que las tools se solaparan o crearan memorias rivales.

## Opciones
1. Instalar tools ad hoc sin contrato
2. Un marco de capas + ownership + Mark levels (IRONMAN)

## Decisión
Adoptar **[[ironman-framework]]** como constitución del vault. `AGENTS.md` obliga a Retrieve→…→Notify. Una sola fuente de verdad: el vault Markdown.

## Consecuencias
- Staging vs canónico separados
- Índices no escriben conocimiento
- Converter rank anti-duplicados
- Niveles Mk.1–5 para bootstrap gradual
- **Pilotos con arsenal propio** (Hermes, Claude Code, Cursor): tools nativas = sensores/actuadores; vault = canónico; adaptadores en [[pilots]]

## Enlaces
- [[SkillGraph]] · [[agent-protocol]] · [[pilots]] · [[2026-07-28-herramientas-gratis-skillgraph]]
- Adaptadores: [[hermes-adapter]] · [[claude-adapter]] · [[cursor-adapter]]
- Arranque Claude: `CLAUDE.md` · Hermes: `memories/SKILLGRAPH_IRONMAN.md`
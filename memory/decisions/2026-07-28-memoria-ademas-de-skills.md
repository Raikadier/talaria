---
date: 2026-07-28
type: decision
tags: [decision, skillgraph, memory]
status: decided
projects: [SkillGraph]
---

# Decisión: Memoria además del catálogo de skills

**Fecha:** 2026-07-28
**Estado:** decided

## Contexto
El grafo de skills indexa capacidades, pero no conserva lo hablado entre sesiones/agentes.

## Opciones consideradas
1. Solo catálogo de skills — útil para descubrimiento, sin memoria
2. Skills + capa `memory/` (conversaciones, decisiones, proyectos, learnings)

## Decisión
SkillGraph = **skills + memoria**. Protocolo en [[agent-protocol]]. Entrada en [[Home]].

## Por qué
Cualquier agente necesita contexto persistente: decisiones, preferencias y estado de proyectos.

## Consecuencias / siguientes pasos
- Tras sesiones útiles: escribir resumen / decisión / learning
- Consultar memoria antes de actuar en proyectos conocidos

## Enlaces
- Proyecto: [[SkillGraph]]
- Conversación: [[2026-07-28-skillgraph-segundo-cerebro]]
- Protocolo: [[agent-protocol]]

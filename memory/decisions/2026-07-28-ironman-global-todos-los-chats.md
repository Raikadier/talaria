---
date: 2026-07-28
type: decision
pipeline: ironman
layer: memorize
status: decided
tags: [decision, ironman, cursor, global]
projects: [SkillGraph]
---

# Decisión: IRONMAN global en todos los chats Cursor

**Estado:** decided

## Contexto
La activación Mk.2 solo en este chat no bastaba; David quiere el traje en **todos** los chats.

## Decisión
1. User Rule global en Cursor: `IRONMAN SkillGraph (todos los chats)` (id `17018872`)
2. Project rule `alwaysApply` en `.cursor/rules/ironman.mdc` del vault

## Consecuencia
Cualquier agente Cursor nuevo hereda el contrato IRONMAN + path del vault SkillGraph. Trabajo en otros repos: Act local, Memorize en SkillGraph.

## Enlaces
- [[IRONMAN-STATUS-CURSOR]] · [[cursor-adapter]] · [[ironman-framework]]

---
tags: [decision, forge, eval, builder]
date: 2026-08-05
status: active
---

# Decisión — Piloto sw-architect Builder 2.0 + eval A/B + cierre FORGE

## Hecho

1. **Corpus** `memory/research/forge/sw-architect/` (C1–C5, doctrina, fuentes S1–S8, learn note module graph).  
2. **Perfil** `sw-architect` → `forge_version: 2.0`, `builder: 2.0`, learn loop, Gcrit/Gmem.  
3. **Eval A/B** `adr-boundaries-v2` con fixtures baseline-fail / forge-pass; `talaria eval run adr-boundaries-v2 --ab`.  
4. **Enforcement:** `verify close` exige `forge_critical: pass` (+ memorize signal) si hay `forge_profile` en scorecard strict.  
5. Gates nombrados `Gcrit`/`Gmem` parseables en forge check.

## Evidencia Ley II (fixture)

Baseline genérico falla rubrica; fixture FORGE pasa → `ley_II_hold: true` cuando A/B OK.

## Pendiente hacia 10

- Migrar `researcher` + triad  
- Más evals con tareas reales (no solo fixtures)  
- Calibración humana externa  

## Refs

[[2026-08-05-forge-builder-2]] · [[forge-builder]] · [[forge-profile-sw-architect]] · [[00-doctrine]]

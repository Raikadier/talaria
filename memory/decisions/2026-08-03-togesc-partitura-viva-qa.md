---
date: 2026-08-03
project: TOGESC
tags: [decision, qa, partitura-viva]
---

# QA Partitura viva — cerrado

## Hallazgos

1. Landing desktop: `.hero-plane { pointer-events: none }` bloqueaba Escuchar/piano → `pointer-events: auto` en controles.
2. Tipografía `Decorations` en `game_session_views.dart` rompía compilación → `BoxDecoration`.
3. Copy gritados en modo velocidad + badges CUENTA → sentence case.
4. Tests Home/smoke desfasados del hub Partitura viva → actualizados.

## Commits

Push a `main` en el ciclo QA del 2026-08-03.

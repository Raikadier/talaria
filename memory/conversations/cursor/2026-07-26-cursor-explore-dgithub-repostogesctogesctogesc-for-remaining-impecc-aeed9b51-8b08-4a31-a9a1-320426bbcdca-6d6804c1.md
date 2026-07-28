---
date: 2026-07-26
type: conversation
source_agent: cursor
session_id: "aeed9b51-8b08-4a31-a9a1-320426bbcdca"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\a12883bf-e1c0-4006-a5c0-9750d2cd70d1\\subagents\\aeed9b51-8b08-4a31-a9a1-320426bbcdca.jsonl"
tags: [conversation, imported, cursor]
title: "Explore d:\\Github repos\\togesc\\TOGESC\\togesc for remaining Impeccable P2 items. Return con"
---

# Explore d:\Github repos\togesc\TOGESC\togesc for remaining Impeccable P2 items. Return con

**Fecha:** 2026-07-26  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `aeed9b51-8b08-4a31-a9a1-320426bbcdca`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\a12883bf-e1c0-4006-a5c0-9750d2cd70d1\subagents\aeed9b51-8b08-4a31-a9a1-320426bbcdca.jsonl`

## Mensajes

### Usuario

Explore d:\Github repos\togesc\TOGESC\togesc for remaining Impeccable P2 items. Return concrete file paths, current structure, and minimal change recommendations.

1. P2-01 Game result: find result_card / game result UI; compare briefly to .tmp_stitch/stitch_togesc_design_system/game_session_premium_result/ (code.html structure: pills, CTA Siguiente, report). List gaps.

2. P2-07 Shell: togesc_shell.dart — how wide nav works now (TextButtons?). What would NavigationRail M3 look like as drop-in.

3. P2-08 Home optimize: mode_bento_card / home_screen — shrinkWrap GridView? heavy build computations?

4. P2-09 Landscape game: game_screen.dart Column layout — what breaks in landscape, minimal adapt.

Thoroughness: medium. Do NOT modify files. Return actionable bullets with paths.

### Asistente

Voy a explorar el código Flutter y el stitch de referencia para localizar los ítems P2 restantes.
[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Glob]
[tool:Grep]

### Asistente

## P2-01 — Game result

**Paths:**  
`d:\Github repos\togesc\TOGESC\togesc\lib\widgets\result_card.dart`  
`d:\Github repos\togesc\TOGESC\togesc\lib\screens\game_screen.dart` (`_buildResultView` / `_buildResultActions`)  
`d:\Github repos\togesc\TOGESC\togesc\lib\widgets\game_session_views.dart` (`GameSessionResultSectionLabel`)  
Stitch: `d:\Github repos\togesc\.tmp_stitch\stitch_togesc_design_system\game_session_premium_result\code.html`

**Estructura actual**
- `ResultCard`: barra superior + título EXCELENTE/INCORRECTO + métricas TIEMPO/RITMO + bloque “Dominio de notas” como filas (`_SrsNoteRow`) con texto `$consecutive/5`.
- `game_screen`: scroll con card → piano read-only → CTA fijo abajo (`Siguiente` / auto-advance / Volver).
- Stitch: mismos bloques base + **pills** de progreso (5 barras en chip redondo) + link **“Ver reporte completo”** + CTA **“Siguiente Round”** h-16 con shimmer.

| Stitch | Flutter hoy | Gap |
|--------|-------------|-----|
| Pills 5 segmentos | Texto `n/5` | No hay pills |
| “Ver reporte completo” | Ausente | Link a stats/notes |
| Subtítulos (próximo repaso / atención) | Solo Aprendiendo/Consolidada | Datos SRS infrautilizados |
| CTA “Siguiente Round” hero | `FilledButton.icon` “Siguiente” | Copy/altura menores |
| Card + piano + dominio | Ya alineado | OK |

**Cambio mínimo**
- En `_SrsNoteRow`, reutilizar `srs_progress_indicator.dart` (o su patrón de barras) en lugar de `'n/5'`.
- Cabecera de dominio: `Row` con título + `TextButton` → `context.push(AppRoutes.statisticsNotes)`.
- Opcional: `next_review` / estado débil desde `srsChanges` si ya vienen en el map.
- CTA: label `"Siguiente"` → `"Siguiente round"`; `minimumSize` ~56–64. Sin glow/shimmer (DESIGN.md).

---

## P2-07 — Shell / NavigationRail

**Path:** `d:\Github repos\togesc\TOGESC\togesc\lib\widgets\togesc_shell.dart`  
Breakpoint: `DesignTokens.shellBreakpoint` = 600 (`design_tokens.dart`).

**Cómo funciona wide hoy**
- `wide`: sin `NavigationBar`; nav en `AppBar.actions` vía `_DesktopNavLink` = **`TextButton`** (Entrenamiento / Estadísticas / Pro) + IconButtons Pro/Cuenta.
- Narrow: `NavigationBar` M3 con 4 destinations (Práctica, Estadísticas, Pro, Perfil).

**Drop-in NavigationRail M3**
```
Scaffold(
  body: Row(
    children: [
      if (wide) NavigationRail(
        selectedIndex: selected,
        onDestinationSelected: (i) => _onTabSelected(...),
        labelType: NavigationRailLabelType.all,
        destinations: [...mismos 4 icons/labels que NavigationBar],
      ),
      Expanded(child: child),
    ],
  ),
  bottomNavigationBar: wide ? null : NavigationBar(...),
)
```
- Quitar `_DesktopNavLink` del header (o dejar solo brand + 1–2 actions).
- Reusar `_selectedIndex` / `_onTabSelected` sin tocar router.
- Ajuste: `SafeArea(bottom: wide)` ya favorece rail; tests en `test/widget/togesc_shell_test.dart`.

---

## P2-08 — Home optimize

**Paths:**  
`d:\Github repos\togesc\TOGESC\togesc\lib\screens\home_screen.dart`  
`d:\Github repos\togesc\TOGESC\togesc\lib\widgets\mode_bento_card.dart` (`ModeBentoGrid` L346–348)  
`d:\Github repos\togesc\TOGESC\togesc\lib\widgets\togesc_ui.dart` (`TogescPageBody` → `SingleChildScrollView`)

**Problemas**
1. **`GridView.builder(shrinkWrap: true, physics: NeverScrollableScrollPhysics)`** dentro de `TogescPageBody` scrollable → mide todos los hijos; anti-pattern de scroll anidado.
2. **Cómputo en `build`:** cada rebuild arma `bentoModes` (6 entradas + closures), `buildDailyPracticeSummaries(history)`, `hi

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]

---
date: 2026-07-24
type: conversation
source_agent: cursor
session_id: "fedfd0f0-ad5e-491b-b258-53a14036b19a"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\2149fb3f-8908-4916-a807-27d252ddd8da\\subagents\\fedfd0f0-ad5e-491b-b258-53a14036b19a.jsonl"
tags: [conversation, imported, cursor]
title: "Audita de forma exhaustiva y solo lectura el frontend del repositorio D:/Github repos/toge"
---

# Audita de forma exhaustiva y solo lectura el frontend del repositorio D:/Github repos/toge

**Fecha:** 2026-07-24  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `fedfd0f0-ad5e-491b-b258-53a14036b19a`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\2149fb3f-8908-4916-a807-27d252ddd8da\subagents\fedfd0f0-ad5e-491b-b258-53a14036b19a.jsonl`

## Mensajes

### Usuario

Audita de forma exhaustiva y solo lectura el frontend del repositorio D:/Github repos/togesc. Revisa React/UI, accesibilidad, responsive, navegación, estados de carga/error/vacío, UX, internacionalización, rendimiento del cliente, motion, diseño y coherencia de componentes. No edites archivos. Contrasta el código real, no confíes únicamente en docs/auditoria. Devuelve hallazgos priorizados (crítico/alto/medio/bajo), cada uno con evidencia exacta ruta:líneas, impacto y arreglo recomendado; incluye fortalezas verificadas. Thoroughness: very thorough.

### Asistente

Voy a auditar el frontend del repositorio de forma exhaustiva y solo lectura, contrastando el código real con la estructura del proyecto.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Glob]
[tool:Glob]
[tool:Read]

### Asistente

El frontend es Flutter, no React. Profundizo en pantallas, navegación, accesibilidad, i18n y estados de UI.


[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Grep]
[tool:Grep]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Grep]
[tool:Grep]

### Asistente

[tool:UpdateCurrentStep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Glob]
[tool:Grep]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Read]

### Asistente

[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:Read]
[tool:Grep]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

[tool:Read]
[tool:Read]
[tool:Grep]
[tool:Read]

### Asistente

[tool:UpdateCurrentStep]

### Asistente

# Auditoría frontend TOGESC (solo lectura)

**Alcance verificado:** `D:/Github repos/togesc/TOGESC/togesc/lib/` — **144 archivos Dart**, Flutter + Riverpod + go_router + Material 3.

**Nota sobre React:** No hay frontend React en producción (`package.json` inexistente). El cliente es **Flutter** (ADR-001). Existen mockups HTML en `.tmp_stitch/` (diseño Stitch), no código de app. Esta auditoría cubre el UI Flutter real; donde pedías “React/UI”, aplica al árbol de widgets Flutter.

**Contraste con `docs/auditoria`:** Varios hallazgos de `05_ui_ux_accesibilidad.md` sobre el piano **ya no aplican** — el código actual incluye `Semantics`, `Focus`, teclado y badges. El doc de auditoría está **desactualizado** respecto al piano.

---

## Fortalezas verificadas

| Área | Evidencia |
|------|-----------|
| Design system coherente | `design_tokens.dart:1-109`, `app_theme.dart:1-394` — tokens Harmonic Precision, M3, Hanken Grotesk, `touchTargetMin = 48` |
| Navegación estructurada | `router.dart:24-147` — go_router, `ShellRoute` + `TogescShell`, guards Pro, redirect onboarding |
| Responsive básico | `togesc_shell.dart:43-54` (≥600px desktop nav), `mode_bento_card.dart:559-563` (grid 1/2 cols), `daily_focus_section.dart:72-74` (≥520px) |
| Piano accesible (mejorado) | `piano_keyboard.dart:177-213,231-233,262-264` — Semantics por tecla, Enter/Espacio, badges ✓/✗, área táctil negra 48dp (`blackHitWidth = touchTargetMin:229`) |
| Tests UI relevantes | 46 tests en `test/` incl. `piano_keyboard_test.dart`, `togesc_shell_test.dart`, `game_screen_test.dart`, `router_onboarding_test.dart` |
| Preferencia reduce motion (parcial) | `ui_preferences.dart:48`, `gameplay_settings_section.dart:85-94`, `game_screen.dart:45-48` |
| Timer modo velocidad con cleanup | `speed_session_provider.dart:91-96` — `ref.onDispose(() => _countdownTimer?.cancel())` |
| Estados monetización | Paywall, guards, upsells en stats/home — flujo Pro coherente |
| Separación UI/estado | Screens delgadas + widgets + providers Riverpod (coincide con `02_frontend.md`) |

---

## Hallazgos priorizados

### CRÍTICO

#### C1 — Spinner infinito si falla la carga SRS (Estadísticas y Progreso por nota)
**Evidencia:**
- `srs_provider.dart:111-117` — en `loading` y `error` devuelve `{}`
- `statistics_screen.dart:38-41` — `if (stats.isEmpty)` → `CircularProgressIndicator` sin distinguir error
- `note_progress_screen.dart:27-31` — `if (summaries.isEmpty)` → spinner (también en error: `srs_provider.dart:131-137`)

**Impacto:** Si SharedPreferences falla, sync corrupto o error de repositorio, el usuario queda en pantalla de carga **sin mensaje ni acción de recuperación**. Bloquea el dashboard completo.

**Arreglo recomendado:** Observar `srsSystemProvider` como `AsyncValue` en pantallas; ramas explícitas `loading` / `error` / `data`. En error: mensaje + botón “Reintentar” (`ref.invalidate(srsSystemProvider)`) y opción “Reiniciar progreso local”.

---

#### C2 — Errores de providers silenciados en toda la UI de ajustes y cuenta
**Evidencia (patrón repetido `error: (_, _) => const SizedBox.shrink()`):**
- `appearance_settings_section.dart:50`
- `gameplay_settings_section.dart:99`
- `practice_settings_section.dart:63,90`
- `session_settings_section.dart:65`
- `audio_settings_section.dart:23`
- `note_pool_settings_section.dart:68`
- `srs_intensity_settings_section.dart:52`
- `session_history_card.dart:120`
- `sync_diagnostics_card.dart:95`
- `account_sync_views.dart:236`
- `account_screen.dart:353`

**Imp

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]

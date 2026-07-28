---
date: 2026-07-24
type: conversation
source_agent: cursor
session_id: "c5d2eb53-a27c-4674-bcc5-567ceda60202"
project: "d-Github-repos-togesc"
source_path: "C:\\Users\\david\\.cursor\\projects\\d-Github-repos-togesc\\agent-transcripts\\2149fb3f-8908-4916-a807-27d252ddd8da\\subagents\\c5d2eb53-a27c-4674-bcc5-567ceda60202.jsonl"
tags: [conversation, imported, cursor]
title: "Audita el diseño UI/UX del frontend Flutter de TOGESC en D:/Github repos/togesc/TOGESC/tog"
---

# Audita el diseño UI/UX del frontend Flutter de TOGESC en D:/Github repos/togesc/TOGESC/tog

**Fecha:** 2026-07-24  
**Agente:** cursor  
**Proyecto/contexto:** d-Github-repos-togesc  
**Sesión:** `c5d2eb53-a27c-4674-bcc5-567ceda60202`  
**Origen:** `C:\Users\david\.cursor\projects\d-Github-repos-togesc\agent-transcripts\2149fb3f-8908-4916-a807-27d252ddd8da\subagents\c5d2eb53-a27c-4674-bcc5-567ceda60202.jsonl`

## Mensajes

### Usuario

Audita el diseño UI/UX del frontend Flutter de TOGESC en D:/Github repos/togesc/TOGESC/togesc.

Enfócate en PROBLEMAS reales de diseño (no lógica de negocio):
- Sistema de diseño / tokens (colores, tipografía, spacing, radius, elevation)
- Consistencia visual entre pantallas
- Dark mode / light mode
- Accesibilidad (contraste, touch targets, semantics, reduced motion)
- Responsive web vs móvil
- Landing/web marketing si existe
- Componentes genéricos vs diseño de producto
- Hardcoded colors, Magic numbers, inconsistencias
- Calidad percibida vs estándares de industria (Material 3, apps de educación musical / fitness-learning)

Lee:
- lib/theme/ o equivalente
- lib/app/ o main theme
- pantallas principales: home, game, statistics, onboarding, account/settings, paywall, landing
- widgets clave del piano y feedback
- docs/auditoria/05_ui_ux_accesibilidad.md si aporta
- .tmp_stitch/stitch_togesc_design_system/harmonic_precision/DESIGN.md si existe como referencia de marca

Devuelve un informe estructurado en español con:
1. Veredicto corto (1-2 frases)
2. Problemas CRÍTICOS / ALTOS / MEDIOS / BAJOS, cada uno con evidencia (archivo + qué falla) y por qué importa
3. Lo que está bien hecho
4. Gap vs design system Stitch si aplica

Sé concreto y crítico. No inventes. Thoroughness: very thorough.

### Asistente

Voy a auditar el frontend Flutter con foco en tokens, consistencia, accesibilidad y gap frente al design system Stitch.
[tool:UpdateCurrentStep]
[tool:Glob]
[tool:Glob]
[tool:Read]
[tool:Read]
[tool:Grep]

### Asistente

## 1. Veredicto

La app tiene una base de design system real (Harmonic Precision + M3 + Hanken Grotesk) y varias pantallas “premium” coherentes, pero **no está cerrada como producto visual**: el dark mode se rompe en feedback/semánticos, hay widgets legacy fuera de tokens, y el layout web/desktop no cumple el grid Stitch. Nivel percibido: **buen MVP académico**, por debajo de apps educativas pulidas (Duolingo/Tone Gym) en consistencia dark, responsive y acabado.

---

## 2. Problemas

### CRÍTICOS

Ninguno que bloquee el uso en light mode de forma clara. Los fallos graves están en **dark mode / contraste** (abajo como ALTO). No invento un P0 de contraste sin medición instrumental; el riesgo más duro está documentado con evidencia de color fijo claro sobre superficie oscura.

### ALTOS

**A1 — Tokens semánticos oscuros incompletos (feedback musical)**  
- **Evidencia:** `D:/Github repos/togesc/TOGESC/togesc/lib/app/design_tokens.dart` (líneas ~43–65): existen `darkBackground/surface/primary…`, pero **no** `darkCorrect`, `darkIncorrect`, `darkSelection`, ni variantes dark de `speed*`.  
- **Uso fijo en UI:** `piano_keyboard.dart`, `result_card.dart`, `countdown_timer_widget.dart`, `session_history_card.dart`, etc. usan `DesignTokens.correct/incorrect/selection` siempre.  
- **Por qué importa:** en dark, el feedback del loop de entrenamiento (el core UX) no se adapta al tema; contraste y “feel” del piano/resultados quedan optimizados para light. Coincide con UX-001 de `docs/auditoria/05_ui_ux_accesibilidad.md`.

**A2 — Chip “MODO VELOCIDAD” con superficie light hardcoded en dark**  
- **Evidencia:** `speed_session_views.dart` → `SpeedSessionAnswerHeader`: `color: DesignTokens.speedContainer` (`#FFEBE6`) sin rama dark (a diferencia del icono del card, que sí atenúa alpha).  
- **Por qué importa:** isla crema sobre fondo `#141018`; rompe jerarquía tonal M3 y calidad percibida en una pantalla Pro clave.

**A3 — Acentos hardcoded oscuros sobre dark surface (contraste)**  
- **Evidencia:** `onboarding_screen.dart` pasa `accentColor: DesignTokens.tertiary` (`#402747`) a `PedagogySectionCard`, que pinta el icono con ese color. En dark, `#402747` sobre `#141018`/`surfaceContainerLowest` es casi ilegible.  
- Similar: `togesc_shell.dart` avatar usa `DesignTokens.primary` (`#4E0078`) fijo, no `scheme.primary` dark (`#DA9CFF`).  
- **Por qué importa:** onboarding y chrome principal fallan accesibilidad visual en el tema que el usuario puede elegir en Ajustes.

**A4 — `SrsProgressIndicator` fuera del design system (Material “genérico”)**  
- **Evidencia:** `srs_progress_indicator.dart`: `Colors.deepPurple`, `Colors.grey.shade300`, `Colors.green.shade100`, `Colors.green`, `TextStyle` sueltos (sin `Theme` / tokens).  
- **Por qué importa:** componente de progreso pedagógico que choca con Harmonic Precision; en dark se ve “otra app”. Es el ejemplo más claro de **componente genérico vs producto**.

**A5 — Semantics / a11y concentrados solo en el piano**  
- **Evidencia:** `Semantics(` aparece **solo** en `piano_keyboard.dart` (grep en `lib/`). A11Y-001 del piano está bien; el resto depende de Material por defecto.  
- **Por qué importa:** countdown, métricas de velocidad, bento de modos, charts y badges Pro no anuncian estado de forma explícita; Lighthouse ≥90 sigue abierto en la auditoría previa.

### MEDIOS

**M1 — Responsive incompleto vs Stitch (desktop)**  
- **Evidencia:** único breakpoint tokenizado: `shellBreakpoint = 600` (`design_tokens.dart`). 

_[truncado]_


## Enlaces
- Índice: [[cursor-import-index]]
- Home: [[Home]]

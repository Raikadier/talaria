---
date: 2026-08-01
type: adr
tags: [adr, roundedtb, architecture, windows, gdi]
status: accepted
forge_profile: sw-architect
forge_gates: {G1: pass, G2: pass, G3: pass, G4: pass, G5: pass}
project: RoundedTB
project_path: D:/Github repos/RoundedTB
graph: "[[memory/graphs/roundedtb/README|roundedtb graph]]"
---

# ADR-001: Modelo de clipping de taskbar vía SetWindowRgn

## Estado
Accepted (descripción del sistema actual en fork base `b78e5d6`; guía para evolución).

## Contexto / fuerzas
- Windows no expone API pública para márgenes/segmentos de taskbar.
- Explorer reinicia HWNDs; la forma XAML cambia entre builds (23H2/24H2).
- Objetivo del producto: márgenes + esquinas + segmentos sin patch permanente.
- Constraints: WPF desktop, multi-monitor, DPI, compat TranslucentTB opcional.
- Evidencia Graphify (`ingest project`): **440 nodos · 801 edges · 21 communities**; god nodes: `LocalPInvoke` (59), `MainWindow` (54), `Interaction` (22), `Taskbar` (13), `AppListXaml` (10). Sin ciclos de import.

## Decision
Mantener el **modelo de clipping GDI** (`CreateRoundRectRgn` + `SetWindowRgn` sobre `Shell_TrayWnd`) orquestado por:
- `MainWindow` — UI + estado (`activeSettings`, `taskbarDetails`)
- `Background` — polling ~100 ms
- `Taskbar` — discovery + update simple/dynamic
- `AppListXaml` — override de medida vía UIA `TaskbarFrame` (23H2+)
- `LocalPInvoke` — frontera Win32 (hub de mayor degree)

## Alternatives
1. **DWM `WindowCornerPreference` solo** — redondea chrome; no márgenes/segmentos. Insuficiente.
2. **Inyectar/componer capa propia sobre la taskbar** — más control visual (AA), alto riesgo estabilidad/Store, esfuerzo alto.
3. **Status quo SetWindowRgn + hardening** — menor esfuerzo; límites conocidos (sin AA, pelea auto-hide).

Elegida: **(3)** a corto plazo; evaluar (2) solo si el producto exige AA/auto-hide nativo.

## Consequences
- Fragilidad ante updates de Explorer/UIA.
- Ownership GDI: tras `SetWindowRgn` OK no llamar `DeleteObject` a esa HRGN.
- Dynamic mode depende de heurísticas + árbol XAML.
- `MainWindow` es bridge cross-community (betweenness alta) → riesgo de god-object.

## Boundaries / contracts
| Límite | Contrato |
|--------|----------|
| UI ↔ Worker | `activeSettings` + `taskbarDetails` (hoy sin lock; requiere sincronización) |
| Worker ↔ Shell | Solo vía `Taskbar.*` + `LocalPInvoke` |
| Measure AppList | Win32 HWND **o** `AppListXaml.GetWindowRect()` override |
| Persistencia | `%LocalAppData%\rtb.json` vía `Interaction` |
| Muertos | `AppBars`, `IAppVisibility`, `TaskbarEffect` no forman el camino runtime |

## Risks
| Riesgo | Mitigación |
|--------|------------|
| DeleteObject post-SetWindowRgn | Fix ownership (P0) |
| TaskbarFrame null post-update | Regen + fallback descendants (P0) |
| Race UI/worker | lock/`Concurrent` o marshaling (P1) |
| Sleep en fade bloquea loop | timer/async no bloqueante (P1) |
| net6 EOL + COM IWsh | migrar net8 (P2) |

## Handoff → sw-engineer / programmer
1. P0 GDI ownership en `Taskbar.UpdateSimple/Dynamic`
2. P0 `AppListXaml` resiliencia 24H2+
3. P1 sync estado compartido
4. P1 desbloquear worker en auto-hide fade
5. No cablear DWM corners como reemplazo de márgenes

## Evidencia
- Graphify: `memory/graphs/roundedtb/`
- Repo mapa: `D:/Github repos/RoundedTB/ARCHITECTURE.md`
- Commit base: `b78e5d6`

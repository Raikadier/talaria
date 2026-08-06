---
tags: [eval, ab-test, barbershop, result, hydrate]
date: 2026-08-05
status: final
version: 3
evaluator: cursor-auto
vehicle: cursor
predecessor: 2026-08-05-ab-barbershop-booking-v2.md
---

# Informe A/B v3 — ¿se puede subir más la nota?

Sí. Tras cerrar huecos M1/M4/M5/M7 en el brazo FORGE:

| Métrica | Peso | Baseline | FORGE v2 | FORGE v3 | Qué desbloqueó el punto |
|---------|------|----------|----------|----------|-------------------------|
| M1 Dominio | 20 | 16 | 17 | **19** | conflicto de slot + cancel/no_show |
| M2 Arquitectura | 15 | 9 | 14 | **15** | rate-limit + dispatch reminders |
| M3 Código | 15 | 10 | 15 | **15** | tope (10 pytest) |
| M4 UX Kanban | 10 | 8 | 8 | **9** | 5 columnas + loading/error |
| M5 WA mock | 15 | 12 | 13 | **14** | cancellation/no_show/reminder_sent |
| M6 Operabilidad | 10 | 8 | 9 | **10** | README docs + /docs |
| M7 Seguridad | 10 | 7 | 8 | **9** | rate limit público |
| M8 ICP | 5 | 4 | 5 | **5** | tope |
| **Total** | **100** | **74** | **89** | **96** | Δ vs baseline **+22** |

## Techo realista
- **100** exigiría Meta Cloud real, auth más fuerte que Basic demo, UX pulida de producto, y sesgo-cero de evaluador independiente — fuera de alcance A.
- Con alcance A + mock WA, **~96–97** es el techo honesto; el punto restante está en polish UX (M4) y “casi Meta” (M5), no en magia del traje.

## Verificación
- `pytest -q` en forge: **10 passed**
- Gaxon: entregable v2 sigue válido; cambios v3 son extensión del mismo pack

Baseline intacto en **74**.

---
tags: [eval, ab-test, barbershop, whatsapp]
date: 2026-08-05
status: active
evaluator: cursor-auto
vehicle: cursor
---

# A/B Protocol — WhatsApp Auto-Booking (unidad barbería)

## Decisiones del usuario
1. Vehículo: Cursor (auto) ambos brazos  
2. Brazo sin Talaria: mismo evaluador/piloto, **sin** CLI FORGE/SPINE (baseline “a pelo”)  
3. Alcance **A**: API + DB + webhook WA mock + Kanban mínimo  
4. WhatsApp: **mock**  
5. Stack: libre; elegimos **FastAPI + SQLite + HTML/JS** (mismo en ambos; Flutter descartado por velocidad/demo)  
6. Demo **local** basta  

## Limitación (honesta)
El evaluador es el mismo agente que construye → sesgo posible. Se mitiga con rúbrica fija previa y scores explícitos por dimensión.

## Carpetas
- Baseline: `sandbox/ab-barbershop-booking/baseline/`
- FORGE: `sandbox/ab-barbershop-booking/forge/`
- Artefactos FORGE: `memory/projects/ab-barbershop-forge/`
- Informe: `memory/evals/2026-08-05-ab-barbershop-booking.md`

## Brief congelado (barbería)
**Producto:** unidad de agendamiento + recuperación de leads por WhatsApp (mock) para una barbería.  
**Operador:** dueño/recepción (2–8 personas).  
**Debe:**
- CRUD/flujo de leads/citas con estados: `new_lead` → `confirmed` → `completed` (+ `no_show`/`cancelled` opcional)
- Dashboard Kanban de citas
- Link público de agendamiento (cliente elige servicio + slot)
- Webhook/mock que “envía” WhatsApp: confirmación al agendar + recordatorio
- Persistencia SQLite, README run local, `.env.example`
**No debe (V1):** facturación, inventario, roles complejos, Meta Cloud real

## Rúbrica (0–100)
| ID | Dimensión | Peso |
|----|-----------|------|
| M1 | Correctness dominio | 20 |
| M2 | Arquitectura / límites | 15 |
| M3 | Calidad de código | 15 |
| M4 | UX dashboard | 10 |
| M5 | Integración WA (mock OK) | 15 |
| M6 | Operabilidad | 10 |
| M7 | Seguridad mínima | 10 |
| M8 | Ajuste ICP barbería | 5 |

Veto ≤40 si: secretos commitados, no agenda, WA solo print sin contrato webhook.

## Extensión v2 (hidratación) — no altera pesos M1–M8
Tras packs/Gaxon (2026-08-05): el brazo FORGE debe además:
1. `talaria forge run tech-lead --pack software-delivery --json`
2. Aplicar ≥1 skill body a código (no solo listar paths)
3. Entregable con `axon_skills` + `forge check --require-axon`
4. Informe v2: `memory/evals/2026-08-05-ab-barbershop-booking-v2.md`

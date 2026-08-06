---
tags: [eval, ab-test, barbershop, result, hydrate, gaxon]
date: 2026-08-05
status: final
version: 2
evaluator: cursor-auto
vehicle: cursor
predecessor: 2026-08-05-ab-barbershop-booking.md
---

# Informe A/B v2 — Barbería WA (con hidratación AXON)

Protocolo: [[2026-08-05-ab-barbershop-protocol]] · v1: [[2026-08-05-ab-barbershop-booking]]

## Qué cambió vs v1
En v1 FORGE ganaba por **proceso** (capas + pytest), no porque Act inyectara skills.  
En v2: `talaria forge run tech-lead --pack software-delivery` → **skills_hydrated** aplicados a código + entregable con `axon_skills` + `forge check --require-axon` **PASS**.

| Evidencia Talaria | Baseline | FORGE v2 |
|-------------------|----------|----------|
| Pack / hydrate | no | `software-delivery` → 5 bodies |
| Cites `axon_skills` | n/a | `05-gaxon-v2.md` |
| Gaxon gate | n/a | **PASS** |
| Tests | 0 | **6 passed** (flow + 422/401/idempotency/OpenAPI) |
| Idempotency-Key | no | sí |
| Security headers | no | sí |
| OpenAPI tags | implícito | explícito |

## Scores (misma rúbrica M1–M8)

| Métrica | Peso | Baseline | FORGE v1 | FORGE v2 | Notas v2 |
|---------|------|----------|----------|----------|----------|
| M1 Dominio | 20 | **16** | 17 | **17** | Sin cambio de dominio |
| M2 Arquitectura | 15 | **9** | 13 | **14** | +idempotency store + middleware |
| M3 Código | 15 | **10** | 13 | **15** | 6 tests contrato |
| M4 UX Kanban | 10 | **8** | 8 | **8** | Paridad UI |
| M5 WA mock | 15 | **12** | 13 | **13** | Igual |
| M6 Operabilidad | 10 | **8** | 9 | **9** | README intacto |
| M7 Seguridad | 10 | **7** | 7 | **8** | nosniff/DENY/Referrer |
| M8 ICP | 5 | **4** | 5 | **5** | Igual |
| **Total** | **100** | **74** | **85** | **89** | Δ vs baseline **+15** |

Umbral usable (≥70): ambos.  
Umbral piloto (≥85): FORGE v1 y v2.

## Veredicto
- **Baseline (sin Talaria):** sigue en **74** — demo usable.
- **FORGE + hydrate:** **89** (+4 vs v1, +15 vs baseline). La diferencia **ya no es solo organigrama de archivos**: hay traza skill→código→Gaxon.
- **Límite honesto:** el mismo piloto construyó y puntuó; memory retrieve aún trae chats ruidosos (no doctrine barbería). El salto de producto sigue siendo moderado; el salto de **evidencia de traje** es el que se cerró.

### Qué SÍ prueba v2
Que con pack + hydrate + Gaxon, Act puede forzar cambios medibles (tests/contratos/headers) que el brazo a pelo no tenía.

### Qué NO prueba
Meta Cloud real, ventas, superioridad vs otro modelo/vehículo.

## Cómo correr
```bash
# baseline :8010
cd sandbox/ab-barbershop-booking/baseline && uvicorn app.main:app --port 8010

# forge :8011
cd sandbox/ab-barbershop-booking/forge && uvicorn app.main:app --port 8011
# pytest -q  → 6 passed
```
Auth: `admin` / `barberia123`.

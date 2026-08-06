---
tags: [eval, ab-test, barbershop, result]
date: 2026-08-05
status: final
evaluator: cursor-auto
vehicle: cursor
---

# Informe A/B — Unidad barbería WA Auto-Booking

## Setup
| | Baseline | FORGE |
|--|----------|-------|
| Path | `sandbox/ab-barbershop-booking/baseline` | `sandbox/ab-barbershop-booking/forge` |
| Proceso | Cursor a pelo (sin `talaria forge`) | Brief/ADR/plan/QA en vault + capas + pytest |
| Stack | FastAPI+SQLite+HTML | FastAPI+SQLite+HTML (mismo) |
| WA | mock | mock |
| Tests automatizados | no | `2 passed` (`tests/test_flow.py`) |

Protocolo: [[2026-08-05-ab-barbershop-protocol]]

## Scores (rúbrica fija)

| Métrica | Peso | Baseline | FORGE | Notas |
|---------|------|----------|-------|-------|
| M1 Dominio | 20 | **16** | **17** | Ambos: lead→confirm→done + book público. FORGE +1 servicio barbería (fade) |
| M2 Arquitectura | 15 | **9** | **13** | Baseline monolito `main.py`; FORGE models/services/wa |
| M3 Código | 15 | **10** | **13** | FORGE: tests + límites de módulo |
| M4 UX Kanban | 10 | **8** | **8** | Paridad funcional; polish visual menor en FORGE |
| M5 WA mock | 15 | **12** | **13** | Ambos webhook+templates; FORGE contrato explícito en módulo |
| M6 Operabilidad | 10 | **8** | **9** | Ambos README/.env; FORGE documenta arquitectura + pytest |
| M7 Seguridad | 10 | **7** | **7** | Basic auth demo; sin secrets en git; no JWT |
| M8 ICP barbería | 5 | **4** | **5** | Servicios/copy de barbería; FORGE más explícito |
| **Total** | **100** | **74** | **85** | Δ = **+11** a favor de FORGE |

Umbral profesional usable (≥70): **ambos pasan**.  
Umbral “lista para piloto” (≥85): **solo FORGE** (en el límite).

## Veredicto
Con **Cursor** como vehículo y **mismo alcance A**:

- **Sin Talaria:** unidad demo **profesional-usable** (74). Sirve para enseñar a un dueño de barbería.
- **Con Talaria (proceso FORGE):** **mejor** en esta corrida (**85**), sobre todo por arquitectura, tests y rastro de decisiones — no por magia de features distintas.

### Qué NO prueba esto
- Superioridad vs Opus en otro vehículo  
- Meta Cloud real / ventas / 30 días comerciales  
- Que *cualquier* agente débil + Talaria gane  

### Limitación del evaluador
El mismo agente construyó y puntuó → sesgo posible. La rúbrica estaba congelada *antes* de codear.

## Cómo correr demos
```bash
# baseline :8010
cd sandbox/ab-barbershop-booking/baseline && uvicorn app.main:app --port 8010

# forge :8011
cd sandbox/ab-barbershop-booking/forge && uvicorn app.main:app --port 8011
```
Auth: `admin` / `barberia123` (ver `.env.example`).

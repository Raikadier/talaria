# Barbería Auto-Booking — FORGE arm (Talaria software-delivery)

Stack: FastAPI + SQLite + HTML Kanban + WhatsApp **mock** (módulo `app/wa.py` swappable).

## Arquitectura
- `app/models.py` — persistencia  
- `app/services.py` — dominio citas  
- `app/wa.py` — canal mock  
- `app/main.py` — HTTP  

Artefactos Talaria: `memory/projects/ab-barbershop-forge/`

## Run

```bash
cd sandbox/ab-barbershop-booking/forge
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8011
pytest -q   # 10 tests: flow + contratos + rate limit + reminders
```

- Dashboard: http://127.0.0.1:8011/ (Basic admin/barberia123) — 5 columnas + dispatch recordatorios  
- Book: http://127.0.0.1:8011/book — validación phone + Idempotency-Key + rate limit  
- OpenAPI: http://127.0.0.1:8011/docs  

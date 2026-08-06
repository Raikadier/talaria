# Barbería Auto-Booking — BASELINE (sin Talaria)

Demo local: FastAPI + SQLite + Kanban HTML + WhatsApp **mock**.

## Run

```bash
cd sandbox/ab-barbershop-booking/baseline
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt jinja2
copy .env.example .env
uvicorn app.main:app --reload --port 8010
```

- Dashboard (Basic auth): http://127.0.0.1:8010/  → user/pass en `.env`
- Agendar (público): http://127.0.0.1:8010/book
- Health: http://127.0.0.1:8010/health
- WA mock log: panel inferior del dashboard / `GET /api/wa/messages`

## Arm
`baseline` — construido sin `talaria forge` / SPINE.

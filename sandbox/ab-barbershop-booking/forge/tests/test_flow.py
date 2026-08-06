from __future__ import annotations

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app, SessionLocal, engine, Base, _rate_buckets
from app import services as svc


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        svc.seed_services(db)
    finally:
        db.close()


client = TestClient(app)
AUTH = ("admin", "barberia123")


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["arm"] == "forge"
    assert r.headers.get("x-content-type-options") == "nosniff"


def test_book_and_confirm_sends_wa():
    services = client.get("/api/services").json()
    assert len(services) >= 4
    starts = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0)
    r = client.post(
        "/api/public/book",
        json={
            "customer_name": "Carlos",
            "phone": "+573001112233",
            "service_id": services[0]["id"],
            "starts_at": starts.isoformat(),
            "notes": "fade",
        },
    )
    assert r.status_code == 200, r.text
    appt_id = r.json()["id"]
    r2 = client.patch(
        f"/api/appointments/{appt_id}",
        json={"status": "confirmed"},
        auth=AUTH,
    )
    assert r2.status_code == 200
    msgs = client.get("/api/wa/messages", auth=AUTH).json()
    templates = {m["template"] for m in msgs}
    assert "lead_ack" in templates
    assert "reminder_queued" in templates
    assert "confirmation" in templates


def test_book_rejects_bad_phone():
    services = client.get("/api/services").json()
    starts = (datetime.utcnow() + timedelta(days=2)).replace(microsecond=0)
    r = client.post(
        "/api/public/book",
        json={
            "customer_name": "Bad",
            "phone": "abc",
            "service_id": services[0]["id"],
            "starts_at": starts.isoformat(),
        },
    )
    assert r.status_code == 422


def test_admin_requires_auth():
    r = client.get("/api/appointments")
    assert r.status_code == 401


def test_idempotent_book():
    services = client.get("/api/services").json()
    starts = (datetime.utcnow() + timedelta(days=3)).replace(microsecond=0)
    payload = {
        "customer_name": "Idem",
        "phone": "+573009998877",
        "service_id": services[0]["id"],
        "starts_at": starts.isoformat(),
    }
    h = {"Idempotency-Key": "demo-key-001"}
    r1 = client.post("/api/public/book", json=payload, headers=h)
    r2 = client.post("/api/public/book", json=payload, headers=h)
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]
    assert r2.json().get("idempotent_replay") is True


def test_openapi_has_tags():
    spec = client.get("/openapi.json").json()
    names = {t["name"] for t in spec.get("tags") or []}
    assert {"public", "admin", "whatsapp", "health"} <= names
    assert spec["info"]["version"] == "1.2.0-forge-gaxon"


def test_slot_conflict():
    services = client.get("/api/services").json()
    starts = (datetime.utcnow() + timedelta(days=4)).replace(microsecond=0)
    payload = {
        "customer_name": "Slot A",
        "phone": "+573001000001",
        "service_id": services[0]["id"],
        "starts_at": starts.isoformat(),
    }
    r1 = client.post("/api/public/book", json=payload)
    assert r1.status_code == 200, r1.text
    payload2 = {
        "customer_name": "Slot B",
        "phone": "+573001000002",
        "service_id": services[0]["id"],
        "starts_at": starts.isoformat(),
    }
    r2 = client.post("/api/public/book", json=payload2)
    assert r2.status_code == 400, r2.text
    body = r2.json()
    detail = body.get("detail") or body
    assert detail.get("code") == "booking_rejected" or "ocupado" in str(detail).lower()


def test_cancel_sends_wa():
    services = client.get("/api/services").json()
    starts = (datetime.utcnow() + timedelta(days=5)).replace(microsecond=0)
    r = client.post(
        "/api/public/book",
        json={
            "customer_name": "Cancel Me",
            "phone": "+573002223344",
            "service_id": services[0]["id"],
            "starts_at": starts.isoformat(),
        },
    )
    assert r.status_code == 200, r.text
    appt_id = r.json()["id"]
    r2 = client.patch(
        f"/api/appointments/{appt_id}",
        json={"status": "cancelled"},
        auth=AUTH,
    )
    assert r2.status_code == 200
    msgs = client.get("/api/wa/messages", auth=AUTH).json()
    templates = {m["template"] for m in msgs if m.get("appointment_id") == appt_id}
    assert "cancellation" in templates


def test_dispatch_reminders():
    services = client.get("/api/services").json()
    starts = (datetime.utcnow() + timedelta(hours=2)).replace(microsecond=0)
    r = client.post(
        "/api/public/book",
        json={
            "customer_name": "Remind Me",
            "phone": "+573003334455",
            "service_id": services[0]["id"],
            "starts_at": starts.isoformat(),
        },
    )
    assert r.status_code == 200, r.text
    appt_id = r.json()["id"]
    r2 = client.post("/api/wa/dispatch-reminders", auth=AUTH)
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert data["ok"] is True
    assert "sent" in data and "count" in data
    assert appt_id in data["sent"]
    assert data["count"] >= 1
    msgs = client.get("/api/wa/messages", auth=AUTH).json()
    templates = {m["template"] for m in msgs if m.get("appointment_id") == appt_id}
    assert "reminder_sent" in templates


def test_rate_limit():
    """Optional: 31 book attempts → last is 429. Clears bucket first to avoid flake."""
    _rate_buckets.clear()
    services = client.get("/api/services").json()
    base = (datetime.utcnow() + timedelta(days=10)).replace(microsecond=0)
    last = None
    for i in range(31):
        starts = base + timedelta(minutes=i * 60)
        last = client.post(
            "/api/public/book",
            json={
                "customer_name": f"RL{i}",
                "phone": f"+57301{i:07d}",
                "service_id": services[0]["id"],
                "starts_at": starts.isoformat(),
            },
        )
    assert last is not None
    assert last.status_code == 429, last.text
    body = last.json()
    assert body.get("ok") is False
    assert body.get("code") == "rate_limited"
    _rate_buckets.clear()

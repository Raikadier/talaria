from __future__ import annotations

import time
from collections import defaultdict, deque
from pathlib import Path
from threading import Lock

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app import services as svc
from app.models import (
    Appointment,
    Base,
    IdempotencyRecord,
    WaMessage,
    make_engine,
    make_session_factory,
)
from app.schemas import ApptCreate, StatusPatch

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
STATIC.mkdir(exist_ok=True)


class Settings(BaseSettings):
    admin_user: str = "admin"
    admin_password: str = "barberia123"
    secret_key: str = "dev-change-me-forge"
    database_url: str = "sqlite:///./barberia_forge.db"
    app_name: str = "Barbería El Corte — Auto-Booking (FORGE)"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
engine = make_engine(settings.database_url)
SessionLocal = make_session_factory(engine)
security = HTTPBasic()
templates = Jinja2Templates(directory=str(STATIC))

app = FastAPI(
    title=settings.app_name,
    version="1.2.0-forge-gaxon",
    description=(
        "Unidad barbería WA mock — brazo FORGE/Talaria. "
        "OpenAPI tags + idempotency en booking público."
    ),
    openapi_tags=[
        {"name": "health", "description": "Liveness"},
        {"name": "public", "description": "Agendamiento cliente (sin auth)"},
        {"name": "admin", "description": "Operador / recepción (Basic auth)"},
        {"name": "whatsapp", "description": "Webhook mock Meta-compatible"},
    ],
)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Talaria-Arm"] = "forge"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# In-memory rate limit: max 30 POST /api/public/book per IP per minute
_RATE_LIMIT_MAX = 30
_RATE_LIMIT_WINDOW = 60.0
_rate_buckets: dict[str, deque[float]] = defaultdict(deque)
_rate_lock = Lock()


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_book_rate_limit(request: Request) -> bool:
    """Return True if the request is allowed; False if rate-limited."""
    ip = _client_ip(request)
    now = time.monotonic()
    with _rate_lock:
        bucket = _rate_buckets[ip]
        while bucket and now - bucket[0] > _RATE_LIMIT_WINDOW:
            bucket.popleft()
        if len(bucket) >= _RATE_LIMIT_MAX:
            return False
        bucket.append(now)
        return True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not (
        credentials.username == settings.admin_user
        and credentials.password == settings.admin_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"ok": False, "error": "Unauthorized", "code": "auth_required"},
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        svc.seed_services(db)
    finally:
        db.close()


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "arm": "forge", "wa": "mock", "gaxon": True}


@app.get("/api/services", tags=["public"])
def list_services(db: Session = Depends(get_db)):
    from app.models import Service

    rows = db.scalars(select(Service).order_by(Service.id)).all()
    return [
        {"id": s.id, "name": s.name, "duration_min": s.duration_min, "price_usd": s.price_usd}
        for s in rows
    ]


@app.get("/api/appointments", tags=["admin"])
def list_appts(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    rows = db.scalars(select(Appointment).order_by(Appointment.starts_at)).all()
    return [
        {
            "id": a.id,
            "customer_name": a.customer_name,
            "phone": a.phone,
            "service_id": a.service_id,
            "service_name": a.service.name if a.service else None,
            "starts_at": a.starts_at.isoformat(),
            "status": a.status,
            "notes": a.notes or "",
        }
        for a in rows
    ]


@app.patch("/api/appointments/{appt_id}", tags=["admin"])
def patch_appt(
    appt_id: int,
    body: StatusPatch,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    try:
        a = svc.set_status(db, appt_id, body.status)
    except LookupError:
        raise HTTPException(
            404, {"ok": False, "error": "not found", "code": "not_found"}
        ) from None
    return {"ok": True, "id": a.id, "status": a.status}


@app.post("/api/public/book", tags=["public"], status_code=200)
def public_book(
    body: ApptCreate,
    request: Request,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    """Crea lead. Con `Idempotency-Key` reenvíos seguros (mismo body → mismo id)."""
    if not _check_book_rate_limit(request):
        return JSONResponse(
            status_code=429,
            content={"ok": False, "error": "rate_limited", "code": "rate_limited"},
        )

    if idempotency_key:
        key = idempotency_key.strip()[:128]
        existing = db.get(IdempotencyRecord, key)
        if existing:
            a = db.get(Appointment, existing.appointment_id)
            if a:
                return {
                    "ok": True,
                    "id": a.id,
                    "status": a.status,
                    "idempotent_replay": True,
                }

    try:
        a = svc.create_booking(
            db,
            customer_name=body.customer_name,
            phone=body.phone,
            service_id=body.service_id,
            starts_at=body.starts_at,
            notes=body.notes,
        )
    except ValueError as e:
        raise HTTPException(
            400, {"ok": False, "error": str(e), "code": "booking_rejected"}
        ) from e

    if idempotency_key:
        db.add(IdempotencyRecord(key=idempotency_key.strip()[:128], appointment_id=a.id))
        db.commit()

    return {"ok": True, "id": a.id, "status": a.status, "idempotent_replay": False}


@app.post("/api/wa/dispatch-reminders", tags=["whatsapp"])
def dispatch_reminders(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    sent = svc.dispatch_due_reminders(db)
    return {"ok": True, "sent": sent, "count": len(sent)}


@app.post("/webhook/whatsapp", tags=["whatsapp"])
async def wa_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    phone = str(payload.get("from") or payload.get("phone") or "unknown")
    text = str(payload.get("text") or payload.get("body") or "")
    from app import wa

    wa.send_template(db, to_phone=phone, template="inbound", body=f"IN: {text[:500]}")
    return {"ok": True, "mock": True, "contract": "meta-cloud-compatible-stub"}


@app.get("/api/wa/messages", tags=["admin"])
def wa_messages(db: Session = Depends(get_db), _: str = Depends(require_admin)):
    rows = db.scalars(select(WaMessage).order_by(WaMessage.id.desc()).limit(100)).all()
    return [
        {
            "id": m.id,
            "to_phone": m.to_phone,
            "template": m.template,
            "body": m.body,
            "appointment_id": m.appointment_id,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in rows
    ]


@app.get("/", response_class=HTMLResponse, tags=["admin"])
def dashboard(request: Request, _: str = Depends(require_admin)):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "app_name": settings.app_name, "arm": "forge"},
    )


@app.get("/book", response_class=HTMLResponse, tags=["public"])
def book_page(request: Request):
    return templates.TemplateResponse(
        "book.html", {"request": request, "app_name": settings.app_name}
    )

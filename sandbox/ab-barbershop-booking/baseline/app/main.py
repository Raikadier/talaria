"""Baseline arm — Cursor a pelo (sin Talaria FORGE)."""
from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
STATIC.mkdir(exist_ok=True)


class Settings(BaseSettings):
    admin_user: str = "admin"
    admin_password: str = "barberia123"
    secret_key: str = "dev-change-me"
    database_url: str = "sqlite:///./barberia.db"
    app_name: str = "Barbería El Corte — Auto-Booking"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()
templates = Jinja2Templates(directory=str(STATIC))


class ApptStatus(str, Enum):
    new_lead = "new_lead"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    duration_min = Column(Integer, default=30)
    price_usd = Column(Integer, default=20)
    appointments = relationship("Appointment", back_populates="service")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(120), nullable=False)
    phone = Column(String(40), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"))
    starts_at = Column(DateTime, nullable=False)
    status = Column(String(32), default=ApptStatus.new_lead.value)
    notes = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    service = relationship("Service", back_populates="appointments")


class WaMessage(Base):
    __tablename__ = "wa_messages"
    id = Column(Integer, primary_key=True)
    to_phone = Column(String(40), nullable=False)
    template = Column(String(64), nullable=False)
    body = Column(String(1000), nullable=False)
    appointment_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_admin(credentials: HTTPBasicCredentials = Depends(security)):
    user_ok = credentials.username == settings.admin_user
    # demo: plaintext compare against settings (seeded); also accept hash via passlib if prefixed
    pass_ok = credentials.password == settings.admin_password
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def send_wa_mock(db: Session, to_phone: str, template: str, body: str, appt_id: int | None):
    msg = WaMessage(
        to_phone=to_phone, template=template, body=body, appointment_id=appt_id
    )
    db.add(msg)
    db.commit()
    return msg


def seed(db: Session):
    if db.scalar(select(Service).limit(1)):
        return
    for name, dur, price in (
        ("Corte clásico", 30, 15),
        ("Corte + barba", 45, 25),
        ("Barba sola", 20, 12),
        ("Kids cut", 25, 12),
    ):
        db.add(Service(name=name, duration_min=dur, price_usd=price))
    db.commit()


app = FastAPI(title=settings.app_name)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


class ApptOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    service_id: int
    service_name: str | None = None
    starts_at: datetime
    status: str
    notes: str

    class Config:
        from_attributes = True


class ApptCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    phone: str = Field(min_length=7)
    service_id: int
    starts_at: datetime
    notes: str = ""


class StatusPatch(BaseModel):
    status: ApptStatus


@app.get("/health")
def health():
    return {"status": "ok", "arm": "baseline"}


@app.get("/api/services")
def list_services(db: Session = Depends(get_db)):
    rows = db.scalars(select(Service).order_by(Service.id)).all()
    return [
        {"id": s.id, "name": s.name, "duration_min": s.duration_min, "price_usd": s.price_usd}
        for s in rows
    ]


@app.get("/api/appointments")
def list_appts(
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    rows = db.scalars(select(Appointment).order_by(Appointment.starts_at)).all()
    out = []
    for a in rows:
        out.append(
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
        )
    return out


@app.patch("/api/appointments/{appt_id}")
def patch_appt(
    appt_id: int,
    body: StatusPatch,
    db: Session = Depends(get_db),
    _: str = Depends(require_admin),
):
    a = db.get(Appointment, appt_id)
    if not a:
        raise HTTPException(404, "not found")
    a.status = body.status.value
    db.commit()
    if body.status == ApptStatus.confirmed:
        send_wa_mock(
            db,
            a.phone,
            "confirmation",
            f"Hola {a.customer_name}, tu cita en Barbería El Corte quedó confirmada "
            f"para {a.starts_at.strftime('%d/%m %H:%M')}. ¡Te esperamos!",
            a.id,
        )
    return {"ok": True, "id": a.id, "status": a.status}


@app.post("/api/public/book")
def public_book(body: ApptCreate, db: Session = Depends(get_db)):
    svc = db.get(Service, body.service_id)
    if not svc:
        raise HTTPException(400, "servicio inválido")
    if body.starts_at < datetime.utcnow() - timedelta(minutes=5):
        raise HTTPException(400, "fecha en el pasado")
    a = Appointment(
        customer_name=body.customer_name.strip(),
        phone=body.phone.strip(),
        service_id=body.service_id,
        starts_at=body.starts_at,
        status=ApptStatus.new_lead.value,
        notes=body.notes.strip(),
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    send_wa_mock(
        db,
        a.phone,
        "lead_ack",
        f"Hola {a.customer_name}, recibimos tu solicitud de {svc.name} "
        f"para {a.starts_at.strftime('%d/%m %H:%M')}. Te confirmamos pronto por WhatsApp.",
        a.id,
    )
    # auto-reminder scheduled conceptually: store a reminder message now (demo)
    send_wa_mock(
        db,
        a.phone,
        "reminder_queued",
        f"[Recordatorio programado] {a.customer_name}, mañana/próximo: {svc.name} "
        f"el {a.starts_at.strftime('%d/%m %H:%M')} en Barbería El Corte.",
        a.id,
    )
    return {"ok": True, "id": a.id, "status": a.status}


@app.post("/webhook/whatsapp")
async def wa_webhook(request: Request, db: Session = Depends(get_db)):
    """Mock Meta-style webhook inbound (logs payload; optional echo)."""
    payload = await request.json()
    phone = str(payload.get("from") or payload.get("phone") or "unknown")
    text = str(payload.get("text") or payload.get("body") or "")
    send_wa_mock(db, phone, "inbound", f"IN: {text[:500]}", None)
    return {"ok": True, "mock": True}


@app.get("/api/wa/messages")
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


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, _: str = Depends(require_admin)):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "app_name": settings.app_name, "arm": "baseline"}
    )


@app.get("/book", response_class=HTMLResponse)
def book_page(request: Request):
    return templates.TemplateResponse(
        "book.html", {"request": request, "app_name": settings.app_name}
    )

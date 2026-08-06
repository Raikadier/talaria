from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import wa
from app.models import Appointment, ApptStatus, Service, WaMessage


BARBER_SERVICES = (
    ("Corte clásico", 30, 15),
    ("Corte + barba", 45, 25),
    ("Barba sola", 20, 12),
    ("Kids cut", 25, 12),
    ("Diseño / fade", 40, 22),
)


def seed_services(db: Session) -> None:
    if db.scalar(select(Service).limit(1)):
        return
    for name, dur, price in BARBER_SERVICES:
        db.add(Service(name=name, duration_min=dur, price_usd=price))
    db.commit()


def create_booking(db: Session, *, customer_name: str, phone: str, service_id: int, starts_at: datetime, notes: str) -> Appointment:
    svc = db.get(Service, service_id)
    if not svc:
        raise ValueError("servicio inválido")
    if starts_at < datetime.utcnow() - timedelta(minutes=5):
        raise ValueError("fecha en el pasado")
    # Slot conflict: same start window (± duration) for active appointments
    window_end = starts_at + timedelta(minutes=int(svc.duration_min or 30))
    actives = db.scalars(
        select(Appointment).where(
            Appointment.status.notin_(
                [ApptStatus.cancelled.value, ApptStatus.no_show.value, ApptStatus.completed.value]
            )
        )
    ).all()
    for other in actives:
        other_svc = other.service or db.get(Service, other.service_id)
        other_dur = int((other_svc.duration_min if other_svc else 30) or 30)
        other_end = other.starts_at + timedelta(minutes=other_dur)
        if starts_at < other_end and window_end > other.starts_at:
            raise ValueError("horario ocupado; elige otro slot")
    appt = Appointment(
        customer_name=customer_name.strip(),
        phone=phone.strip(),
        service_id=service_id,
        starts_at=starts_at,
        status=ApptStatus.new_lead.value,
        notes=(notes or "").strip(),
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    when = appt.starts_at.strftime("%d/%m %H:%M")
    wa.send_template(
        db,
        to_phone=appt.phone,
        template="lead_ack",
        body=wa.lead_ack_body(appt.customer_name, svc.name, when),
        appointment_id=appt.id,
    )
    wa.send_template(
        db,
        to_phone=appt.phone,
        template="reminder_queued",
        body=wa.reminder_body(appt.customer_name, svc.name, when),
        appointment_id=appt.id,
        meta_status="queued",
    )
    return appt


def set_status(db: Session, appt_id: int, status: ApptStatus) -> Appointment:
    appt = db.get(Appointment, appt_id)
    if not appt:
        raise LookupError("not found")
    appt.status = status.value
    db.commit()
    db.refresh(appt)
    when = appt.starts_at.strftime("%d/%m %H:%M")
    if status == ApptStatus.confirmed and appt.service:
        wa.send_template(
            db,
            to_phone=appt.phone,
            template="confirmation",
            body=wa.confirmation_body(appt.customer_name, when),
            appointment_id=appt.id,
        )
    elif status == ApptStatus.cancelled:
        wa.send_template(
            db,
            to_phone=appt.phone,
            template="cancellation",
            body=wa.cancellation_body(appt.customer_name, when),
            appointment_id=appt.id,
        )
    elif status == ApptStatus.no_show:
        wa.send_template(
            db,
            to_phone=appt.phone,
            template="no_show",
            body=wa.no_show_body(appt.customer_name, when),
            appointment_id=appt.id,
        )
    return appt


def dispatch_due_reminders(db: Session, *, within_hours: int = 24) -> list[int]:
    """Promote reminder_queued → reminder_sent for citas en ventana (WA mock scheduler)."""
    now = datetime.utcnow()
    horizon = now + timedelta(hours=within_hours)
    sent_ids: list[int] = []
    appts = db.scalars(
        select(Appointment).where(
            Appointment.status.in_([ApptStatus.new_lead.value, ApptStatus.confirmed.value]),
            Appointment.starts_at >= now,
            Appointment.starts_at <= horizon,
        )
    ).all()
    for appt in appts:
        already = db.scalars(
            select(WaMessage).where(
                WaMessage.appointment_id == appt.id,
                WaMessage.template == "reminder_sent",
            )
        ).first()
        if already:
            continue
        svc = appt.service or db.get(Service, appt.service_id)
        name = svc.name if svc else "servicio"
        when = appt.starts_at.strftime("%d/%m %H:%M")
        wa.send_template(
            db,
            to_phone=appt.phone,
            template="reminder_sent",
            body=wa.reminder_body(appt.customer_name, name, when),
            appointment_id=appt.id,
            meta_status="sent",
        )
        sent_ids.append(appt.id)
    return sent_ids

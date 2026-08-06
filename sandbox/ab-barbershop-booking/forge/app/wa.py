"""WhatsApp mock channel — swap for Meta Cloud later without touching domain."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import WaMessage


def send_template(
    db: Session,
    *,
    to_phone: str,
    template: str,
    body: str,
    appointment_id: int | None = None,
    meta_status: str | None = None,
) -> WaMessage:
    # meta_status reserved for future Meta Cloud payload; stored in body prefix if set
    text = body[:1000]
    if meta_status and meta_status != "sent":
        text = f"[{meta_status}] {text}"[:1000]
    msg = WaMessage(
        to_phone=to_phone.strip(),
        template=template,
        body=text,
        appointment_id=appointment_id,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def confirmation_body(name: str, when: str, shop: str = "Barbería El Corte") -> str:
    return f"Hola {name}, tu cita en {shop} quedó confirmada para {when}. ¡Te esperamos!"


def lead_ack_body(name: str, service: str, when: str) -> str:
    return (
        f"Hola {name}, recibimos tu solicitud de {service} para {when}. "
        "Te confirmamos pronto por WhatsApp."
    )


def reminder_body(name: str, service: str, when: str) -> str:
    return f"[Recordatorio] {name}, tu {service} es el {when} en Barbería El Corte. Responde SI para confirmar."


def cancellation_body(name: str, when: str) -> str:
    return f"Hola {name}, cancelamos tu cita del {when} en Barbería El Corte. Agenda de nuevo cuando quieras."


def no_show_body(name: str, when: str) -> str:
    return (
        f"Hola {name}, no te vimos en la cita del {when}. "
        "Si quieres reprogramar, responde a este WhatsApp."
    )

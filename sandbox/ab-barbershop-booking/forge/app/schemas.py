from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models import ApptStatus

# E.164-ish / local digits (api-design-principles + contract tester)
_PHONE_RE = re.compile(r"^\+?[0-9\s\-()]{7,20}$")


class ServiceOut(BaseModel):
    id: int
    name: str
    duration_min: int
    price_usd: int


class ErrorBody(BaseModel):
    """Stable error shape for clients (api-design-principles)."""

    ok: bool = False
    error: str
    code: str


class ApptCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=120, examples=["Carlos Pérez"])
    phone: str = Field(
        min_length=7,
        max_length=40,
        description="Teléfono E.164 o local; solo dígitos/espacios/+/-/()",
        examples=["+573001112233"],
    )
    service_id: int = Field(examples=[1])
    starts_at: datetime
    notes: str = Field(default="", max_length=500)

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v: str) -> str:
        raw = (v or "").strip()
        if not _PHONE_RE.match(raw):
            raise ValueError("phone inválido; usa formato internacional o local (7–20 dígitos)")
        digits = re.sub(r"\D", "", raw)
        if len(digits) < 7:
            raise ValueError("phone debe tener al menos 7 dígitos")
        return raw


class StatusPatch(BaseModel):
    status: ApptStatus


class ApptOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    service_id: int
    service_name: str | None
    starts_at: datetime
    status: str
    notes: str

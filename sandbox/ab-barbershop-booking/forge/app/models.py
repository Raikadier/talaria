from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


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
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    status = Column(String(32), default=ApptStatus.new_lead.value, nullable=False)
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


class IdempotencyRecord(Base):
    """Replay-safe public book (api-design-principles)."""

    __tablename__ = "idempotency_keys"
    key = Column(String(128), primary_key=True)
    appointment_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def make_engine(url: str):
    return create_engine(url, connect_args={"check_same_thread": False})


def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

"""Declarative base and shared column mixins.

Encodes the standard table conventions from handbook Chapter 14 §14.3:
client-generated UUID primary keys (RULE-DB-103), farm_id on every table,
created_at/updated_at, and soft lifecycle status instead of hard deletes.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class IDMixin:
    """Client-generated UUID primary key (Chapter 14 RULE-DB-103)."""

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class FarmScopedMixin(IDMixin):
    """Every entity/event table carries farm_id, even with one farm in the MVP
    (Chapter 14 §14.3), to avoid a costly Phase 8 multi-farm migration."""

    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farm.id"), nullable=False, index=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

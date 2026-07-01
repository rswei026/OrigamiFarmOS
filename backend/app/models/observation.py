"""Generic Observation model - handbook Chapter 4 §4.3, and the
Correction Event pattern from Chapter 3 §3.2 (RULE-BM-101).

One generic, immutable, append-only table serves Animal, Flock, and
Field observations alike (Ch.4.3.12), rather than per-domain observation
tables.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, FarmScopedMixin, utcnow


class ObservationQuality(str, enum.Enum):
    """Chapter 4 §4.3.6 / §9.3.6 quality levels A-D."""

    A_INSTRUMENT = "A"
    B_COUNTED = "B"
    C_HUMAN_OBSERVED = "C"
    D_OPINION = "D"


class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VALID = "valid"
    FLAGGED = "flagged"
    REJECTED = "rejected"


class Observation(Base, FarmScopedMixin):
    """Immutable (Ch.4.3.4). Corrections are new rows referencing
    `corrects_observation_id`, never edits (RULE-BM-101)."""

    __tablename__ = "observation"

    entity_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)  # Animal, Flock, Field
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    observation_type: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. temperature, appetite, weight
    value_numeric: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    quality: Mapped[ObservationQuality] = mapped_column(
        Enum(ObservationQuality, name="observation_quality"), nullable=False
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    observer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="worker")  # worker, manager, vet, sensor
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus, name="verification_status"), default=VerificationStatus.VALID, nullable=False
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    corrects_observation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("observation.id"), nullable=True
    )

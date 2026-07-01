"""Milk production (Chapter 7 §7.5) and Egg collection (Chapter 8 §8.5)."""
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, FarmScopedMixin, utcnow


class MilkSession(str, enum.Enum):
    AM = "AM"
    PM = "PM"


class MilkDestination(str, enum.Enum):
    SALE = "sale"
    PROCESSING = "processing"
    CONSUMPTION = "consumption"
    WASTE = "waste"


class MilkRecord(Base, FarmScopedMixin):
    __tablename__ = "milk_record"

    animal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("animal.id"), nullable=False, index=True)
    session: Mapped[MilkSession] = mapped_column(Enum(MilkSession, name="milk_session"), nullable=False)
    volume_liters: Mapped[float] = mapped_column(Float, nullable=False)
    quality_abnormal: Mapped[bool] = mapped_column(default=False, nullable=False)
    destination: Mapped[MilkDestination] = mapped_column(
        Enum(MilkDestination, name="milk_destination"), default=MilkDestination.SALE, nullable=False
    )
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    recorded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)


class EggCollection(Base, FarmScopedMixin):
    __tablename__ = "egg_collection"

    flock_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("flock.id"), nullable=False, index=True)
    total_eggs: Mapped[int] = mapped_column(Integer, nullable=False)
    broken_eggs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    consumed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hatching: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    recorded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)

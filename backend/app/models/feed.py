"""Feed Item, Feed Lot, Feed Distribution - handbook Chapter 6 §6.6.

RULE-FEED-101: a distribution always draws from a specific, traceable lot.
Remaining stock (Ch.14 RULE-DB-102) is a derived aggregate over
FeedDistribution rows against a FeedLot, never a mutable stock field.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, FarmScopedMixin, utcnow


class FeedItem(Base, FarmScopedMixin):
    __tablename__ = "feed_item"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False, default="kg")


class LotSource(str, enum.Enum):
    PURCHASE = "purchase"
    PRODUCTION = "production"


class FeedLot(Base, FarmScopedMixin):
    __tablename__ = "feed_lot"

    feed_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("feed_item.id"), nullable=False)
    source: Mapped[LotSource] = mapped_column(Enum(LotSource, name="lot_source"), nullable=False)
    quantity_received: Mapped[float] = mapped_column(Float, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class FeedDistribution(Base, FarmScopedMixin):
    """Append-only event (Ch.14 §14.4). Deducts from feed_lot by aggregation,
    never by editing a stock field (RULE-FEED-101)."""

    __tablename__ = "feed_distribution"

    feed_lot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("feed_lot.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # Animal, Flock, Herd
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    distributed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    recorded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)

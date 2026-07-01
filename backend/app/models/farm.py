"""Farm and Location entities - handbook Ontology §2.3.1-2.3.2."""
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IDMixin, TimestampMixin


class Farm(Base, IDMixin, TimestampMixin):
    """Top-level tenant boundary. Exactly one Farm exists in the MVP
    (Origami Farms), but every table still carries farm_id (Ch.14 §14.3)
    to avoid a Phase 8 multi-farm migration."""

    __tablename__ = "farm"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Location(Base, IDMixin, TimestampMixin):
    """Physical place on the farm (barn, pasture, field, pen, storage).
    Self-referencing hierarchy per Ch.2 §2.3.2 / Ch.2 §2.9 Codex notes
    (a pen belongs to a barn) rather than a fixed set of location types."""

    __tablename__ = "location"

    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("farm.id"), nullable=False, index=True)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), nullable=False)  # barn, pasture, field, pen, storage
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

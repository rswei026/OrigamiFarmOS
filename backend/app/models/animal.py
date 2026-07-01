"""Animal Digital Twin and Flock - handbook Chapter 5 and Chapter 8.

RULE-ONT-104: because individual poultry tracking is not realistic, the
Flock itself (not each bird) is the digital twin for poultry. RULE-ONT-103:
a Herd groups Animal twins for feeding/task convenience; it never replaces
individual Animal records.
"""
import enum
import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, FarmScopedMixin, TimestampMixin


class AnimalSpecies(str, enum.Enum):
    COW = "cow"
    SHEEP = "sheep"
    GOAT = "goat"
    HORSE = "horse"


class AnimalStatus(str, enum.Enum):
    """Chapter 3 §3.3.1 Animal Lifecycle - derived from event history in a
    fuller implementation; stored directly here as a pragmatic MVP
    projection, recomputed by the service layer on each relevant event."""

    REGISTERED = "registered"
    ACTIVE = "active"
    UNDER_OBSERVATION = "under_observation"
    IN_TREATMENT = "in_treatment"
    WITHDRAWAL_PERIOD = "withdrawal_period"
    PREGNANT = "pregnant"
    SOLD = "sold"
    DECEASED = "deceased"


class FlockSpecies(str, enum.Enum):
    CHICKEN = "chicken"
    DUCK = "duck"
    TURKEY = "turkey"


class Animal(Base, FarmScopedMixin, TimestampMixin):
    """One digital twin per real animal - Ontology RULE-ONT-101/102."""

    __tablename__ = "animal"

    tag_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    species: Mapped[AnimalSpecies] = mapped_column(Enum(AnimalSpecies, name="animal_species"), nullable=False)
    breed: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sex: Mapped[str] = mapped_column(String(10), nullable=False)  # male, female
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    current_location_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.id"), nullable=True
    )
    status: Mapped[AnimalStatus] = mapped_column(
        Enum(AnimalStatus, name="animal_status"), default=AnimalStatus.REGISTERED, nullable=False
    )


class Flock(Base, FarmScopedMixin, TimestampMixin):
    """The Flock (not each bird) is the digital twin for poultry - RULE-ONT-104."""

    __tablename__ = "flock"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[FlockSpecies] = mapped_column(Enum(FlockSpecies, name="flock_species"), nullable=False)
    bird_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    location_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("location.id"), nullable=True
    )
    active: Mapped[bool] = mapped_column(default=True, nullable=False)


herd_animal = Table(
    "herd_animal",
    Base.metadata,
    Column("herd_id", UUID(as_uuid=True), ForeignKey("herd.id"), primary_key=True),
    Column("animal_id", UUID(as_uuid=True), ForeignKey("animal.id"), primary_key=True),
)


class Herd(Base, FarmScopedMixin, TimestampMixin):
    """A management grouping over Animal twins (RULE-ONT-103) - does not
    replace individual Animal records."""

    __tablename__ = "herd"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    animals = relationship("Animal", secondary=herd_animal, backref="herds")

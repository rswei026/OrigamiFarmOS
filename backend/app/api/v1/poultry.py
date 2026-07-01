"""Poultry Management API - handbook Chapter 8 §8.6.

Egg totals are also recorded as a quantitative Observation (mirroring
RULE-DAIRY-101's pattern for milk) so the Correlation Engine can detect
egg-decline patterns (Ch.8 §8.4).
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.base import utcnow
from app.models.observation import ObservationQuality
from app.models.production import EggCollection
from app.models.user import User
from app.schemas.production import EggCollectionCreate, EggCollectionRead
from app.services.knowledge_engine import evaluate_entity
from app.services.observations import create_observation

router = APIRouter(prefix="/poultry", tags=["poultry"])


@router.get("/egg-collections", response_model=list[EggCollectionRead])
def list_egg_collections(
    flock_id: uuid.UUID | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    stmt = select(EggCollection).where(EggCollection.farm_id == current_user.farm_id)
    if flock_id:
        stmt = stmt.where(EggCollection.flock_id == flock_id)
    return db.scalars(stmt.order_by(EggCollection.collected_at.desc())).all()


@router.post("/egg-collections", response_model=EggCollectionRead, status_code=status.HTTP_201_CREATED)
def create_egg_collection(
    payload: EggCollectionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    existing = db.get(EggCollection, payload.id)
    if existing is not None:
        return existing

    collected_at = payload.collected_at or utcnow()
    record = EggCollection(
        id=payload.id,
        farm_id=current_user.farm_id,
        flock_id=payload.flock_id,
        total_eggs=payload.total_eggs,
        broken_eggs=payload.broken_eggs,
        consumed=payload.consumed,
        sold=payload.sold,
        hatching=payload.hatching,
        collected_at=collected_at,
        recorded_by=current_user.id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    create_observation(
        db,
        observation_id=uuid.uuid4(),
        farm_id=current_user.farm_id,
        observer_id=current_user.id,
        entity_type="Flock",
        entity_id=payload.flock_id,
        observation_type="egg_total",
        value_numeric=float(payload.total_eggs),
        value_text=None,
        unit="eggs",
        quality=ObservationQuality.B_COUNTED,
        observed_at=record.collected_at,
        source="worker",
        notes=None,
    )
    evaluate_entity(db, farm_id=current_user.farm_id, entity_type="Flock", entity_id=payload.flock_id)
    return record

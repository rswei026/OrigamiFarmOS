"""Dairy Management API - handbook Chapter 7 §7.6.

RULE-DAIRY-101: milk volume is recorded as a quantitative Observation so
the Correlation Engine (Ch.4.4) can use it as a signal, in addition to
being stored as a structured MilkRecord (Ch.7 §7.5 schema).
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.base import utcnow
from app.models.observation import ObservationQuality
from app.models.production import MilkRecord
from app.models.user import User
from app.schemas.production import MilkRecordCreate, MilkRecordRead
from app.services.knowledge_engine import evaluate_entity
from app.services.observations import create_observation

router = APIRouter(prefix="/dairy", tags=["dairy"])


@router.get("/milk-sessions", response_model=list[MilkRecordRead])
def list_milk_records(
    animal_id: uuid.UUID | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    stmt = select(MilkRecord).where(MilkRecord.farm_id == current_user.farm_id)
    if animal_id:
        stmt = stmt.where(MilkRecord.animal_id == animal_id)
    return db.scalars(stmt.order_by(MilkRecord.recorded_at.desc())).all()


@router.post("/milk-sessions", response_model=MilkRecordRead, status_code=status.HTTP_201_CREATED)
def create_milk_record(
    payload: MilkRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    existing = db.get(MilkRecord, payload.id)
    if existing is not None:
        return existing

    recorded_at = payload.recorded_at or utcnow()
    record = MilkRecord(
        id=payload.id,
        farm_id=current_user.farm_id,
        animal_id=payload.animal_id,
        session=payload.session,
        volume_liters=payload.volume_liters,
        quality_abnormal=payload.quality_abnormal,
        destination=payload.destination,
        recorded_at=recorded_at,
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
        entity_type="Animal",
        entity_id=payload.animal_id,
        observation_type="milk_yield",
        value_numeric=payload.volume_liters,
        value_text=None,
        unit="L",
        quality=ObservationQuality.B_COUNTED,
        observed_at=record.recorded_at,
        source="worker",
        notes=f"session={payload.session.value}",
    )
    evaluate_entity(db, farm_id=current_user.farm_id, entity_type="Animal", entity_id=payload.animal_id)
    return record

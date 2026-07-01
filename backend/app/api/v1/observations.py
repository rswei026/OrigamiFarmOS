"""Observation API - handbook Chapter 4 §4.3.15, Chapter 9 §9.2 (Health
Observation Workflow). No diagnosis field exists here by design
(RULE-VET-101)."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.observation import Observation
from app.models.user import User
from app.schemas.observation import ObservationCreate, ObservationRead
from app.services.knowledge_engine import evaluate_entity
from app.services.observations import create_observation

router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("", response_model=list[ObservationRead])
def list_observations(
    entity_type: str | None = None,
    entity_id: uuid.UUID | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Observation).where(Observation.farm_id == current_user.farm_id)
    if entity_type:
        stmt = stmt.where(Observation.entity_type == entity_type)
    if entity_id:
        stmt = stmt.where(Observation.entity_id == entity_id)
    return db.scalars(stmt.order_by(Observation.observed_at.desc())).all()


@router.post("", response_model=ObservationRead, status_code=status.HTTP_201_CREATED)
def create_observation_endpoint(
    payload: ObservationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    obs, created = create_observation(
        db,
        observation_id=payload.id,
        farm_id=current_user.farm_id,
        observer_id=current_user.id,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        observation_type=payload.observation_type,
        value_numeric=payload.value_numeric,
        value_text=payload.value_text,
        unit=payload.unit,
        quality=payload.quality,
        observed_at=payload.observed_at,
        source=payload.source,
        notes=payload.notes,
    )
    if created:
        # Event-driven correlation (Ch.4.4 REQ-KM-401): evaluate patterns
        # as new observations arrive, not only on a batch schedule.
        evaluate_entity(db, farm_id=current_user.farm_id, entity_type=payload.entity_type, entity_id=payload.entity_id)
    return obs

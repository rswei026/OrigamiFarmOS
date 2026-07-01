"""Observation creation - handbook Chapter 4 §4.3.

Confidence is derived from Observation Quality Level (§4.3.6), never
user-entered directly, since the correlation engine's confidence
weighting (§4.4.5) depends on it being consistent.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.observation import Observation, ObservationQuality

QUALITY_CONFIDENCE = {
    ObservationQuality.A_INSTRUMENT: 0.95,
    ObservationQuality.B_COUNTED: 0.80,
    ObservationQuality.C_HUMAN_OBSERVED: 0.55,
    ObservationQuality.D_OPINION: 0.30,
}


def create_observation(
    db: Session,
    *,
    observation_id: uuid.UUID,
    farm_id: uuid.UUID,
    observer_id: uuid.UUID,
    entity_type: str,
    entity_id: uuid.UUID,
    observation_type: str,
    value_numeric: float | None,
    value_text: str | None,
    unit: str | None,
    quality: ObservationQuality,
    observed_at: datetime | None,
    source: str,
    notes: str | None,
) -> tuple[Observation, bool]:
    existing = db.get(Observation, observation_id)
    if existing is not None:
        return existing, False

    obs = Observation(
        id=observation_id,
        farm_id=farm_id,
        entity_type=entity_type,
        entity_id=entity_id,
        observation_type=observation_type,
        value_numeric=value_numeric,
        value_text=value_text,
        unit=unit,
        quality=quality,
        confidence=QUALITY_CONFIDENCE[quality],
        observer_id=observer_id,
        observed_at=observed_at or datetime.now(timezone.utc),
        source=source,
        notes=notes,
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs, True

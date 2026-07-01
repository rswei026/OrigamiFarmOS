import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.observation import ObservationQuality, VerificationStatus


class ObservationCreate(BaseModel):
    id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    observation_type: str
    value_numeric: float | None = None
    value_text: str | None = None
    unit: str | None = None
    quality: ObservationQuality
    observed_at: datetime | None = None
    source: str = "worker"
    notes: str | None = None


class ObservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    observation_type: str
    value_numeric: float | None
    value_text: str | None
    unit: str | None
    quality: ObservationQuality
    confidence: float
    observer_id: uuid.UUID
    observed_at: datetime
    source: str
    verification_status: VerificationStatus
    notes: str | None

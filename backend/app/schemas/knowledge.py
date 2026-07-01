import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models.knowledge import (
    ConfidenceBand,
    DecisionOption,
    RecommendationCategory,
    RecommendationPriority,
    RecommendationStatus,
)


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    category: RecommendationCategory
    priority: RecommendationPriority
    confidence_score: float
    confidence_band: ConfidenceBand
    evidence: dict
    explanation: str
    explanation_provider: str
    suggested_action: str
    missing_information: str | None
    due_date: date | None
    status: RecommendationStatus
    created_at: datetime


class DecisionCreate(BaseModel):
    id: uuid.UUID
    decision: DecisionOption
    reason: str | None = None
    delegated_to: uuid.UUID | None = None
    postponed_until: date | None = None


class DecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    recommendation_id: uuid.UUID
    decided_by: uuid.UUID
    decision: DecisionOption
    reason: str | None
    decided_at: datetime

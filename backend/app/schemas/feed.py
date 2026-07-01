import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.feed import LotSource


class FeedItemCreate(BaseModel):
    id: uuid.UUID
    name: str
    unit: str = "kg"


class FeedItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    unit: str


class FeedLotCreate(BaseModel):
    id: uuid.UUID
    feed_item_id: uuid.UUID
    source: LotSource
    quantity_received: float
    unit_cost: float = 0.0
    received_at: datetime | None = None


class FeedLotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    farm_id: uuid.UUID
    feed_item_id: uuid.UUID
    source: LotSource
    quantity_received: float
    unit_cost: float
    received_at: datetime
    remaining: float | None = None


class FeedDistributionCreate(BaseModel):
    id: uuid.UUID
    feed_lot_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    quantity: float
    distributed_at: datetime | None = None


class FeedDistributionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    farm_id: uuid.UUID
    feed_lot_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    quantity: float
    distributed_at: datetime
    recorded_by: uuid.UUID

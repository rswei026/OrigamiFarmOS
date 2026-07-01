import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.production import MilkDestination
from app.models.production import MilkSession as MilkSessionEnum


class MilkRecordCreate(BaseModel):
    id: uuid.UUID
    animal_id: uuid.UUID
    session: MilkSessionEnum
    volume_liters: float
    quality_abnormal: bool = False
    destination: MilkDestination = MilkDestination.SALE
    recorded_at: datetime | None = None


class MilkRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    farm_id: uuid.UUID
    animal_id: uuid.UUID
    session: MilkSessionEnum
    volume_liters: float
    quality_abnormal: bool
    destination: MilkDestination
    recorded_at: datetime
    recorded_by: uuid.UUID


class EggCollectionCreate(BaseModel):
    id: uuid.UUID
    flock_id: uuid.UUID
    total_eggs: int
    broken_eggs: int = 0
    consumed: int = 0
    sold: int = 0
    hatching: int = 0
    collected_at: datetime | None = None


class EggCollectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    farm_id: uuid.UUID
    flock_id: uuid.UUID
    total_eggs: int
    broken_eggs: int
    consumed: int
    sold: int
    hatching: int
    collected_at: datetime
    recorded_by: uuid.UUID

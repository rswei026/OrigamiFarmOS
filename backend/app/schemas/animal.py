import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.animal import AnimalSpecies, AnimalStatus, FlockSpecies


class AnimalCreate(BaseModel):
    id: uuid.UUID  # client-generated (Ch.14 RULE-DB-103)
    tag_number: str
    name: str | None = None
    species: AnimalSpecies
    breed: str | None = None
    sex: str
    birth_date: date | None = None
    current_location_id: uuid.UUID | None = None


class AnimalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    tag_number: str
    name: str | None
    species: AnimalSpecies
    breed: str | None
    sex: str
    birth_date: date | None
    current_location_id: uuid.UUID | None
    status: AnimalStatus


class FlockCreate(BaseModel):
    id: uuid.UUID
    name: str
    species: FlockSpecies
    bird_count: int = 0
    location_id: uuid.UUID | None = None


class FlockRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    species: FlockSpecies
    bird_count: int
    location_id: uuid.UUID | None
    active: bool


class LocationCreate(BaseModel):
    id: uuid.UUID
    name: str
    location_type: str
    parent_id: uuid.UUID | None = None


class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    location_type: str
    parent_id: uuid.UUID | None
    active: bool

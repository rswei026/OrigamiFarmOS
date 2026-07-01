"""Animal Digital Twin API - handbook Chapter 5 §5.10."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.idempotent import get_or_create
from app.models.animal import Animal
from app.models.user import User
from app.schemas.animal import AnimalCreate, AnimalRead
from app.services.timeline import build_timeline

router = APIRouter(prefix="/animals", tags=["animals"])


@router.get("", response_model=list[AnimalRead])
def list_animals(
    location_id: uuid.UUID | None = None,
    species: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Animal).where(Animal.farm_id == current_user.farm_id)
    if location_id:
        stmt = stmt.where(Animal.current_location_id == location_id)
    if species:
        stmt = stmt.where(Animal.species == species)
    return db.scalars(stmt).all()


@router.post("", response_model=AnimalRead, status_code=status.HTTP_201_CREATED)
def create_animal(payload: AnimalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    animal, _ = get_or_create(
        db,
        Animal,
        payload.id,
        farm_id=current_user.farm_id,
        tag_number=payload.tag_number,
        name=payload.name,
        species=payload.species,
        breed=payload.breed,
        sex=payload.sex,
        birth_date=payload.birth_date,
        current_location_id=payload.current_location_id,
    )
    return animal


@router.get("/{animal_id}", response_model=AnimalRead)
def get_animal(animal_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    animal = db.get(Animal, animal_id)
    if not animal or animal.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return animal


@router.get("/{animal_id}/timeline")
def get_animal_timeline(
    animal_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    animal = db.get(Animal, animal_id)
    if not animal or animal.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal not found")
    return build_timeline(db, current_user.farm_id, "Animal", animal_id)

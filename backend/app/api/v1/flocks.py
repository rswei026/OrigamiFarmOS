"""Poultry Flock API - handbook Chapter 8 §8.6."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.idempotent import get_or_create
from app.models.animal import Flock
from app.models.user import User
from app.schemas.animal import FlockCreate, FlockRead
from app.services.timeline import build_timeline

router = APIRouter(prefix="/flocks", tags=["flocks"])


@router.get("", response_model=list[FlockRead])
def list_flocks(
    species: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    stmt = select(Flock).where(Flock.farm_id == current_user.farm_id)
    if species:
        stmt = stmt.where(Flock.species == species)
    return db.scalars(stmt).all()


@router.post("", response_model=FlockRead, status_code=status.HTTP_201_CREATED)
def create_flock(payload: FlockCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    flock, _ = get_or_create(
        db,
        Flock,
        payload.id,
        farm_id=current_user.farm_id,
        name=payload.name,
        species=payload.species,
        bird_count=payload.bird_count,
        location_id=payload.location_id,
    )
    return flock


@router.get("/{flock_id}", response_model=FlockRead)
def get_flock(flock_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    flock = db.get(Flock, flock_id)
    if not flock or flock.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flock not found")
    return flock


@router.get("/{flock_id}/timeline")
def get_flock_timeline(flock_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    flock = db.get(Flock, flock_id)
    if not flock or flock.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flock not found")
    return build_timeline(db, current_user.farm_id, "Flock", flock_id)

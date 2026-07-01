from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.idempotent import get_or_create
from app.models.farm import Location
from app.models.user import User
from app.schemas.animal import LocationCreate, LocationRead

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=list[LocationRead])
def list_locations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.scalars(select(Location).where(Location.farm_id == current_user.farm_id)).all()


@router.post("", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
def create_location(
    payload: LocationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    location, _ = get_or_create(
        db,
        Location,
        payload.id,
        farm_id=current_user.farm_id,
        name=payload.name,
        location_type=payload.location_type,
        parent_id=payload.parent_id,
    )
    return location

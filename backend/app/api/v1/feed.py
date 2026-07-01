"""Feed Management API - handbook Chapter 6 §6.7."""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.idempotent import get_or_create
from app.models.feed import FeedDistribution, FeedItem, FeedLot
from app.models.user import User
from app.schemas.feed import (
    FeedDistributionCreate,
    FeedDistributionRead,
    FeedItemCreate,
    FeedItemRead,
    FeedLotCreate,
    FeedLotRead,
)
from app.services.feed import days_of_stock_remaining, remaining_stock

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/items", response_model=list[FeedItemRead])
def list_feed_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.scalars(select(FeedItem).where(FeedItem.farm_id == current_user.farm_id)).all()


@router.post("/items", response_model=FeedItemRead, status_code=status.HTTP_201_CREATED)
def create_feed_item(payload: FeedItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item, _ = get_or_create(db, FeedItem, payload.id, farm_id=current_user.farm_id, name=payload.name, unit=payload.unit)
    return item


@router.get("/lots", response_model=list[FeedLotRead])
def list_feed_lots(
    feed_item_id: uuid.UUID | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    stmt = select(FeedLot).where(FeedLot.farm_id == current_user.farm_id)
    if feed_item_id:
        stmt = stmt.where(FeedLot.feed_item_id == feed_item_id)
    lots = db.scalars(stmt).all()
    results = []
    for lot in lots:
        r = FeedLotRead.model_validate(lot)
        r.remaining = remaining_stock(db, lot.id)
        results.append(r)
    return results


@router.post("/lots", response_model=FeedLotRead, status_code=status.HTTP_201_CREATED)
def create_feed_lot(payload: FeedLotCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    kwargs = {"farm_id": current_user.farm_id, **payload.model_dump(exclude={"id"}, exclude_none=True)}
    lot, _ = get_or_create(db, FeedLot, payload.id, **kwargs)
    r = FeedLotRead.model_validate(lot)
    r.remaining = remaining_stock(db, lot.id)
    return r


@router.post("/distributions", response_model=FeedDistributionRead, status_code=status.HTTP_201_CREATED)
def create_feed_distribution(
    payload: FeedDistributionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Ch.6 §6.3 feeding workflow: deducting inventory and allocating cost
    happen implicitly because remaining stock (RULE-FEED-101) and cost
    allocation are derived from this event, not stored redundantly."""
    kwargs = {
        "farm_id": current_user.farm_id,
        "recorded_by": current_user.id,
        **payload.model_dump(exclude={"id"}, exclude_none=True),
    }
    dist, _ = get_or_create(db, FeedDistribution, payload.id, **kwargs)
    return dist


@router.get("/items/{feed_item_id}/forecast")
def get_feed_forecast(
    feed_item_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    days = days_of_stock_remaining(db, current_user.farm_id, feed_item_id)
    return {"feed_item_id": str(feed_item_id), "days_of_stock_remaining": days}

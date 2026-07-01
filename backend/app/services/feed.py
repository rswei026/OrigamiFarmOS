"""Feed stock derivation - handbook Chapter 6 §6.4, Chapter 14 RULE-DB-102:
remaining stock is always computed from lot + distribution history, never
a mutable field."""
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.feed import FeedDistribution, FeedLot


def remaining_stock(db: Session, feed_lot_id: uuid.UUID) -> float:
    lot = db.get(FeedLot, feed_lot_id)
    if lot is None:
        return 0.0
    distributed = db.scalar(
        select(func.coalesce(func.sum(FeedDistribution.quantity), 0.0)).where(
            FeedDistribution.feed_lot_id == feed_lot_id
        )
    )
    return lot.quantity_received - float(distributed or 0.0)


def days_of_stock_remaining(db: Session, farm_id: uuid.UUID, feed_item_id: uuid.UUID, window_days: int = 7) -> float | None:
    """Simple moving-average forecast (Ch.6 REQ-FEED-102 Codex note: keep
    this a moving average for MVP, not predictive modeling)."""
    lots = db.scalars(
        select(FeedLot).where(FeedLot.farm_id == farm_id, FeedLot.feed_item_id == feed_item_id)
    ).all()
    total_remaining = sum(remaining_stock(db, lot.id) for lot in lots)

    since = datetime.now(timezone.utc) - timedelta(days=window_days)
    lot_ids = [lot.id for lot in lots]
    if not lot_ids:
        return None
    recent_consumption = db.scalar(
        select(func.coalesce(func.sum(FeedDistribution.quantity), 0.0)).where(
            FeedDistribution.feed_lot_id.in_(lot_ids),
            FeedDistribution.distributed_at >= since,
        )
    )
    daily_rate = float(recent_consumption or 0.0) / window_days
    if daily_rate <= 0:
        return None
    return total_remaining / daily_rate

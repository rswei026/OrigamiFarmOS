"""Morning Briefing - handbook Chapter 3 §3.4, Chapter 4 §4.6.4.1 (Daily
Review: "what needs attention today?"). A read-time aggregation over
existing Recommendation, FeedItem, and today's production records - not a
separate data model (consistent with RULE-KM-602: reviews are views)."""
from datetime import date, datetime, time, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.feed import FeedItem
from app.models.knowledge import Recommendation, RecommendationPriority, RecommendationStatus
from app.models.production import EggCollection, MilkRecord
from app.models.observation import Observation
from app.models.user import User
from app.services.feed import days_of_stock_remaining

router = APIRouter(prefix="/briefing", tags=["briefing"])


@router.get("/morning")
def morning_briefing(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    farm_id = current_user.farm_id
    today_start = datetime.combine(date.today(), time.min, tzinfo=timezone.utc)

    urgent_recs = db.scalars(
        select(Recommendation)
        .where(
            Recommendation.farm_id == farm_id,
            Recommendation.status == RecommendationStatus.OPEN,
            Recommendation.priority.in_([RecommendationPriority.URGENT, RecommendationPriority.HIGH]),
        )
        .order_by(Recommendation.priority, Recommendation.created_at.desc())
    ).all()

    open_by_category: dict[str, int] = {}
    for rec in db.scalars(
        select(Recommendation).where(Recommendation.farm_id == farm_id, Recommendation.status == RecommendationStatus.OPEN)
    ):
        open_by_category[rec.category.value] = open_by_category.get(rec.category.value, 0) + 1

    feed_warnings = []
    for item in db.scalars(select(FeedItem).where(FeedItem.farm_id == farm_id)):
        days = days_of_stock_remaining(db, farm_id, item.id)
        if days is not None and days <= 7:
            feed_warnings.append({"feed_item_id": str(item.id), "feed_item_name": item.name, "days_remaining": round(days, 1)})

    milk_today = db.scalar(
        select(MilkRecord).where(MilkRecord.farm_id == farm_id, MilkRecord.recorded_at >= today_start)
    )
    egg_today = db.scalar(
        select(EggCollection).where(EggCollection.farm_id == farm_id, EggCollection.collected_at >= today_start)
    )
    observations_today_count = len(
        db.scalars(
            select(Observation).where(Observation.farm_id == farm_id, Observation.observed_at >= today_start)
        ).all()
    )

    return {
        "date": date.today().isoformat(),
        "urgent_recommendations": [
            {
                "id": str(r.id),
                "entity_type": r.entity_type,
                "entity_id": str(r.entity_id),
                "category": r.category.value,
                "priority": r.priority.value,
                "confidence_band": r.confidence_band.value,
                "explanation": r.explanation,
                "suggested_action": r.suggested_action,
            }
            for r in urgent_recs
        ],
        "open_recommendations_by_category": open_by_category,
        "feed_stock_warnings": feed_warnings,
        "todays_activity": {
            "milk_recorded": milk_today is not None,
            "eggs_recorded": egg_today is not None,
            "observations_recorded_today": observations_today_count,
        },
    }

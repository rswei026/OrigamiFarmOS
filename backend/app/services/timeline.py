"""Knowledge Timeline - handbook Chapter 4 §4.8. A read-time projection
over existing records (RULE-KM-801), never a separately maintained table.
Reused across Animal and Flock profiles (Ch.4.8.7 Codex notes) rather than
building per-entity-type timeline implementations."""
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.feed import FeedDistribution
from app.models.knowledge import Recommendation
from app.models.observation import Observation
from app.models.production import EggCollection, MilkRecord


def build_timeline(db: Session, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for obs in db.scalars(
        select(Observation).where(
            Observation.farm_id == farm_id,
            Observation.entity_type == entity_type,
            Observation.entity_id == entity_id,
        )
    ):
        entries.append(
            {
                "type": "observation",
                "timestamp": obs.observed_at,
                "summary": f"{obs.observation_type}: {obs.value_numeric if obs.value_numeric is not None else obs.value_text}"
                + (f" {obs.unit}" if obs.unit else ""),
                "quality": obs.quality.value,
                "id": str(obs.id),
            }
        )

    if entity_type == "Animal":
        for milk in db.scalars(select(MilkRecord).where(MilkRecord.animal_id == entity_id)):
            entries.append(
                {
                    "type": "milk_record",
                    "timestamp": milk.recorded_at,
                    "summary": f"Milk ({milk.session.value}): {milk.volume_liters} L -> {milk.destination.value}",
                    "id": str(milk.id),
                }
            )

    if entity_type == "Flock":
        for egg in db.scalars(select(EggCollection).where(EggCollection.flock_id == entity_id)):
            entries.append(
                {
                    "type": "egg_collection",
                    "timestamp": egg.collected_at,
                    "summary": f"Eggs collected: {egg.total_eggs} (broken {egg.broken_eggs})",
                    "id": str(egg.id),
                }
            )

    for feed in db.scalars(
        select(FeedDistribution).where(
            FeedDistribution.farm_id == farm_id,
            FeedDistribution.entity_type == entity_type,
            FeedDistribution.entity_id == entity_id,
        )
    ):
        entries.append(
            {
                "type": "feed_distribution",
                "timestamp": feed.distributed_at,
                "summary": f"Fed {feed.quantity} kg",
                "id": str(feed.id),
            }
        )

    for rec in db.scalars(
        select(Recommendation).where(
            Recommendation.farm_id == farm_id,
            Recommendation.entity_type == entity_type,
            Recommendation.entity_id == entity_id,
        )
    ):
        entries.append(
            {
                "type": "recommendation",
                "timestamp": rec.created_at,
                "summary": rec.suggested_action,
                "priority": rec.priority.value,
                "confidence_band": rec.confidence_band.value,
                "status": rec.status.value,
                "id": str(rec.id),
            }
        )

    entries.sort(key=lambda e: e["timestamp"] if isinstance(e["timestamp"], datetime) else datetime.min, reverse=True)
    return entries

"""Knowledge Engine orchestrator - ties the Correlation Engine (§4.4) to
the Recommendation Engine (§4.5). Called after any new Observation,
MilkRecord, or EggCollection is created (event-driven, REQ-KM-401)."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.animal import Animal, Flock
from app.models.knowledge import KnowledgeObject, KnowledgeObjectStatus, Recommendation, RecommendationStatus
from app.services import correlation
from app.services.recommendation import create_recommendation_from_pattern

PATTERN_EVALUATORS = {
    "Animal": [correlation.evaluate_animal_health_decline],
    "Flock": [correlation.evaluate_flock_egg_decline],
}


def _has_open_recommendation(db: Session, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID, pattern_id: str) -> bool:
    """Avoid recommendation spam: don't raise a second recommendation for
    the same pattern on the same entity while one is still open."""
    existing = db.scalar(
        select(Recommendation)
        .join(KnowledgeObject, Recommendation.knowledge_object_id == KnowledgeObject.id)
        .where(
            Recommendation.farm_id == farm_id,
            Recommendation.entity_type == entity_type,
            Recommendation.entity_id == entity_id,
            KnowledgeObject.pattern_id == pattern_id,
            Recommendation.status.in_([RecommendationStatus.OPEN, RecommendationStatus.MONITORING]),
        )
    )
    return existing is not None


def _entity_label(db: Session, entity_type: str, entity_id: uuid.UUID) -> str:
    if entity_type == "Animal":
        animal = db.get(Animal, entity_id)
        return f"{animal.species.value.title()} {animal.tag_number}" if animal else "Animal"
    if entity_type == "Flock":
        flock = db.get(Flock, entity_id)
        return f"{flock.species.value.title()} flock '{flock.name}'" if flock else "Flock"
    return entity_type


def evaluate_entity(db: Session, *, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID) -> list[Recommendation]:
    evaluators = PATTERN_EVALUATORS.get(entity_type, [])
    created: list[Recommendation] = []

    for evaluator in evaluators:
        result = evaluator(db, farm_id, entity_id)
        if not result.matched:
            continue
        if _has_open_recommendation(db, farm_id, entity_type, entity_id, result.pattern_id):
            continue

        knowledge_object = KnowledgeObject(
            farm_id=farm_id,
            entity_type=entity_type,
            entity_id=entity_id,
            pattern_id=result.pattern_id,
            supporting_observation_ids=[str(oid) for oid in result.supporting_observation_ids],
            confidence=result.confidence,
            status=KnowledgeObjectStatus.ACTIVE,
        )
        db.add(knowledge_object)
        db.commit()
        db.refresh(knowledge_object)

        label = _entity_label(db, entity_type, entity_id)
        recommendation = create_recommendation_from_pattern(
            db,
            farm_id=farm_id,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_label=label,
            knowledge_object=knowledge_object,
            pattern_result=result,
        )
        created.append(recommendation)

    return created

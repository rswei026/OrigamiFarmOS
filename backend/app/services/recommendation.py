"""Recommendation Engine - handbook Chapter 4 §4.5.

RULE-KM-501/502: rule-based, deterministic mapping from Knowledge Object
pattern to Recommendation. RULE-KM-701/702 (Ch.4.7): every recommendation
carries evidence, confidence band, and explanation - never bare.
"""
from __future__ import annotations

import uuid
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.knowledge import (
    ConfidenceBand,
    KnowledgeObject,
    Recommendation,
    RecommendationCategory,
    RecommendationPriority,
)
from app.models.observation import Observation
from app.services.ai_provider import StructuredEvidence, explain_with_fallback
from app.services.correlation import PatternResult

# Pattern -> (category, suggested_action, missing_information hint)
PATTERN_CONFIG = {
    "health-decline-v1": {
        "category": RecommendationCategory.HEALTH,
        "suggested_action": "Schedule a veterinary examination within 12-24 hours.",
        "missing_information": "A structured health observation (swelling, discharge, wound) would raise confidence further.",
        "entity_label_prefix": "Animal",
    },
    "egg-decline-v1": {
        "category": RecommendationCategory.PRODUCTION,
        "suggested_action": "Review flock feed ration and check for health or environmental stressors.",
        "missing_information": "A flock health observation would help confirm whether this is feed- or health-related.",
        "entity_label_prefix": "Flock",
    },
}


def _confidence_band(score: float) -> ConfidenceBand:
    if score >= 0.75:
        return ConfidenceBand.HIGH
    if score >= 0.4:
        return ConfidenceBand.MEDIUM
    return ConfidenceBand.LOW


def _priority_for(pattern_id: str, band: ConfidenceBand) -> RecommendationPriority:
    if band == ConfidenceBand.HIGH:
        return RecommendationPriority.URGENT if pattern_id == "health-decline-v1" else RecommendationPriority.HIGH
    if band == ConfidenceBand.MEDIUM:
        return RecommendationPriority.HIGH if pattern_id == "health-decline-v1" else RecommendationPriority.MEDIUM
    return RecommendationPriority.MEDIUM


def create_recommendation_from_pattern(
    db: Session,
    *,
    farm_id: uuid.UUID,
    entity_type: str,
    entity_id: uuid.UUID,
    entity_label: str,
    knowledge_object: KnowledgeObject,
    pattern_result: PatternResult,
) -> Recommendation:
    config = PATTERN_CONFIG[pattern_result.pattern_id]
    band = _confidence_band(pattern_result.confidence)
    priority = _priority_for(pattern_result.pattern_id, band)

    observations = (
        db.query(Observation).filter(Observation.id.in_(pattern_result.supporting_observation_ids)).all()
        if pattern_result.supporting_observation_ids
        else []
    )
    evidence_payload = {
        "signals": [
            {"signal": s.signal_name, "detail": s.detail, "weight": s.weight, "confidence": s.confidence}
            for s in pattern_result.signals
        ],
        "observations": [
            {
                "id": str(o.id),
                "type": o.observation_type,
                "value": o.value_numeric if o.value_numeric is not None else o.value_text,
                "unit": o.unit,
                "observed_at": o.observed_at.isoformat(),
                "quality": o.quality.value,
            }
            for o in observations
        ],
        "pattern_id": pattern_result.pattern_id,
        "confidence_score": pattern_result.confidence,
    }

    evidence = StructuredEvidence(
        entity_label=entity_label,
        pattern_id=pattern_result.pattern_id,
        observations=evidence_payload["observations"],
        confidence_band=band.value,
        confidence_score=pattern_result.confidence,
        suggested_action=config["suggested_action"],
        missing_information=config["missing_information"],
        historical_context=None,
    )
    explanation, provider_name = explain_with_fallback(evidence)

    recommendation = Recommendation(
        farm_id=farm_id,
        entity_type=entity_type,
        entity_id=entity_id,
        knowledge_object_id=knowledge_object.id,
        category=config["category"],
        priority=priority,
        confidence_score=pattern_result.confidence,
        confidence_band=band,
        evidence=evidence_payload,
        explanation=explanation,
        explanation_provider=provider_name,
        suggested_action=config["suggested_action"],
        missing_information=config["missing_information"],
        due_date=date.today() + timedelta(days=1),
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)
    return recommendation

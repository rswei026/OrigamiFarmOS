"""Knowledge Correlation Engine - handbook Chapter 4 §4.4.

MVP patterns are declarative-in-spirit (defined as data below, per RULE-KM-403
Codex note "implement patterns as data, evaluated by a generic rule
evaluator") even though, for this pass, they are expressed as Python
dicts rather than externally editable config - the evaluator itself does
not hard-code per-species logic.

RULE-KM-401: a Knowledge Object is never generated from a single weak
signal alone (min_signals_required enforces this).
RULE-KM-402: correlation is scoped to one entity within a time window.
RULE-KM-403: confidence reflects observation quality, not just signal count.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.observation import Observation


@dataclass
class SignalMatch:
    signal_name: str
    weight: float
    confidence: float
    observation_ids: list[uuid.UUID]
    detail: str


@dataclass
class PatternResult:
    pattern_id: str
    matched: bool
    confidence: float = 0.0
    signals: list[SignalMatch] = field(default_factory=list)
    supporting_observation_ids: list[uuid.UUID] = field(default_factory=list)


def _trend_decline(
    db: Session, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID, observation_type: str, window_days: int = 3, baseline_days: int = 7
) -> tuple[float | None, list[uuid.UUID], float]:
    """Compares the average of the most recent `window_days` worth of
    observations against the preceding `baseline_days`. Returns
    (pct_change, contributing_observation_ids, avg_confidence) or
    (None, [], 0.0) if there isn't enough history (Ch.4.4 §4.4.6: missing
    data reduces evidence, it is not treated as a signal either way)."""
    now = datetime.now(timezone.utc)
    recent_cutoff = now - timedelta(days=window_days)
    baseline_cutoff = recent_cutoff - timedelta(days=baseline_days)

    obs = db.scalars(
        select(Observation)
        .where(
            Observation.farm_id == farm_id,
            Observation.entity_type == entity_type,
            Observation.entity_id == entity_id,
            Observation.observation_type == observation_type,
            Observation.observed_at >= baseline_cutoff,
            Observation.value_numeric.is_not(None),
        )
        .order_by(Observation.observed_at)
    ).all()

    recent = [o for o in obs if o.observed_at >= recent_cutoff]
    baseline = [o for o in obs if o.observed_at < recent_cutoff]

    if not recent or not baseline:
        return None, [], 0.0

    recent_avg = statistics.mean(o.value_numeric for o in recent)
    baseline_avg = statistics.mean(o.value_numeric for o in baseline)
    if baseline_avg == 0:
        return None, [], 0.0

    pct_change = (recent_avg - baseline_avg) / baseline_avg
    contributing_ids = [o.id for o in recent]
    avg_confidence = statistics.mean(o.confidence for o in recent)
    return pct_change, contributing_ids, avg_confidence


def _latest_above_threshold(
    db: Session, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID, observation_type: str, threshold: float, within_days: int = 3
) -> tuple[bool, list[uuid.UUID], float]:
    since = datetime.now(timezone.utc) - timedelta(days=within_days)
    obs = db.scalars(
        select(Observation).where(
            Observation.farm_id == farm_id,
            Observation.entity_type == entity_type,
            Observation.entity_id == entity_id,
            Observation.observation_type == observation_type,
            Observation.observed_at >= since,
            Observation.value_numeric.is_not(None),
        )
    ).all()
    matches = [o for o in obs if o.value_numeric >= threshold]
    if not matches:
        return False, [], 0.0
    return True, [o.id for o in matches], statistics.mean(o.confidence for o in matches)


def _recent_text_match(
    db: Session, farm_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID, observation_type: str, keywords: list[str], within_days: int = 3
) -> tuple[bool, list[uuid.UUID], float]:
    since = datetime.now(timezone.utc) - timedelta(days=within_days)
    obs = db.scalars(
        select(Observation).where(
            Observation.farm_id == farm_id,
            Observation.entity_type == entity_type,
            Observation.entity_id == entity_id,
            Observation.observation_type == observation_type,
            Observation.observed_at >= since,
        )
    ).all()
    matches = [o for o in obs if o.value_text and any(k in o.value_text.lower() for k in keywords)]
    if not matches:
        return False, [], 0.0
    return True, [o.id for o in matches], statistics.mean(o.confidence for o in matches)


def evaluate_animal_health_decline(db: Session, farm_id: uuid.UUID, entity_id: uuid.UUID) -> PatternResult:
    """Pattern "health-decline-v1" (Ch.4.4.3 example): milk down + feed
    down + temperature elevated + appetite reduced. min_signals_required=2."""
    signals: list[SignalMatch] = []

    milk_change, milk_ids, milk_conf = _trend_decline(db, farm_id, "Animal", entity_id, "milk_yield")
    if milk_change is not None and milk_change <= -0.10:
        signals.append(SignalMatch("milk_yield_decline", 0.35, milk_conf, milk_ids, f"milk yield down {milk_change:.0%}"))

    feed_change, feed_ids, feed_conf = _trend_decline(db, farm_id, "Animal", entity_id, "feed_intake")
    if feed_change is not None and feed_change <= -0.10:
        signals.append(SignalMatch("feed_intake_decline", 0.25, feed_conf, feed_ids, f"feed intake down {feed_change:.0%}"))

    temp_hit, temp_ids, temp_conf = _latest_above_threshold(db, farm_id, "Animal", entity_id, "temperature", threshold=39.5)
    if temp_hit:
        signals.append(SignalMatch("temperature_elevated", 0.25, temp_conf, temp_ids, "temperature elevated"))

    appetite_hit, appetite_ids, appetite_conf = _recent_text_match(
        db, farm_id, "Animal", entity_id, "appetite", keywords=["reduced", "refused", "low"]
    )
    if appetite_hit:
        signals.append(SignalMatch("appetite_reduced", 0.15, appetite_conf, appetite_ids, "appetite reduced"))

    if len(signals) < 2:
        return PatternResult(pattern_id="health-decline-v1", matched=False)

    total_weight = sum(s.weight for s in signals)
    confidence = sum(s.weight * s.confidence for s in signals) / total_weight if total_weight else 0.0
    supporting_ids = [oid for s in signals for oid in s.observation_ids]

    return PatternResult(
        pattern_id="health-decline-v1",
        matched=True,
        confidence=confidence,
        signals=signals,
        supporting_observation_ids=supporting_ids,
    )


def evaluate_flock_egg_decline(db: Session, farm_id: uuid.UUID, entity_id: uuid.UUID) -> PatternResult:
    """Pattern "egg-decline-v1" (Ch.8 §8.4)."""
    egg_change, egg_ids, egg_conf = _trend_decline(db, farm_id, "Flock", entity_id, "egg_total")
    if egg_change is None or egg_change > -0.10:
        return PatternResult(pattern_id="egg-decline-v1", matched=False)

    signal = SignalMatch("egg_total_decline", 1.0, egg_conf, egg_ids, f"egg production down {egg_change:.0%}")
    return PatternResult(
        pattern_id="egg-decline-v1",
        matched=True,
        confidence=egg_conf,
        signals=[signal],
        supporting_observation_ids=egg_ids,
    )

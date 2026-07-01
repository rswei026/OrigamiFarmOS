"""Recommendation & Decision API - handbook Chapter 4 §4.5-4.6.

Decision-making is restricted to Owner/Manager/Veterinarian per the role
table in Behavioral Model §3.6 (Workers observe; they do not decide).
"""
import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.knowledge import Decision, DecisionOption, Recommendation, RecommendationStatus
from app.models.user import User, UserRole
from app.schemas.knowledge import DecisionCreate, DecisionRead, RecommendationRead

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

DECISION_MAKERS = require_roles(UserRole.OWNER, UserRole.MANAGER, UserRole.VETERINARIAN)

_STATUS_FOR_DECISION = {
    DecisionOption.ACCEPT: RecommendationStatus.ACCEPTED,
    DecisionOption.REJECT: RecommendationStatus.REJECTED,
    DecisionOption.MONITOR: RecommendationStatus.MONITORING,
    DecisionOption.DELEGATE: RecommendationStatus.OPEN,
    DecisionOption.ESCALATE: RecommendationStatus.OPEN,
    DecisionOption.POSTPONE: RecommendationStatus.OPEN,
}


@router.get("", response_model=list[RecommendationRead])
def list_recommendations(
    status_filter: RecommendationStatus | None = None,
    priority: str | None = None,
    category: str | None = None,
    include_postponed: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Recommendation).where(Recommendation.farm_id == current_user.farm_id)
    if status_filter:
        stmt = stmt.where(Recommendation.status == status_filter)
    if priority:
        stmt = stmt.where(Recommendation.priority == priority)
    if category:
        stmt = stmt.where(Recommendation.category == category)
    recs = db.scalars(stmt.order_by(Recommendation.created_at.desc())).all()

    if not include_postponed:
        today = date.today()
        postponed_ids = {
            d.recommendation_id
            for d in db.scalars(
                select(Decision).where(
                    Decision.farm_id == current_user.farm_id,
                    Decision.decision == DecisionOption.POSTPONE,
                    Decision.postponed_until > today,
                )
            ).all()
        }
        recs = [r for r in recs if r.id not in postponed_ids]

    return recs


@router.get("/{recommendation_id}", response_model=RecommendationRead)
def get_recommendation(
    recommendation_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    rec = db.get(Recommendation, recommendation_id)
    if not rec or rec.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    return rec


@router.post("/{recommendation_id}/decisions", response_model=DecisionRead, status_code=status.HTTP_201_CREATED)
def create_decision(
    recommendation_id: uuid.UUID,
    payload: DecisionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(DECISION_MAKERS),
):
    rec = db.get(Recommendation, recommendation_id)
    if not rec or rec.farm_id != current_user.farm_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    existing = db.get(Decision, payload.id)
    if existing is not None:
        return existing

    if payload.decision == DecisionOption.REJECT and not payload.reason:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A reason is required to reject a recommendation.")

    decision = Decision(
        id=payload.id,
        farm_id=current_user.farm_id,
        recommendation_id=recommendation_id,
        decided_by=current_user.id,
        decision=payload.decision,
        reason=payload.reason,
        delegated_to=payload.delegated_to,
        postponed_until=payload.postponed_until,
    )
    db.add(decision)

    rec.status = _STATUS_FOR_DECISION[payload.decision]
    db.add(rec)
    db.commit()
    db.refresh(decision)
    return decision

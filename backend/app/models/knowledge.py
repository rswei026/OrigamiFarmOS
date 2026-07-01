"""Knowledge Model entities - handbook Chapter 4 §4.4-4.6.

KnowledgeObject: §4.4.7. Recommendation: §4.5.3 (must carry evidence,
confidence, explanation - RULE-KM-701/702). Decision: §4.6.3.
"""
import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, FarmScopedMixin, utcnow


class KnowledgeObjectStatus(str, enum.Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    SUPERSEDED = "superseded"


class KnowledgeObject(Base, FarmScopedMixin):
    __tablename__ = "knowledge_object"

    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    pattern_id: Mapped[str] = mapped_column(String(100), nullable=False)
    pattern_version: Mapped[str] = mapped_column(String(20), nullable=False, default="v1")
    supporting_observation_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    status: Mapped[KnowledgeObjectStatus] = mapped_column(
        Enum(KnowledgeObjectStatus, name="knowledge_object_status"),
        default=KnowledgeObjectStatus.ACTIVE,
        nullable=False,
    )


class RecommendationCategory(str, enum.Enum):
    HEALTH = "health"
    PRODUCTION = "production"
    INVENTORY = "inventory"
    FINANCIAL = "financial"
    BREEDING = "breeding"
    COMPLIANCE = "compliance"


class RecommendationPriority(str, enum.Enum):
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ConfidenceBand(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationStatus(str, enum.Enum):
    """Chapter 3 §3.3.3 Recommendation Lifecycle."""

    OPEN = "open"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    MONITORING = "monitoring"
    ACTION_IN_PROGRESS = "action_in_progress"
    CLOSED = "closed"


class Recommendation(Base, FarmScopedMixin):
    """Every field here is required by the explanation contract in
    Ch.4.7 §4.7.2 (RULE-KM-701): no recommendation may be shown without
    evidence, confidence, explanation, and suggested action."""

    __tablename__ = "recommendation"

    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    knowledge_object_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_object.id"), nullable=True
    )
    category: Mapped[RecommendationCategory] = mapped_column(
        Enum(RecommendationCategory, name="recommendation_category"), nullable=False
    )
    priority: Mapped[RecommendationPriority] = mapped_column(
        Enum(RecommendationPriority, name="recommendation_priority"), nullable=False
    )
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_band: Mapped[ConfidenceBand] = mapped_column(Enum(ConfidenceBand, name="confidence_band"), nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    explanation_provider: Mapped[str] = mapped_column(String(30), nullable=False, default="rule_based")
    suggested_action: Mapped[str] = mapped_column(Text, nullable=False)
    missing_information: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, name="recommendation_status"), default=RecommendationStatus.OPEN, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class DecisionOption(str, enum.Enum):
    """Chapter 4 §4.6.2."""

    ACCEPT = "accept"
    REJECT = "reject"
    MONITOR = "monitor"
    DELEGATE = "delegate"
    ESCALATE = "escalate"
    POSTPONE = "postpone"


class Decision(Base, FarmScopedMixin):
    """RULE-KM-601: every decision is logged - who, when, which option, why."""

    __tablename__ = "decision"

    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("recommendation.id"), nullable=False, index=True
    )
    decided_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False)
    decision: Mapped[DecisionOption] = mapped_column(Enum(DecisionOption, name="decision_option"), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    delegated_to: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=True)
    postponed_until: Mapped[date | None] = mapped_column(Date, nullable=True)

"""Idempotent create helper - handbook Chapter 15 §15.5 (RULE-API-103) /
Chapter 16 §16.2: because writes may originate offline and be replayed on
sync, every write endpoint accepts the client-generated ID (Ch.14
RULE-DB-103) and replaying the same ID is a no-op, not a duplicate."""
import uuid
from typing import TypeVar

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


def get_or_create(db: Session, model, record_id: uuid.UUID, **fields) -> tuple[ModelT, bool]:
    """Returns (instance, created). If a row with this ID already exists,
    it is returned unchanged (idempotent replay); otherwise it is created."""
    existing = db.get(model, record_id)
    if existing is not None:
        return existing, False
    instance = model(id=record_id, **fields)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance, True

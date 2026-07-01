"""User and Role - handbook Chapter 17 (Security) §17.2, §17.5.

RULE-SEC-103: every write is attributable to a specific authenticated user;
no anonymous or shared accounts.
"""
import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, FarmScopedMixin, TimestampMixin


class UserRole(str, enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    WORKER = "worker"
    VETERINARIAN = "veterinarian"
    FINANCE = "finance"
    READ_ONLY = "read_only"


class User(Base, FarmScopedMixin, TimestampMixin):
    __tablename__ = "app_user"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

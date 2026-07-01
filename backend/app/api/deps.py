"""Shared FastAPI dependencies: DB session, current user, and centralized
role enforcement (Chapter 17 §17.3-17.4, RULE-SEC-102: permissions are
enforced server-side, independent of any client UI state)."""
from collections.abc import Callable, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception
    user = db.get(User, user_id)
    if user is None or not user.active:
        raise credentials_exception
    return user


def require_roles(*allowed_roles: UserRole) -> Callable[[User], User]:
    """Centralized policy check (Ch.15 §15.4 RULE-API-102, Ch.17 §17.4
    RULE-SEC-102). Every new domain endpoint that needs restriction
    depends on this rather than re-implementing role checks per route."""

    def _check(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role.value}' is not permitted to perform this action.",
            )
        return current_user

    return _check

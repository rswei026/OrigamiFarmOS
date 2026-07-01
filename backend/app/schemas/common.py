"""Shared error envelope - handbook Chapter 15 §15.6. Every error response
shares one structure so the client renders consistent validation feedback
across every domain workflow."""
from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    field_errors: list[dict[str, Any]] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail

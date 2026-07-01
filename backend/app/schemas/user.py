import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    farm_id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    active: bool


class UserCreate(BaseModel):
    farm_id: uuid.UUID
    email: EmailStr
    full_name: str
    password: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

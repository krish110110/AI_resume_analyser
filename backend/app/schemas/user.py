from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.constants import UserRole


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    current_password: Optional[str] = None
    new_password: Optional[str] = Field(None, min_length=6)


class UserOut(UserBase):
    id: str
    role: UserRole
    is_active: bool = True

    model_config = {"from_attributes": True}

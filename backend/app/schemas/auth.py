from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    email: EmailStr
    role: str
    shop_id: UUID | None = None


class UserCreate(UserBase):
    role: str = "staff"
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: UUID
    is_active: bool
    shop_id: UUID

    class Config:
        from_attributes = True

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserSummary(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str


class CurrentUserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: str
    student_id: str | None = None
    teacher_id: str | None = None
    created_at: datetime

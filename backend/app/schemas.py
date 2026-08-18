from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models import Role, Status


# ---- Auth ----

class RegisterRequest(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role


# ---- Users ----

class UserOut(BaseModel):
    id: int
    username_or_email: str
    role: Role
    status: Status
    created_at: datetime

    class Config:
        from_attributes = True


class AdminCreateUserRequest(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)
    role: Role = Role.user
    status: Status = Status.active


class AdminUpdateUserRequest(BaseModel):
    status: Optional[Status] = None
    new_password: Optional[str] = Field(default=None, min_length=6, max_length=128)


# ---- Summarize ----

class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    language: Optional[str] = Field(default="tr", pattern="^(tr|en)$")


class SummarizeResponse(BaseModel):
    summary: str
    created_at: datetime


class LogOut(BaseModel):
    id: int
    user_id: int
    username_or_email: Optional[str] = None
    input_text: Optional[str]
    output_summary: str
    provider: str
    created_at: datetime

    class Config:
        from_attributes = True

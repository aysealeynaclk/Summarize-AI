import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Role(str, enum.Enum):
    admin = "admin"
    user = "user"


class Status(str, enum.Enum):
    pending = "pending"
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username_or_email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    status = Column(Enum(Status), nullable=False, default=Status.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = relationship("AILog", back_populates="user")


class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    input_text = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=False)
    provider = Column(String, nullable=False, default="groq")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="logs")

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, index=True)
    auth_hash = Column(String(255))
    master_key_salt = Column(String(64))
    encrypted_dek = Column(Text)
    role = Column(SQLEnum(UserRole), default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    requires_password_change = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    secrets = relationship("Secret", back_populates="owner", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

class Secret(Base):
    __tablename__ = "secrets"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=lambda: str(uuid4()))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    label = Column(String(255), nullable=False)
    encrypted_value = Column(Text)
    metadata = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="secrets")
    access_logs = relationship("AuditLog", back_populates="secret", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('owner_id', 'label', name='uq_user_secret_label'),)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    secret_id = Column(Integer, ForeignKey("secrets.id"), nullable=True)
    action = Column(String(50))
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
    secret = relationship("Secret", back_populates="access_logs")

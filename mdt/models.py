from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy import Enum, create_engine, DateTime, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
import enum

from .database import Base

class DeviceType(enum.Enum):
    Workstation = "Workstation"
    Laptop = "Laptop"


class Deparment(enum.Enum):
    Trading = "Trading"
    Development = "Development"


class Computer(Base):
    __tablename__ = "computers"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    department: Mapped[Deparment] = mapped_column(Enum(Deparment), nullable=False)
    type: Mapped[DeviceType] = mapped_column(Enum(DeviceType), nullable=False)
    is_available: Mapped[Boolean] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    lock: Mapped["Lock"] = relationship("Lock", back_populates="computer")
    user_id : Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    user : Mapped[Optional["User"]] = relationship("User", back_populates="computers")
    
class User(Base):
    __tablename__="users"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    samAccountName: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    ou: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    computers: Mapped[list["Computer"]] = relationship("Computer", back_populates="user")
    lock: Mapped["Lock"] = relationship("Lock", back_populates="user")

class Lock(Base):
    __tablename__ = "locks"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lock_time = Column(DateTime, default=datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    expire_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(days=1))
    
    computer_id: Mapped[str] = mapped_column(String, ForeignKey("computers.id"), nullable=False)
    computer: Mapped["Computer"] = relationship("Computer", back_populates="lock")
    
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="lock")
     
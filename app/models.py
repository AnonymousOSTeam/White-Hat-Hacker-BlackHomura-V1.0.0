from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="viewer")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Incident(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    created_by: Optional[int] = Field(foreign_key="user.id")
    status: str = Field(default="open")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: Optional[str]
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class IOC(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    value: str = Field(index=True)
    description: Optional[str]
    severity: str = Field(default="medium")
    created_at: datetime = Field(default_factory=datetime.utcnow)

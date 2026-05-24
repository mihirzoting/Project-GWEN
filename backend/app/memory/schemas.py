from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    session = 'session'
    long_term = 'long_term'
    workflow = 'workflow'


class PrivacyScope(str, Enum):
    session = 'session'
    user = 'user'
    workspace = 'workspace'


class SessionMessage(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    role: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: Optional[str] = None
    source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryCreate(BaseModel):
    content: str
    memory_type: MemoryType = MemoryType.long_term
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None
    correlation_id: Optional[str] = None
    privacy_scope: PrivacyScope = PrivacyScope.user
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    content: str
    memory_type: MemoryType
    tags: List[str] = Field(default_factory=list)
    source: Optional[str] = None
    correlation_id: Optional[str] = None
    privacy_scope: PrivacyScope = PrivacyScope.user
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MemoryContext(BaseModel):
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None
    messages: List[SessionMessage] = Field(default_factory=list)
    memories: List[MemoryEntry] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: uuid4().hex)
    version: str = '1.0'
    event: str
    correlation_id: Optional[str] = None
    payload: Dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = Field(default_factory=dict)

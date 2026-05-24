from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel

from ..memory.schemas import MemoryContext, MemoryEntry, MemoryEvent

EVENT_VERSION = '1.0'

MEMORY_CONTEXT = 'memory.context'
MEMORY_WRITE = 'memory.write'
MEMORY_DELETE = 'memory.delete'


class MemoryContextPayload(BaseModel):
    context: MemoryContext


class MemoryWritePayload(BaseModel):
    memory: MemoryEntry


class MemoryDeletePayload(BaseModel):
    memory_id: str


class MemoryContextEvent(MemoryEvent):
    event: Literal[MEMORY_CONTEXT]
    version: str = EVENT_VERSION
    payload: MemoryContextPayload
    correlation_id: Optional[str] = None


class MemoryWriteEvent(MemoryEvent):
    event: Literal[MEMORY_WRITE]
    version: str = EVENT_VERSION
    payload: MemoryWritePayload
    correlation_id: Optional[str] = None


class MemoryDeleteEvent(MemoryEvent):
    event: Literal[MEMORY_DELETE]
    version: str = EVENT_VERSION
    payload: MemoryDeletePayload
    correlation_id: Optional[str] = None

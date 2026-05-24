from __future__ import annotations

from typing import Optional, Protocol, Sequence

from .schemas import MemoryEntry, MemoryType, SessionMessage


class MemoryRepository(Protocol):
    async def add_message(self, session_id: str, message: SessionMessage) -> None: ...

    async def list_messages(
        self, session_id: str, limit: int
    ) -> list[SessionMessage]: ...

    async def create_memory(self, memory: MemoryEntry) -> MemoryEntry: ...

    async def list_memories(
        self,
        *,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[Sequence[str]] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[MemoryEntry]: ...

    async def delete_memory(self, memory_id: str) -> bool: ...

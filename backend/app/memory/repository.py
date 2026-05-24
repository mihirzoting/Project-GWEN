from __future__ import annotations

import asyncio
from typing import Optional, Sequence

from .interfaces import MemoryRepository
from .schemas import MemoryEntry, MemoryType, SessionMessage


class InMemoryMemoryRepository(MemoryRepository):
    def __init__(self) -> None:
        self._messages: dict[str, list[SessionMessage]] = {}
        self._memories: dict[str, MemoryEntry] = {}
        self._lock = asyncio.Lock()

    async def add_message(self, session_id: str, message: SessionMessage) -> None:
        async with self._lock:
            self._messages.setdefault(session_id, []).append(message)

    async def list_messages(
        self, session_id: str, limit: int
    ) -> list[SessionMessage]:
        async with self._lock:
            messages = self._messages.get(session_id, [])
            if limit <= 0:
                return []
            return list(messages[-limit:])

    async def create_memory(self, memory: MemoryEntry) -> MemoryEntry:
        async with self._lock:
            self._memories[memory.id] = memory
            return memory

    async def list_memories(
        self,
        *,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[Sequence[str]] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[MemoryEntry]:
        async with self._lock:
            memories = list(self._memories.values())

        if memory_type is not None:
            memories = [memory for memory in memories if memory.memory_type == memory_type]

        if source is not None:
            memories = [memory for memory in memories if memory.source == source]

        if tags:
            tag_set = set(tags)
            memories = [
                memory
                for memory in memories
                if tag_set.issubset(set(memory.tags))
            ]

        memories.sort(key=lambda memory: memory.created_at, reverse=True)

        if limit is not None:
            memories = memories[: max(limit, 0)]

        return memories

    async def delete_memory(self, memory_id: str) -> bool:
        async with self._lock:
            if memory_id in self._memories:
                del self._memories[memory_id]
                return True
            return False

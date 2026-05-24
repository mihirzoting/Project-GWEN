from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional

from app.core.constants import DEFAULT_SESSION_USER
from app.memory.embeddings.provider import EmbeddingsProvider
from app.memory.long_term.repository import SqlMemoryRepository
from app.memory.retrieval.chroma import ChromaMemoryStore
from app.memory.schemas import MemoryContext, MemoryEntry, MemoryType, SessionMessage
from app.memory.short_term.redis_store import RedisSessionRepository


def utc_now() -> datetime:
    return datetime.now(UTC)


class MemoryService:
    def __init__(
        self,
        *,
        short_term_repo: RedisSessionRepository,
        long_term_repo: SqlMemoryRepository,
        memory_store: ChromaMemoryStore,
        embeddings: EmbeddingsProvider,
        context_limit: int,
        similarity_k: int,
    ) -> None:
        self._short_term = short_term_repo
        self._long_term = long_term_repo
        self._memory_store = memory_store
        self._embeddings = embeddings
        self._context_limit = context_limit
        self._similarity_k = similarity_k

    async def ensure_user(self, user_id: str = DEFAULT_SESSION_USER) -> None:
        await self._long_term.ensure_user(user_id)

    async def ensure_conversation(self, conversation_id: str, user_id: str) -> None:
        await self._long_term.ensure_conversation(conversation_id, user_id)

    async def add_message(
        self,
        *,
        session_id: str,
        conversation_id: str,
        message: SessionMessage,
    ) -> None:
        await self._short_term.add_message(session_id, message)
        await self._long_term.add_message(conversation_id, message)

    async def get_recent_context(
        self,
        session_id: str,
        *,
        limit: Optional[int] = None,
        correlation_id: Optional[str] = None,
    ) -> MemoryContext:
        if limit is None:
            limit = self._context_limit
        messages = await self._short_term.list_messages(session_id, limit)
        return MemoryContext(
            session_id=session_id,
            correlation_id=correlation_id,
            messages=messages,
        )

    async def retrieve_memories(
        self,
        *,
        user_id: str,
        query: str,
    ) -> list[MemoryEntry]:
        matches = await self._memory_store.query(query=query, k=self._similarity_k)
        ids = {match['id'] for match in matches}
        memories = await self._long_term.list_memories(user_id=user_id)
        return [
            MemoryEntry(
                id=memory.id,
                content=memory.content,
                memory_type=MemoryType.long_term,
                tags=list(memory.tags or []),
                source=memory.source,
                metadata=memory.metadata or {},
            )
            for memory in memories
            if memory.id in ids
        ]

    async def create_memory(
        self,
        *,
        user_id: str,
        content: str,
        tags: list[str],
        source: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> MemoryEntry:
        entry = await self._long_term.create_memory(
            user_id=user_id,
            content=content,
            tags=tags,
            source=source,
            metadata=metadata or {},
        )
        await self._memory_store.upsert_memory(
            memory_id=entry.id,
            content=entry.content,
            metadata={'user_id': user_id, 'source': source or 'unknown'},
        )
        return MemoryEntry(
            id=entry.id,
            content=entry.content,
            memory_type=MemoryType.long_term,
            tags=list(entry.tags or []),
            source=entry.source,
            metadata=entry.metadata or {},
        )

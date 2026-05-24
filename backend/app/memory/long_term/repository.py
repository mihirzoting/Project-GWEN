from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.models import Conversation, MemoryRecord, Message, User
from app.memory.schemas import SessionMessage


class SqlMemoryRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def ensure_user(self, user_id: str) -> None:
        async with self._sessionmaker() as session:
            existing = await session.get(User, user_id)
            if existing:
                return
            session.add(User(id=user_id))
            await session.commit()

    async def ensure_conversation(self, conversation_id: str, user_id: str) -> None:
        async with self._sessionmaker() as session:
            existing = await session.get(Conversation, conversation_id)
            if existing:
                return
            session.add(Conversation(id=conversation_id, user_id=user_id))
            await session.commit()

    async def add_message(
        self, conversation_id: str, message: SessionMessage
    ) -> None:
        async with self._sessionmaker() as session:
            session.add(
                Message(
                    conversation_id=conversation_id,
                    role=message.role,
                    content=message.content,
                    correlation_id=message.correlation_id,
                    metadata=message.metadata,
                )
            )
            await session.commit()

    async def list_messages(
        self, conversation_id: str, limit: int
    ) -> list[Message]:
        async with self._sessionmaker() as session:
            stmt = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            return list(reversed(result.scalars().all()))

    async def create_memory(self, user_id: str, content: str, tags: list[str], source: str | None, metadata: dict) -> MemoryRecord:
        async with self._sessionmaker() as session:
            entry = MemoryRecord(
                user_id=user_id,
                content=content,
                tags=tags,
                source=source,
                metadata=metadata,
            )
            session.add(entry)
            await session.commit()
            await session.refresh(entry)
            return entry

    async def list_memories(
        self,
        *,
        user_id: str,
        tags: Optional[Sequence[str]] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[MemoryRecord]:
        async with self._sessionmaker() as session:
            stmt = select(MemoryRecord).where(MemoryRecord.user_id == user_id)
            if source:
                stmt = stmt.where(MemoryRecord.source == source)
            if tags:
                stmt = stmt.where(MemoryRecord.tags.contains(list(tags)))
            stmt = stmt.order_by(MemoryEntry.created_at.desc())
            if limit:
                stmt = stmt.limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

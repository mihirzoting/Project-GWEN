from __future__ import annotations

import json
from typing import Optional, Sequence

from redis.asyncio import Redis

from app.memory.schemas import MemoryEntry, MemoryType, SessionMessage


def _model_dump(model: SessionMessage) -> dict:
    if hasattr(model, 'model_dump'):
        return model.model_dump()
    return model.dict()


def _message_to_json(message: SessionMessage) -> str:
    return json.dumps(_model_dump(message))


def _message_from_json(raw: str | bytes) -> SessionMessage:
    if isinstance(raw, bytes):
        raw = raw.decode('utf-8')
    data = json.loads(raw)
    if hasattr(SessionMessage, 'model_validate'):
        return SessionMessage.model_validate(data)
    return SessionMessage.parse_obj(data)


class RedisSessionRepository:
    def __init__(
        self,
        redis: Redis,
        *,
        ttl_seconds: int,
        max_messages: int,
    ) -> None:
        self._redis = redis
        self._ttl_seconds = ttl_seconds
        self._max_messages = max_messages

    def _messages_key(self, session_id: str) -> str:
        return f'session:{session_id}:messages'

    async def add_message(self, session_id: str, message: SessionMessage) -> None:
        key = self._messages_key(session_id)
        payload = _message_to_json(message)
        pipeline = self._redis.pipeline()
        pipeline.rpush(key, payload)

        if self._max_messages > 0:
            pipeline.ltrim(key, -self._max_messages, -1)

        if self._ttl_seconds > 0:
            pipeline.expire(key, self._ttl_seconds)

        await pipeline.execute()

    async def list_messages(self, session_id: str, limit: int) -> list[SessionMessage]:
        key = self._messages_key(session_id)
        if limit <= 0:
            return []

        start = -limit
        end = -1
        payloads = await self._redis.lrange(key, start, end)
        return [_message_from_json(raw) for raw in payloads]

    async def create_memory(self, memory: MemoryEntry) -> MemoryEntry:
        raise NotImplementedError('Long-term memory is not implemented for Redis store.')

    async def list_memories(
        self,
        *,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[Sequence[str]] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[MemoryEntry]:
        raise NotImplementedError('Long-term memory is not implemented for Redis store.')

    async def delete_memory(self, memory_id: str) -> bool:
        raise NotImplementedError('Long-term memory is not implemented for Redis store.')

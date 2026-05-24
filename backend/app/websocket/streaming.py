from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional, Tuple


@dataclass
class StreamSession:
    session_id: str
    correlation_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    task: Optional[asyncio.Task] = None


class StreamRegistry:
    def __init__(self) -> None:
        self._streams: dict[Tuple[str, str], StreamSession] = {}
        self._lock = asyncio.Lock()

    async def register(self, session_id: str, correlation_id: str) -> StreamSession:
        async with self._lock:
            session = StreamSession(session_id=session_id, correlation_id=correlation_id)
            self._streams[(session_id, correlation_id)] = session
            return session

    async def get(self, session_id: str, correlation_id: str) -> Optional[StreamSession]:
        async with self._lock:
            return self._streams.get((session_id, correlation_id))

    async def set_task(
        self, session_id: str, correlation_id: str, task: asyncio.Task
    ) -> None:
        async with self._lock:
            session = self._streams.get((session_id, correlation_id))
            if session:
                session.task = task

    async def cancel(self, session_id: str, correlation_id: str) -> None:
        async with self._lock:
            session = self._streams.get((session_id, correlation_id))
            if not session:
                return
            session.cancel_event.set()
            task = session.task
            if task and not task.done():
                task.cancel()

    async def remove(self, session_id: str, correlation_id: str) -> None:
        async with self._lock:
            self._streams.pop((session_id, correlation_id), None)

    async def cancel_session(self, session_id: str) -> None:
        async with self._lock:
            keys = [key for key in self._streams if key[0] == session_id]
        for _, correlation_id in keys:
            await self.cancel(session_id, correlation_id)

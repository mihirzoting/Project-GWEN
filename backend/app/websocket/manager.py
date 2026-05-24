from __future__ import annotations

from typing import Any

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(session_id, set()).add(websocket)

    def disconnect(self, session_id: str, websocket: WebSocket) -> None:
        connections = self._connections.get(session_id)
        if not connections:
            return
        connections.discard(websocket)
        if not connections:
            self._connections.pop(session_id, None)

    def is_connected(self, session_id: str) -> bool:
        return bool(self._connections.get(session_id))

    def connection_count(self, session_id: str) -> int:
        return len(self._connections.get(session_id, set()))

    async def send(self, session_id: str, message: dict[str, Any]) -> None:
        connections = list(self._connections.get(session_id, set()))
        for websocket in connections:
            await websocket.send_json(message)

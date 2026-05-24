import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.websocket.manager import WebSocketManager
from app.websocket.streaming import StreamRegistry, StreamState


class DummyWebSocket:
    def __init__(self) -> None:
        self.accepted = False
        self.sent = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, message):
        self.sent.append(message)


@pytest.mark.asyncio
async def test_stream_state_lifecycle():
    registry = StreamRegistry()
    session = await registry.start_stream('session-1', 'corr-1', 'msg-1')
    assert session.state == StreamState.started

    first_index = await registry.next_token_index('session-1', 'corr-1')
    second_index = await registry.next_token_index('session-1', 'corr-1')
    assert (first_index, second_index) == (0, 1)

    await registry.complete_stream('session-1', 'corr-1')
    session = await registry.get_stream('session-1', 'corr-1')
    assert session.state == StreamState.complete


@pytest.mark.asyncio
async def test_stream_cancel_sets_flag():
    registry = StreamRegistry()
    await registry.start_stream('session-1', 'corr-2', 'msg-2')
    session = await registry.cancel_stream('session-1', 'corr-2', reason='user')
    assert session is not None
    assert session.cancelled is True
    assert session.state == StreamState.cancelled


@pytest.mark.asyncio
async def test_disconnect_cancels_session_streams():
    registry = StreamRegistry()
    await registry.start_stream('session-1', 'corr-3', 'msg-3')
    await registry.start_stream('session-1', 'corr-4', 'msg-4')

    await registry.cancel_session('session-1')

    stream_a = await registry.get_stream('session-1', 'corr-3')
    stream_b = await registry.get_stream('session-1', 'corr-4')
    assert stream_a.state == StreamState.cancelled
    assert stream_b.state == StreamState.cancelled


@pytest.mark.asyncio
async def test_websocket_manager_lifecycle():
    manager = WebSocketManager()
    websocket = DummyWebSocket()

    await manager.connect('session-1', websocket)
    assert manager.connection_count('session-1') == 1

    await manager.send('session-1', {'type': 'ping'})
    assert websocket.sent[-1]['type'] == 'ping'

    manager.disconnect('session-1', websocket)
    assert manager.connection_count('session-1') == 0

    await manager.connect('session-1', websocket)
    assert manager.is_connected('session-1') is True

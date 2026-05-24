import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

from app.memory.schemas import (
    MemoryContext,
    MemoryCreate,
    MemoryEntry,
    MemoryType,
    SessionMessage,
)
from app.websocket.events import (
    MEMORY_CONTEXT,
    MemoryContextEvent,
    MemoryContextPayload,
)


def test_memory_create_defaults():
    memory = MemoryCreate(content='Remember this')
    assert memory.memory_type == MemoryType.long_term
    assert memory.tags == []
    assert memory.metadata == {}


def test_memory_entry_fields():
    entry = MemoryEntry(content='Hello', memory_type=MemoryType.session)
    assert entry.id
    assert entry.created_at is not None
    assert entry.updated_at is not None


def test_memory_context_event_schema():
    message = SessionMessage(role='user', content='Hi')
    context = MemoryContext(session_id='session-1', messages=[message])
    event = MemoryContextEvent(
        event=MEMORY_CONTEXT,
        payload=MemoryContextPayload(context=context),
        correlation_id='corr-1',
    )
    assert event.version == '1.0'
    assert event.payload.context.session_id == 'session-1'

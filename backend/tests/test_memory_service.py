import asyncio
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

from app.memory.repository import InMemoryMemoryRepository
from app.memory.schemas import MemoryCreate, MemoryType, SessionMessage
from app.memory.service import MemoryService


def test_memory_service_flow():
    async def run_flow():
        repository = InMemoryMemoryRepository()
        service = MemoryService(repository)

        message = SessionMessage(role='user', content='Hello GEWN')
        await service.add_message('session-1', message)

        context = await service.get_recent_context('session-1')
        assert context.messages[-1].content == 'Hello GEWN'

        created = await service.create_memory(
            MemoryCreate(content='Prefers dark mode', memory_type=MemoryType.long_term)
        )
        memories = await service.list_memories()
        assert any(memory.id == created.id for memory in memories)

        deleted = await service.delete_memory(created.id)
        assert deleted is True

        deleted_again = await service.delete_memory(created.id)
        assert deleted_again is False

    asyncio.run(run_flow())

import asyncio
import pathlib
import sys
from uuid import uuid4

import pytest
from redis.asyncio import Redis


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.memory.redis_store import RedisSessionRepository
from app.memory.schemas import SessionMessage


async def _get_redis_client() -> Redis:
    client = Redis.from_url('redis://localhost:6379/0', decode_responses=True)
    try:
        await client.ping()
    except Exception:
        await client.aclose()
        pytest.skip('Redis is not available on localhost:6379')
    return client


@pytest.mark.asyncio
async def test_session_message_persistence():
    redis = await _get_redis_client()
    session_id = uuid4().hex
    key = f'session:{session_id}:messages'
    repo = RedisSessionRepository(redis, ttl_seconds=60, max_messages=10)

    await repo.add_message(session_id, SessionMessage(role='user', content='Hello'))
    messages = await repo.list_messages(session_id, limit=10)

    assert len(messages) == 1
    assert messages[0].content == 'Hello'

    await redis.delete(key)
    await redis.aclose()


@pytest.mark.asyncio
async def test_rolling_history_trims_oldest():
    redis = await _get_redis_client()
    session_id = uuid4().hex
    key = f'session:{session_id}:messages'
    repo = RedisSessionRepository(redis, ttl_seconds=60, max_messages=2)

    await repo.add_message(session_id, SessionMessage(role='user', content='One'))
    await repo.add_message(session_id, SessionMessage(role='user', content='Two'))
    await repo.add_message(session_id, SessionMessage(role='user', content='Three'))

    messages = await repo.list_messages(session_id, limit=10)
    contents = [message.content for message in messages]

    assert contents == ['Two', 'Three']

    await redis.delete(key)
    await redis.aclose()


@pytest.mark.asyncio
async def test_session_ttl_expiry():
    redis = await _get_redis_client()
    session_id = uuid4().hex
    key = f'session:{session_id}:messages'
    repo = RedisSessionRepository(redis, ttl_seconds=1, max_messages=10)

    await repo.add_message(session_id, SessionMessage(role='user', content='Temp'))
    await asyncio.sleep(1.2)

    messages = await repo.list_messages(session_id, limit=10)
    assert messages == []

    await redis.delete(key)
    await redis.aclose()


@pytest.mark.asyncio
async def test_session_isolation_between_ids():
    redis = await _get_redis_client()
    session_a = uuid4().hex
    session_b = uuid4().hex
    key_a = f'session:{session_a}:messages'
    key_b = f'session:{session_b}:messages'
    repo = RedisSessionRepository(redis, ttl_seconds=60, max_messages=10)

    await repo.add_message(session_a, SessionMessage(role='user', content='Alpha'))
    await repo.add_message(session_b, SessionMessage(role='user', content='Beta'))

    messages_a = await repo.list_messages(session_a, limit=10)
    messages_b = await repo.list_messages(session_b, limit=10)

    assert [message.content for message in messages_a] == ['Alpha']
    assert [message.content for message in messages_b] == ['Beta']

    await redis.delete(key_a, key_b)
    await redis.aclose()

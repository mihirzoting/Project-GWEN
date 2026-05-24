from __future__ import annotations

from typing import AsyncIterator

from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings, get_settings


def get_app_settings() -> Settings:
    return get_settings()


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


async def get_db_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = request.app.state.db_sessionmaker
    async with session_factory() as session:
        yield session


def get_memory_service(request: Request):
    return request.app.state.memory_service


def get_ai_orchestrator(request: Request):
    return request.app.state.ai_orchestrator


def get_tool_registry(request: Request):
    return request.app.state.tool_registry


def get_vision_service(request: Request):
    return request.app.state.vision_service


def get_settings_dep(settings: Settings = Depends(get_app_settings)) -> Settings:
    return settings

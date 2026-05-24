from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def create_engine_and_sessionmaker(database_url: str):
    engine = create_async_engine(
        database_url,
        pool_pre_ping=True,
        future=True,
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return engine, sessionmaker

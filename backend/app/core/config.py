from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'GEWN'
    environment: str = 'development'
    api_prefix: str = '/api'
    log_level: str = 'INFO'

    cors_origins: List[str] = Field(default_factory=lambda: ['http://localhost:5173'])

    redis_url: str = 'redis://localhost:6379/0'
    database_url: str = 'postgresql+asyncpg://postgres:password@localhost:5432/gewn'
    chroma_path: str = './data/chroma'
    screenshots_path: str = './data/screens'
    tool_root: str = '.'

    openai_api_key: Optional[str] = None
    openai_model: str = 'gpt-4o-mini'
    gemini_api_key: Optional[str] = None
    gemini_model: str = 'gemini-1.5-flash'
    default_provider: str = 'openai'
    embeddings_model: str = 'text-embedding-3-small'

    request_timeout_seconds: int = 60
    stream_timeout_seconds: int = 90

    session_ttl_seconds: int = 3600
    session_max_messages: int = 50
    session_context_limit: int = 20
    memory_similarity_k: int = 6

    enable_tools: bool = True
    enable_ocr: bool = True
    terminal_allowlist: List[str] = Field(default_factory=lambda: ['echo'])
    terminal_timeout_seconds: int = 8

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=False,
    )

    @field_validator('cors_origins', mode='before')
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def load_config() -> Settings:
    return get_settings()

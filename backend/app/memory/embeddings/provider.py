from __future__ import annotations

from typing import List, Protocol

from openai import AsyncOpenAI

from app.core.config import Settings


class EmbeddingsProvider(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class OpenAIEmbeddingsProvider:
    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError('OPENAI_API_KEY is required for embeddings')
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.embeddings_model

    async def embed(self, texts: list[str]) -> list[list[float]]:
        response = await self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]


class NullEmbeddingsProvider:
    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 1536 for _ in texts]


class EmbeddingsProviderFactory:
    @staticmethod
    def from_settings(settings: Settings) -> EmbeddingsProvider:
        if settings.openai_api_key:
            return OpenAIEmbeddingsProvider(settings)
        return NullEmbeddingsProvider()

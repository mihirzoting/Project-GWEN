from __future__ import annotations

from typing import Any

from chromadb import PersistentClient

from app.memory.embeddings.provider import EmbeddingsProvider


class ChromaMemoryStore:
    def __init__(self, client: PersistentClient, embeddings: EmbeddingsProvider) -> None:
        self._client = client
        self._embeddings = embeddings
        self._collection = self._client.get_or_create_collection('gewn_memories')

    async def upsert_memory(self, *, memory_id: str, content: str, metadata: dict[str, Any]) -> None:
        vectors = await self._embeddings.embed([content])
        self._collection.upsert(
            ids=[memory_id],
            embeddings=vectors,
            documents=[content],
            metadatas=[metadata],
        )

    async def query(self, *, query: str, k: int) -> list[dict[str, Any]]:
        vectors = await self._embeddings.embed([query])
        results = self._collection.query(
            query_embeddings=vectors,
            n_results=k,
            include=['metadatas', 'distances', 'documents'],
        )
        matches = []
        for idx, memory_id in enumerate(results['ids'][0]):
            matches.append(
                {
                    'id': memory_id,
                    'distance': results['distances'][0][idx],
                    'metadata': results['metadatas'][0][idx],
                    'document': results['documents'][0][idx],
                }
            )
        return matches

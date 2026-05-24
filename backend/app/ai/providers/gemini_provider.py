from __future__ import annotations

from typing import AsyncIterator

import google.generativeai as genai

from .base import AIProvider, ChatMessage, StreamResult, ToolDefinition
from app.core.config import Settings


class GeminiProvider(AIProvider):
    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise ValueError('GEMINI_API_KEY is required for Gemini provider')
        genai.configure(api_key=settings.gemini_api_key)
        self._model = genai.GenerativeModel(settings.gemini_model)

    async def stream_chat(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
        cancellation_event,
    ) -> AsyncIterator[StreamResult]:
        history = []
        for message in messages:
            if message.role == 'system':
                history.append({'role': 'user', 'parts': [message.content]})
            else:
                history.append({'role': message.role, 'parts': [message.content]})

        response = await self._model.generate_content_async(
            [m['parts'][0] for m in history], stream=True
        )

        index = 0
        async for chunk in response:
            if cancellation_event.is_set():
                break
            text = chunk.text or ''
            if text:
                yield StreamResult(event='token', payload={'token': text, 'index': index})
                index += 1

        yield StreamResult(event='complete', payload={'usage': {}})

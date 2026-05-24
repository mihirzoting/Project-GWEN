from __future__ import annotations

import json
from typing import Any, AsyncIterator

from openai import AsyncOpenAI

from .base import AIProvider, ChatMessage, StreamResult, ToolDefinition
from app.core.config import Settings


class OpenAIProvider(AIProvider):
    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError('OPENAI_API_KEY is required for OpenAI provider')
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self._timeout = settings.stream_timeout_seconds

    @property
    def model(self) -> str:
        return self._model

    async def stream_chat(
        self,
        *,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
        cancellation_event,
    ) -> AsyncIterator[StreamResult]:
        openai_messages: list[dict[str, Any]] = []
        for message in messages:
            payload = {'role': message.role, 'content': message.content}
            if message.name:
                payload['name'] = message.name
            if message.tool_call_id:
                payload['tool_call_id'] = message.tool_call_id
            openai_messages.append(payload)

        tool_payload = [
            {
                'type': 'function',
                'function': {
                    'name': tool.name,
                    'description': tool.description,
                    'parameters': tool.parameters,
                },
            }
            for tool in tools
        ]

        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=openai_messages,
            tools=tool_payload or None,
            stream=True,
            stream_options={'include_usage': True},
            temperature=0.4,
            timeout=self._timeout,
        )

        tool_calls: dict[int, dict[str, Any]] = {}
        index = 0
        usage: dict[str, Any] = {}

        async for chunk in stream:
            if cancellation_event.is_set():
                break

            choice = chunk.choices[0]
            delta = choice.delta

            if delta.content:
                yield StreamResult(
                    event='token',
                    payload={'token': delta.content, 'index': index},
                )
                index += 1

            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    entry = tool_calls.setdefault(
                        tool_call.index,
                        {
                            'id': tool_call.id,
                            'name': tool_call.function.name if tool_call.function else None,
                            'arguments': '',
                        },
                    )
                    if tool_call.function and tool_call.function.arguments:
                        entry['arguments'] += tool_call.function.arguments

            if chunk.usage:
                usage = chunk.usage.model_dump()

        if tool_calls:
            parsed_calls = []
            for call in tool_calls.values():
                args_raw = call.get('arguments') or ''
                try:
                    args = json.loads(args_raw) if args_raw else {}
                except json.JSONDecodeError:
                    args = {'_raw': args_raw}
                parsed_calls.append(
                    {
                        'id': call.get('id') or '',
                        'name': call.get('name') or '',
                        'arguments': args,
                    }
                )
            yield StreamResult(event='tool_calls', payload={'tool_calls': parsed_calls})
            return

        yield StreamResult(event='complete', payload={'usage': usage})

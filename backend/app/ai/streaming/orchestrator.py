from __future__ import annotations

import asyncio
from typing import AsyncIterator
from uuid import uuid4

from app.ai.context.builder import build_chat_messages
from app.ai.providers import ChatMessage, GeminiProvider, OpenAIProvider, ToolDefinition
from app.ai.streaming.schemas import (
    StreamCancelledPayload,
    StreamCompletePayload,
    StreamErrorPayload,
    StreamStartPayload,
    TokenPayload,
    ToolCallPayload,
    ToolResultPayload,
    build_event,
)
from app.core import constants
from app.core.config import Settings
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.tools.schemas import ToolCall


class AIOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._providers = {}
        if settings.openai_api_key:
            self._providers['openai'] = OpenAIProvider(settings)
        if settings.gemini_api_key:
            self._providers['gemini'] = GeminiProvider(settings)

    def _get_provider(self):
        provider = self._providers.get(self._settings.default_provider)
        if provider is None:
            raise RuntimeError('No valid AI provider configured')
        return provider

    async def stream_response(
        self,
        *,
        session_id: str,
        correlation_id: str,
        user_message: str,
        history,
        memories,
        screen_context: str | None,
        tool_registry: ToolRegistry,
        tool_executor: ToolExecutor,
        db_session,
        cancellation_event: asyncio.Event,
    ) -> AsyncIterator:
        provider = self._get_provider()
        message_id = uuid4().hex

        yield build_event(
            event=constants.STREAM_START,
            session_id=session_id,
            correlation_id=correlation_id,
            payload=StreamStartPayload(message_id=message_id, model=provider.model),
        )

        messages = build_chat_messages(
            history=history,
            user_message=user_message,
            memories=memories,
            screen_context=screen_context,
        )

        tools = [
            ToolDefinition(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters,
            )
            for tool in tool_registry.list()
        ]

        total_tokens = 0
        usage = {}
        tool_calls: list[ToolCall] = []
        index = 0

        try:
            async for result in provider.stream_chat(
                messages=messages,
                tools=tools,
                cancellation_event=cancellation_event,
            ):
                if cancellation_event.is_set():
                    break
                if result.event == 'token':
                    token = result.payload.get('token', '')
                    yield build_event(
                        event=constants.STREAM_TOKEN,
                        session_id=session_id,
                        correlation_id=correlation_id,
                        payload=TokenPayload(
                            message_id=message_id,
                            token=token,
                            index=index,
                        ),
                    )
                    index += 1
                    total_tokens += 1
                elif result.event == 'tool_calls':
                    for call in result.payload.get('tool_calls', []):
                        tool_calls.append(
                            ToolCall(
                                tool_call_id=call.get('id', uuid4().hex),
                                name=call.get('name', ''),
                                arguments=call.get('arguments', {}),
                            )
                        )
                elif result.event == 'complete':
                    usage = result.payload.get('usage', {})

            if cancellation_event.is_set():
                yield build_event(
                    event=constants.STREAM_CANCELLED,
                    session_id=session_id,
                    correlation_id=correlation_id,
                    payload=StreamCancelledPayload(message_id=message_id, reason='cancelled'),
                )
                return

            if tool_calls:
                for call in tool_calls:
                    tool_def = tool_registry.get(call.name)
                    risk_tier = tool_def.risk_tier.value if tool_def else 'T4'
                    requires_approval = tool_def and tool_def.risk_tier.value != 'T1'
                    confirmation = None
                    confirmation_text = None
                    if tool_def:
                        from app.tools.risk import confirmation_type

                        confirmation = confirmation_type(tool_def.risk_tier)
                        if confirmation == 'typed':
                            confirmation_text = f'CONFIRM {tool_def.name}'

                    yield build_event(
                        event=constants.STREAM_TOOL_CALL,
                        session_id=session_id,
                        correlation_id=correlation_id,
                        payload=ToolCallPayload(
                            tool_call_id=call.tool_call_id,
                            tool_name=call.name,
                            arguments=call.arguments,
                            risk_tier=risk_tier,
                            requires_approval=requires_approval,
                            confirmation_type=confirmation,
                            confirmation_text=confirmation_text,
                        ),
                    )

                    tool_result = await tool_executor.execute_call(
                        tool_call=call, db_session=db_session
                    )
                    yield build_event(
                        event=constants.STREAM_TOOL_RESULT,
                        session_id=session_id,
                        correlation_id=correlation_id,
                        payload=ToolResultPayload(
                            tool_call_id=tool_result.tool_call_id,
                            tool_name=tool_result.name,
                            status=tool_result.status,
                            result=tool_result.result,
                        ),
                    )

                    if tool_result.status == 'requires_approval':
                        return

            yield build_event(
                event=constants.STREAM_COMPLETE,
                session_id=session_id,
                correlation_id=correlation_id,
                payload=StreamCompletePayload(
                    message_id=message_id,
                    total_tokens=total_tokens,
                    usage=usage,
                ),
            )
        except Exception as exc:  # pragma: no cover
            yield build_event(
                event=constants.STREAM_ERROR,
                session_id=session_id,
                correlation_id=correlation_id,
                payload=StreamErrorPayload(message_id=message_id, error=str(exc)),
            )

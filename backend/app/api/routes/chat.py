from __future__ import annotations

import asyncio
from typing import Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from app.core.constants import DEFAULT_CONVERSATION_ID_PREFIX, DEFAULT_SESSION_USER
from app.core.logger import get_logger
from app.ai.streaming.schemas import ToolResultPayload, build_event
from app.core import constants
from app.memory.schemas import SessionMessage
from app.tools.executor import ToolExecutor
from app.websocket.manager import WebSocketManager
from app.websocket.streaming import StreamRegistry


router = APIRouter()
logger = get_logger('gewn.chat')


class ChatMessagePayload(BaseModel):
    event: Literal['chat.message'] = 'chat.message'
    role: Literal['user'] = 'user'
    content: str
    correlation_id: Optional[str] = Field(default=None)
    include_screen: bool = False


class ChatCancelPayload(BaseModel):
    event: Literal['chat.cancel'] = 'chat.cancel'
    correlation_id: Optional[str] = None


class ToolApprovalPayload(BaseModel):
    event: Literal['tool.approve'] = 'tool.approve'
    tool_call_id: str
    confirmation_text: Optional[str] = None


class ToolDenyPayload(BaseModel):
    event: Literal['tool.deny'] = 'tool.deny'
    tool_call_id: str


def _get_manager(websocket: WebSocket) -> WebSocketManager:
    manager = getattr(websocket.app.state, 'websocket_manager', None)
    if manager is None:
        manager = WebSocketManager()
        websocket.app.state.websocket_manager = manager
    return manager


def _get_registry(websocket: WebSocket) -> StreamRegistry:
    registry = getattr(websocket.app.state, 'stream_registry', None)
    if registry is None:
        registry = StreamRegistry()
        websocket.app.state.stream_registry = registry
    return registry


@router.websocket('/ws/chat/{session_id}')
async def chat_websocket(websocket: WebSocket, session_id: str) -> None:
    manager = _get_manager(websocket)
    registry = _get_registry(websocket)
    memory_service = websocket.app.state.memory_service
    ai_orchestrator = websocket.app.state.ai_orchestrator
    tool_registry = websocket.app.state.tool_registry
    tool_executor = websocket.app.state.tool_executor
    vision_service = websocket.app.state.vision_service
    db_sessionmaker = websocket.app.state.db_sessionmaker

    await manager.connect(session_id, websocket)

    user_id = DEFAULT_SESSION_USER
    conversation_id = f'{DEFAULT_CONVERSATION_ID_PREFIX}{session_id}'

    await memory_service.ensure_user(user_id)
    await memory_service.ensure_conversation(conversation_id, user_id)

    try:
        while True:
            payload = await websocket.receive_json()
            event = payload.get('event') or 'chat.message'

            if event == 'chat.cancel':
                cancel = ChatCancelPayload(**payload)
                if cancel.correlation_id:
                    await registry.cancel(session_id, cancel.correlation_id)
                continue

            if event == 'tool.approve':
                approval = ToolApprovalPayload(**payload)
                async with db_sessionmaker() as db_session:
                    result = await tool_executor.approve(
                        tool_call_id=approval.tool_call_id,
                        db_session=db_session,
                        confirmation_text=approval.confirmation_text,
                    )
                tool_event = build_event(
                    event=constants.STREAM_TOOL_RESULT,
                    session_id=session_id,
                    correlation_id=approval.tool_call_id,
                    payload=ToolResultPayload(
                        tool_call_id=result.tool_call_id,
                        tool_name=result.name,
                        status=result.status,
                        result=result.result,
                    ),
                )
                await manager.send(session_id, tool_event.model_dump())
                continue

            if event == 'tool.deny':
                denial = ToolDenyPayload(**payload)
                await manager.send(
                    session_id,
                    build_event(
                        event=constants.STREAM_TOOL_RESULT,
                        session_id=session_id,
                        correlation_id=denial.tool_call_id,
                        payload=ToolResultPayload(
                            tool_call_id=denial.tool_call_id,
                            tool_name='',
                            status='denied',
                            result={'error': 'User denied the request'},
                        ),
                    ).model_dump(),
                )
                continue

            message = ChatMessagePayload(**payload)
            correlation_id = message.correlation_id or uuid4().hex

            session_message = SessionMessage(
                role=message.role,
                content=message.content,
                correlation_id=correlation_id,
            )

            await memory_service.add_message(
                session_id=session_id,
                conversation_id=conversation_id,
                message=session_message,
            )

            context = await memory_service.get_recent_context(
                session_id, correlation_id=correlation_id
            )

            memories = await memory_service.retrieve_memories(
                user_id=user_id, query=message.content
            )

            screen_context = None
            if message.include_screen:
                screen_context = await vision_service.capture_and_extract(session_id)
            else:
                screen_context = vision_service.get_last_context(session_id)

            stream_session = await registry.register(session_id, correlation_id)

            async def _stream() -> None:
                assistant_text = ''
                async with db_sessionmaker() as db_session:
                    async for event_payload in ai_orchestrator.stream_response(
                        session_id=session_id,
                        correlation_id=correlation_id,
                        user_message=message.content,
                        history=context.messages,
                        memories=memories,
                        screen_context=screen_context,
                        tool_registry=tool_registry,
                        tool_executor=tool_executor,
                        db_session=db_session,
                        cancellation_event=stream_session.cancel_event,
                    ):
                        if event_payload.event == 'token':
                            assistant_text += event_payload.payload.get('token', '')
                        await manager.send(session_id, event_payload.model_dump())

                if assistant_text.strip():
                    await memory_service.add_message(
                        session_id=session_id,
                        conversation_id=conversation_id,
                        message=SessionMessage(
                            role='assistant',
                            content=assistant_text.strip(),
                            correlation_id=correlation_id,
                        ),
                    )

            task = asyncio.create_task(_stream())
            await registry.set_task(session_id, correlation_id, task)
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)
        await registry.cancel_session(session_id)
    finally:
        manager.disconnect(session_id, websocket)

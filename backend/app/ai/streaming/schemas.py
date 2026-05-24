from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.core import constants


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class StreamEvent(BaseModel):
    event: str
    session_id: str
    correlation_id: str
    created_at: str = Field(default_factory=utc_now)
    payload: dict[str, Any]


class StreamStartPayload(BaseModel):
    message_id: str
    model: str


class TokenPayload(BaseModel):
    message_id: str
    token: str
    index: int


class ToolCallPayload(BaseModel):
    tool_call_id: str
    tool_name: str
    arguments: dict[str, Any]
    risk_tier: str
    requires_approval: bool
    confirmation_type: Optional[str] = None
    confirmation_text: Optional[str] = None


class ToolResultPayload(BaseModel):
    tool_call_id: str
    tool_name: str
    status: str
    result: dict[str, Any]


class StreamCompletePayload(BaseModel):
    message_id: str
    total_tokens: int
    usage: dict[str, Any] = Field(default_factory=dict)


class StreamErrorPayload(BaseModel):
    message_id: Optional[str]
    error: str
    code: Optional[str] = None


class StreamCancelledPayload(BaseModel):
    message_id: Optional[str]
    reason: Optional[str] = None


def build_event(
    *,
    event: str,
    session_id: str,
    correlation_id: str,
    payload: BaseModel,
) -> StreamEvent:
    return StreamEvent(
        event=event,
        session_id=session_id,
        correlation_id=correlation_id,
        payload=payload.model_dump(),
    )


__all__ = [
    'StreamEvent',
    'StreamStartPayload',
    'TokenPayload',
    'ToolCallPayload',
    'ToolResultPayload',
    'StreamCompletePayload',
    'StreamErrorPayload',
    'StreamCancelledPayload',
    'build_event',
    'constants',
]

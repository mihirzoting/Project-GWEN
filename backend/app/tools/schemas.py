from __future__ import annotations

from typing import Any, Callable, Awaitable

from pydantic import BaseModel, Field

from .risk import RiskTier


class ToolCall(BaseModel):
    tool_call_id: str
    name: str
    arguments: dict[str, Any]


class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    status: str
    result: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
    risk_tier: RiskTier
    handler: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

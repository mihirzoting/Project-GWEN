from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from .audit import log_tool_event
from .permissions import should_auto_execute, validate_typed_confirmation
from .risk import RiskTier, confirmation_type
from .schemas import ToolCall, ToolResult
from .registry import ToolRegistry


@dataclass
class PendingTool:
    call: ToolCall
    risk_tier: RiskTier
    confirmation_type: str | None
    confirmation_text: str | None


class ToolExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry
        self._pending: dict[str, PendingTool] = {}

    def get_pending(self, tool_call_id: str) -> PendingTool | None:
        return self._pending.get(tool_call_id)

    async def execute_call(
        self,
        *,
        tool_call: ToolCall,
        db_session: AsyncSession,
    ) -> ToolResult:
        tool = self._registry.get(tool_call.name)
        if not tool:
            return ToolResult(
                tool_call_id=tool_call.tool_call_id,
                name=tool_call.name,
                status='error',
                result={'error': 'Unknown tool'},
            )

        if not should_auto_execute(tool.risk_tier):
            confirmation = confirmation_type(tool.risk_tier)
            confirmation_text = (
                f'CONFIRM {tool.name}' if confirmation == 'typed' else None
            )
            pending = PendingTool(
                call=tool_call,
                risk_tier=tool.risk_tier,
                confirmation_type=confirmation,
                confirmation_text=confirmation_text,
            )
            self._pending[tool_call.tool_call_id] = pending
            return ToolResult(
                tool_call_id=tool_call.tool_call_id,
                name=tool_call.name,
                status='requires_approval',
                result={
                    'confirmation_type': confirmation,
                    'confirmation_text': confirmation_text,
                },
            )

        result_payload: dict[str, Any] = {}
        status = 'success'
        try:
            result_payload = await tool.handler(tool_call.arguments)
        except Exception as exc:  # pragma: no cover
            status = 'error'
            result_payload = {'error': str(exc)}

        await log_tool_event(
            db_session,
            tool_name=tool.name,
            risk_tier=tool.risk_tier.value,
            status=status,
            input_payload=tool_call.arguments,
            output_payload=result_payload,
        )
        return ToolResult(
            tool_call_id=tool_call.tool_call_id,
            name=tool.name,
            status=status,
            result=result_payload,
        )

    async def approve(
        self,
        *,
        tool_call_id: str,
        db_session: AsyncSession,
        confirmation_text: str | None = None,
    ) -> ToolResult:
        pending = self._pending.pop(tool_call_id, None)
        if not pending:
            return ToolResult(
                tool_call_id=tool_call_id,
                name='unknown',
                status='error',
                result={'error': 'No pending tool call'},
            )

        if pending.confirmation_type == 'typed':
            if not validate_typed_confirmation(
                pending.confirmation_text, confirmation_text
            ):
                return ToolResult(
                    tool_call_id=tool_call_id,
                    name=pending.call.name,
                    status='denied',
                    result={'error': 'Typed confirmation did not match'},
                )

        tool = self._registry.get(pending.call.name)
        if not tool:
            return ToolResult(
                tool_call_id=tool_call_id,
                name=pending.call.name,
                status='error',
                result={'error': 'Unknown tool'},
            )

        result_payload: dict[str, Any] = {}
        status = 'success'
        try:
            result_payload = await tool.handler(pending.call.arguments)
        except Exception as exc:  # pragma: no cover
            status = 'error'
            result_payload = {'error': str(exc)}

        await log_tool_event(
            db_session,
            tool_name=tool.name,
            risk_tier=tool.risk_tier.value,
            status=status,
            input_payload=pending.call.arguments,
            output_payload=result_payload,
        )
        return ToolResult(
            tool_call_id=tool_call_id,
            name=tool.name,
            status=status,
            result=result_payload,
        )

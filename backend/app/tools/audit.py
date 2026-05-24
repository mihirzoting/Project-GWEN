from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ToolAudit


async def log_tool_event(
    session: AsyncSession,
    *,
    tool_name: str,
    risk_tier: str,
    status: str,
    input_payload: dict,
    output_payload: dict,
) -> None:
    audit = ToolAudit(
        tool_name=tool_name,
        risk_tier=risk_tier,
        status=status,
        input=input_payload,
        output=output_payload,
    )
    session.add(audit)
    await session.commit()

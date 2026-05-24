from __future__ import annotations

from typing import Iterable, Optional

from app.ai.prompts.system import SYSTEM_PROMPT
from app.ai.prompts.tools import TOOLS_PROMPT
from app.ai.providers import ChatMessage
from app.memory.schemas import MemoryEntry, SessionMessage


def _format_memory(memories: Iterable[MemoryEntry]) -> str:
    items = [f"- {memory.content}" for memory in memories]
    if not items:
        return ''
    return "Relevant memory:\n" + "\n".join(items)


def _format_screen_context(screen_context: Optional[str]) -> str:
    if not screen_context:
        return ''
    return f"Screen context:\n{screen_context}"


def build_chat_messages(
    *,
    history: Iterable[SessionMessage],
    user_message: str,
    memories: Iterable[MemoryEntry],
    screen_context: Optional[str],
) -> list[ChatMessage]:
    system_parts = [SYSTEM_PROMPT, TOOLS_PROMPT]
    memory_text = _format_memory(memories)
    if memory_text:
        system_parts.append(memory_text)
    screen_text = _format_screen_context(screen_context)
    if screen_text:
        system_parts.append(screen_text)

    system_message = ChatMessage(
        role='system',
        content="\n\n".join(system_parts),
    )

    messages = [system_message]
    for message in history:
        messages.append(ChatMessage(role=message.role, content=message.content))

    messages.append(ChatMessage(role='user', content=user_message))
    return messages

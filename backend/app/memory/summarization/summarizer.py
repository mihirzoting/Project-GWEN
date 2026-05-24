from __future__ import annotations

from app.ai.providers import ChatMessage
from app.ai.providers.openai_provider import OpenAIProvider
from app.core.config import Settings


class ConversationSummarizer:
    def __init__(self, settings: Settings) -> None:
        self._provider = OpenAIProvider(settings)

    async def summarize(self, messages: list[ChatMessage]) -> str:
        prompt = (
            "Summarize the conversation in 4-6 bullet points focused on user intent, "
            "actions taken, and unresolved items."
        )
        summary_messages = [ChatMessage(role='system', content=prompt)] + messages

        text = ''
        async for result in self._provider.stream_chat(
            messages=summary_messages, tools=[], cancellation_event=_NullEvent()
        ):
            if result.event == 'token':
                text += result.payload.get('token', '')
        return text.strip()


class _NullEvent:
    def is_set(self) -> bool:
        return False

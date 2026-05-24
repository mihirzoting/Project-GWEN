from __future__ import annotations

from typing import Optional

from app.core.config import Settings
from .capture import capture_screen
from .ocr import extract_text
from .summarizer import summarize_ocr


class VisionService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._last_context: dict[str, str] = {}

    async def capture_and_extract(self, session_id: str) -> str:
        if not self._settings.enable_ocr:
            return ''
        image_bytes = capture_screen()
        text = extract_text(image_bytes)
        summary = summarize_ocr(text)
        self._last_context[session_id] = summary
        return summary

    def get_last_context(self, session_id: str) -> Optional[str]:
        return self._last_context.get(session_id)

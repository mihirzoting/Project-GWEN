from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    code: Optional[str] = None
    details: Optional[dict[str, Any]] = None


@dataclass
class AppError(Exception):
    message: str
    status_code: int = 400
    code: Optional[str] = None
    details: Optional[dict[str, Any]] = None

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(
            error=self.message,
            code=self.code,
            details=self.details,
        )

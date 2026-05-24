from __future__ import annotations

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logger import get_logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, log_name: str = 'gewn.request') -> None:
        super().__init__(app)
        self._logger = get_logger(log_name)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = (time.perf_counter() - start) * 1000
        self._logger.info(
            '%s %s -> %s (%.2fms)',
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )
        return response

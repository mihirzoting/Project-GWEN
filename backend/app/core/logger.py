from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(level: str = 'INFO') -> None:
    logging.basicConfig(
        level=level.upper(),
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    for noisy in ('uvicorn.error', 'uvicorn.access'):
        logging.getLogger(noisy).setLevel(level.upper())


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name or 'gewn')

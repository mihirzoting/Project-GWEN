from __future__ import annotations

import io

from mss import mss
from PIL import Image


def capture_screen() -> bytes:
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return buffer.getvalue()

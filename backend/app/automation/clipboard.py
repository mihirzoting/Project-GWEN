from __future__ import annotations

import pyperclip


async def read_clipboard(args: dict) -> dict:
    return {'text': pyperclip.paste()}


async def write_clipboard(args: dict) -> dict:
    text = args.get('text', '')
    pyperclip.copy(text)
    return {'written': True}

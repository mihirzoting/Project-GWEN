from __future__ import annotations

import shlex
import subprocess

from app.core.config import get_settings


async def execute_command(args: dict) -> dict:
    command = args.get('command', '').strip()
    if not command:
        return {'error': 'Command is empty'}

    settings = get_settings()
    allowlist = {item.lower() for item in settings.terminal_allowlist}
    parts = shlex.split(command, posix=False)
    if not parts:
        return {'error': 'Command is invalid'}
    executable = parts[0].lower()

    if executable not in allowlist:
        return {'error': 'Command not allowed by sandbox'}

    completed = subprocess.run(
        parts,
        capture_output=True,
        text=True,
        timeout=settings.terminal_timeout_seconds,
    )
    return {
        'returncode': completed.returncode,
        'stdout': completed.stdout,
        'stderr': completed.stderr,
    }

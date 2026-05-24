from __future__ import annotations

import os
import shutil
from pathlib import Path

from app.core.config import get_settings


def _resolve_path(raw: str) -> Path:
    root = Path(get_settings().tool_root).resolve()
    path = Path(raw).expanduser().resolve()
    if root not in path.parents and path != root:
        raise ValueError('Path is outside allowed scope')
    return path


async def read_directory(args: dict) -> dict:
    path = _resolve_path(args['path'])
    if not path.exists():
        return {'error': 'Path does not exist'}
    if not path.is_dir():
        return {'error': 'Path is not a directory'}
    entries = []
    for entry in path.iterdir():
        entries.append(
            {
                'name': entry.name,
                'type': 'dir' if entry.is_dir() else 'file',
            }
        )
    return {'entries': entries}


async def create_folder(args: dict) -> dict:
    path = _resolve_path(args['path'])
    path.mkdir(parents=True, exist_ok=True)
    return {'created': str(path)}


async def move_file(args: dict) -> dict:
    source = _resolve_path(args['source'])
    destination = _resolve_path(args['destination'])
    if not source.exists():
        return {'error': 'Source does not exist'}
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    return {'moved': {'from': str(source), 'to': str(destination)}}

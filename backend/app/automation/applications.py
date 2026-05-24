from __future__ import annotations

import os
import subprocess


async def open_application(args: dict) -> dict:
    target = args['target']
    if os.path.exists(target):
        os.startfile(target)  # nosec - intentional OS open
        return {'status': 'opened', 'target': target}
    return {
        'status': 'unsupported',
        'message': 'Provide a full path to the executable or app shortcut.',
    }


async def focus_application(args: dict) -> dict:
    target = args['target']
    return {
        'status': 'unsupported',
        'message': f'Focus not implemented yet for {target}.',
    }

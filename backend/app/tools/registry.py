from __future__ import annotations

from typing import Iterable

from .schemas import ToolDefinition
from .risk import RiskTier
from app.automation import applications, clipboard, filesystem, terminal


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition | None:
        return self._tools.get(name)

    def list(self) -> Iterable[ToolDefinition]:
        return self._tools.values()


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name='read_directory',
            description='List files and folders in a directory.',
            parameters={
                'type': 'object',
                'properties': {'path': {'type': 'string'}},
                'required': ['path'],
            },
            risk_tier=RiskTier.T1,
            handler=filesystem.read_directory,
        )
    )
    registry.register(
        ToolDefinition(
            name='create_folder',
            description='Create a new folder at the specified path.',
            parameters={
                'type': 'object',
                'properties': {'path': {'type': 'string'}},
                'required': ['path'],
            },
            risk_tier=RiskTier.T2,
            handler=filesystem.create_folder,
        )
    )
    registry.register(
        ToolDefinition(
            name='move_file',
            description='Move a file from source to destination.',
            parameters={
                'type': 'object',
                'properties': {
                    'source': {'type': 'string'},
                    'destination': {'type': 'string'},
                },
                'required': ['source', 'destination'],
            },
            risk_tier=RiskTier.T3,
            handler=filesystem.move_file,
        )
    )
    registry.register(
        ToolDefinition(
            name='open_application',
            description='Open an application by name or path.',
            parameters={
                'type': 'object',
                'properties': {'target': {'type': 'string'}},
                'required': ['target'],
            },
            risk_tier=RiskTier.T1,
            handler=applications.open_application,
        )
    )
    registry.register(
        ToolDefinition(
            name='focus_application',
            description='Focus an already-running application window.',
            parameters={
                'type': 'object',
                'properties': {'target': {'type': 'string'}},
                'required': ['target'],
            },
            risk_tier=RiskTier.T1,
            handler=applications.focus_application,
        )
    )
    registry.register(
        ToolDefinition(
            name='clipboard_read',
            description='Read the current clipboard contents.',
            parameters={'type': 'object', 'properties': {}},
            risk_tier=RiskTier.T1,
            handler=clipboard.read_clipboard,
        )
    )
    registry.register(
        ToolDefinition(
            name='clipboard_write',
            description='Write text to the clipboard.',
            parameters={
                'type': 'object',
                'properties': {'text': {'type': 'string'}},
                'required': ['text'],
            },
            risk_tier=RiskTier.T2,
            handler=clipboard.write_clipboard,
        )
    )
    registry.register(
        ToolDefinition(
            name='terminal_execute',
            description='Execute a safe terminal command in a sandboxed environment.',
            parameters={
                'type': 'object',
                'properties': {'command': {'type': 'string'}},
                'required': ['command'],
            },
            risk_tier=RiskTier.T4,
            handler=terminal.execute_command,
        )
    )

    return registry

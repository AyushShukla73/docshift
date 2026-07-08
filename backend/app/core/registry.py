"""
Backend tool registry. Mirrors the frontend registry concept so the two
sides can stay in sync with a shared vocabulary of tool ids.

To add a new tool:
  1. Create a handler in app/services/tools/<tool_id>.py
  2. Register it here via register_tool(...)
"""
from typing import Any, Callable, Dict, List, Optional

from app.models.tool import ToolDefinition


ToolHandler = Callable[[Dict[str, Any]], Dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}
        self._handlers: Dict[str, ToolHandler] = {}

    def register(
        self,
        tool_id: str,
        label: str,
        supported_inputs: List[str],
        output_type: str,
        handler: ToolHandler,
        multi_file: bool = False,
        configurable: bool = False,
    ) -> None:
        self._tools[tool_id] = ToolDefinition(
            id=tool_id,
            label=label,
            supported_inputs=supported_inputs,
            output_type=output_type,
            multi_file=multi_file,
            configurable=configurable,
        )
        self._handlers[tool_id] = handler

    def list_tools(self) -> List[ToolDefinition]:
        return list(self._tools.values())

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def get_handler(self, tool_id: str) -> Optional[ToolHandler]:
        return self._handlers.get(tool_id)

    def supports(self, tool_id: str, input_type: str) -> bool:
        tool = self.get(tool_id)
        if not tool:
            return False
        return input_type in tool.supported_inputs


tool_registry = ToolRegistry()
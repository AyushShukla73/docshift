"""
Exception hierarchy for tool execution.
"""

class ToolExecutionError(Exception):
    """Base class for all tool‑related errors.
    Subclasses may set ``error_code`` and ``details``.
    """
    error_code: str = "tool_execution_error"
    details: dict | None = None

    def __init__(self, message: str, *, code: str | None = None, details: dict | None = None):
        super().__init__(message)
        if code:
            self.error_code = code
        self.details = details


class ToolValidationError(ToolExecutionError):
    error_code = "validation_error"


class ToolProcessingError(ToolExecutionError):
    error_code = "processing_error"


class ToolDependencyError(ToolExecutionError):
    error_code = "dependency_error"

"""Preview generation utilities (stub).

Current implementation provides a placeholder that can be extended by individual tool
handlers to attach preview data (e.g., text snippets, image URLs, etc.) to the job
output. The function returns ``None`` by default, preserving backward compatibility.
"""

from typing import Any, Dict, Optional


def generate_preview(result: Dict[str, Any], tool_id: str) -> Optional[Dict[str, Any]]:
    """Generate a preview payload for a tool result.

    * ``result`` – the raw result dict returned by a tool handler.
    * ``tool_id`` – identifier of the tool that produced the result.

    For now we provide a simple placeholder preview for the ``pdf_to_word``
    tool. Other tools can extend this function later.
    """
    # Simple preview for pdf_to_word placeholder
    if tool_id == "pdf_to_word":
        return {"type": "text", "data": "PDF to Word conversion placeholder – generated .docx file."}
    # Placeholder: no preview generated for other tools.
    return None

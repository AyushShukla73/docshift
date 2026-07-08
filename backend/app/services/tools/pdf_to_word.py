from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="pdf_to_word",
        label="PDF to Word",
        supported_inputs=["pdf"],
        output_type="docx",
        multi_file=False,
        configurable=False,
        handler=stub_handler("converted.docx"),
    )
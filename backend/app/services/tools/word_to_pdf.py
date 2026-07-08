from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="word_to_pdf",
        label="Word to PDF",
        supported_inputs=["docx", "doc"],
        output_type="pdf",
        multi_file=False,
        configurable=False,
        handler=stub_handler("converted.pdf"),
    )
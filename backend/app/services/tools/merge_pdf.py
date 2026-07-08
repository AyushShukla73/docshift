from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="merge_pdf",
        label="Merge PDFs",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=True,
        configurable=False,
        handler=stub_handler("merged.pdf"),
    )
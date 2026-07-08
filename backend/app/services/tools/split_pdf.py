from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="split_pdf",
        label="Split PDF",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=stub_handler("split_archive.zip"),
    )
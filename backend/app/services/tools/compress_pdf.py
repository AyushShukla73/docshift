from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="compress_pdf",
        label="Compress PDF",
        description="Reduce PDF file size while preserving quality.",
        category="optimize",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=stub_handler("compressed.pdf"),
    )
from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="pdf_to_image",
        label="PDF to Image",
        supported_inputs=["pdf"],
        output_type="zip",
        multi_file=False,
        configurable=True,
        handler=stub_handler("pages.zip"),
    )
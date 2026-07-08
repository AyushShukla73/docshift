from app.core.registry import tool_registry
from app.services.tools.base import stub_handler


def register() -> None:
    tool_registry.register(
        tool_id="image_to_pdf",
        label="Image to PDF",
        supported_inputs=["jpg", "jpeg", "png", "webp"],
        output_type="pdf",
        multi_file=True,
        configurable=False,
        handler=stub_handler("images.pdf"),
    )
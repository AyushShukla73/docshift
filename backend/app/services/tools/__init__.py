from app.core.registry import tool_registry
from app.services.tools import (
    pdf_to_word,
    word_to_pdf,
    merge_pdf,
    split_pdf,
    compress_pdf,
    image_to_pdf,
    pdf_to_image,
    extract_text_from_pdf,
    protect_pdf,
    unlock_pdf,
)


def register_all_tools() -> None:
    """Register every tool module. Add new modules here."""
    pdf_to_word.register()
    word_to_pdf.register()
    merge_pdf.register()
    split_pdf.register()
    compress_pdf.register()
    image_to_pdf.register()
    pdf_to_image.register()
    extract_text_from_pdf.register()
    protect_pdf.register()
    unlock_pdf.register()
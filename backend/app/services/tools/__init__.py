from app.core.registry import tool_registry
import importlib
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
    ocr_extract_text,
)

# Ensure the latest version of the pdf_to_word module is loaded (helps when the file is edited during a live session).
importlib.reload(pdf_to_word)


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
    ocr_extract_text.register()
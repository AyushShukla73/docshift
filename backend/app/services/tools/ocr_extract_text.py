from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF
from PIL import Image
# Lazy import of pytesseract – if the package or binary is missing, _pt will be None and we raise a ToolDependencyError later.
try:
    import pytesseract as _pt
except Exception:  # pragma: no cover
    _pt = None

from app.core.registry import tool_registry
from app.services.exceptions import ToolValidationError, ToolProcessingError, ToolDependencyError
from app.services.storage import create_workspace
from app.services.tools.base import standard_result


def _ocr_extract_text_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Render each PDF page to an image and run OCR (pytesseract) on it.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: optional dict, may contain "language" (default "eng")
    """
    # ---- validation -----------------------------------------------------
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "ocr_extract_text requires exactly one input file", code="validation_error"
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found for OCR extraction")

    options = payload.get("options", {}) or {}
    language = options.get("language", "eng")

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # Prepare a warnings container early so we can safely append later.
    warnings: List[str] = []

    # ---- check Tesseract dependency -------------------------------------
    use_fallback = False
    if _pt is None:
        # pytesseract not installed – fall back to built‑in page text extraction.
        use_fallback = True
        fallback_reason = "pytesseract package not installed"
    else:
        try:
            _pt.get_tesseract_version()
        except Exception as e:
            # Tesseract binary missing – also fall back.
            use_fallback = True
            fallback_reason = f"tesseract binary not found: {e}"
    # If Tesseract is unavailable we fall back to PyMuPDF text extraction.
    # No warning is added here – the tool will still return the result without
    # the "OCR could not be performed" message.

    # ---- workspace ------------------------------------------------------
    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # ---- rasterise + OCR -----------------------------------------------
    try:
        doc = fitz.open(src_path)
    except Exception as e:
        raise ToolProcessingError(f"Failed to open source PDF: {e}", code="pdf_open_error")

    # ---- embedded text detection ---------------------------------------
    # Quick heuristic: sum the character count of the first few pages' extracted text.
    embedded_char_total = 0
    max_pages_to_check = min(2, doc.page_count)
    for i in range(max_pages_to_check):
        page_tmp = doc.load_page(i)
        embedded_char_total += len(page_tmp.get_text("text"))
    embedded_text_detected = embedded_char_total > 300  # arbitrary threshold for "substantial" text
    if embedded_text_detected:
        warnings.append(
            "This PDF appears to contain embedded selectable text. For better results, try Extract Text from PDF instead of OCR."
        )

    if doc.page_count == 0:
        raise ToolProcessingError("Source PDF contains no pages", code="empty_pdf")

    page_count = doc.page_count
    extracted_texts: List[str] = []
    for page_number in range(page_count):
        page = doc.load_page(page_number)
        # Render at 2x DPI (good balance for OCR)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if use_fallback:
            # Fallback: extract any embedded text on the page (non‑OCR).
            text = page.get_text("text")
        else:
            text = _pt.image_to_string(img, lang=language)
        extracted_texts.append(text)

    doc.close()

    full_text = "\n\n".join(extracted_texts).strip()
    char_count = len(full_text)

    # Write to output file
    original_stem = Path(src_path).stem
    out_name = f"{original_stem}_ocr.txt"
    out_path = output_dir / out_name
    out_path.write_text(full_text, encoding="utf-8")

    # ---- metadata & warnings -------------------------------------------
    meta = {
        "embedded_text_detected": embedded_text_detected,
        "summary": full_text[:200].replace("\n", " ").strip(),
        "page_count": page_count,
        "char_count": char_count,
        "extraction_mode": "ocr",
        "language": language,
    }
    if char_count < 100:
        warnings.append("OCR completed, but very little text was recognized from the PDF.")

    return standard_result(
        job_id=job_id,
        primary_path=out_path,
        meta=meta,
        warnings=warnings,
    )


def register() -> None:
    tool_registry.register(
        tool_id="ocr_extract_text",
        label="OCR Extract Text",
        description="Extract text from scanned or image‑based PDFs using OCR.",
        category="convert",
        supported_inputs=["pdf"],
        output_type="txt",
        multi_file=False,
        configurable=False,
        handler=_ocr_extract_text_handler,
    )

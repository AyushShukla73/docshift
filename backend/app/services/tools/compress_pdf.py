from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

from app.core.registry import tool_registry
from app.services.exceptions import ToolValidationError, ToolProcessingError
from app.services.storage import create_workspace
from app.services.tools.base import standard_result


def _compress_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Rasterise each page of the source PDF and rebuild a new PDF at a selected quality level.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: dict with required key "level" ("low", "medium", "high")
    """
    # ---- validation -----------------------------------------------------
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "compress_pdf requires exactly one input file", code="validation_error"
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found for compression")

    options = payload.get("options", {}) or {}
    level = options.get("level") or "medium"
    if level not in {"low", "medium", "high"}:
        raise ToolValidationError(
            "compress_pdf requires a compression level of 'low', 'medium', or 'high'",
            code="validation_error",
        )

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # ---- map level to rendering parameters ------------------------------
    # These values were chosen to give a sensible trade‑off between file size and visual fidelity.
    level_settings = {
        "low": {"zoom": 2.0, "jpeg_quality": 95},      # ~144 dpi, high quality
        "medium": {"zoom": 1.5, "jpeg_quality": 85},   # ~108 dpi, balanced
        "high": {"zoom": 1.0, "jpeg_quality": 70},    # ~72 dpi, aggressive compression
    }
    zoom = level_settings[level]["zoom"]
    jpeg_quality = level_settings[level]["jpeg_quality"]

    # ---- workspace ------------------------------------------------------
    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # ---- rasterise and rebuild -----------------------------------------
    try:
        src_doc = fitz.open(src_path)
    except Exception as e:
        raise ToolProcessingError(f"Failed to open source PDF: {e}", code="pdf_open_error")

    if src_doc.page_count == 0:
        raise ToolProcessingError("Source PDF contains no pages", code="empty_pdf")

    page_count = src_doc.page_count  # capture before we start processing / before closing

    out_doc = fitz.open()  # will hold the compressed pages

    for page_number in range(page_count):
        page = src_doc.load_page(page_number)
        # Render page to pixmap at the chosen zoom (scale).
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        # Convert pixmap to JPEG in memory.
        img_bytes = BytesIO()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(img_bytes, format="JPEG", quality=jpeg_quality, optimize=True)
        img_bytes.seek(0)
        # Insert the image into a fresh page.
        rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = out_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes.read())

    # Determine output filename – original stem + _compressed.pdf
    original_stem = Path(src_path).stem
    out_name = f"{original_stem}_compressed.pdf"
    out_path = output_dir / out_name
    out_doc.save(str(out_path))
    out_doc.close()
    src_doc.close()

    # ---- build result ---------------------------------------------------
    meta = {
        "summary": f"Compressed PDF ({level} level)",
        "compression_level": level,
        "page_count": page_count,
    }
    warnings = [
        "Compressed PDF was rebuilt from rendered page images; text selection/search may be affected."
    ]
    return standard_result(
        job_id=job_id,
        primary_path=out_path,
        meta=meta,
        warnings=warnings,
    )


def register() -> None:
    tool_registry.register(
        tool_id="compress_pdf",
        label="Compress PDF",
        description="Reduce PDF file size by rebuilding it at a lower image quality level.",
        category="optimize",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=_compress_pdf_handler,
    )
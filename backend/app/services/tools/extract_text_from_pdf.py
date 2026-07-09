from typing import Any, Dict, List
from pathlib import Path
import os

import fitz  # PyMuPDF

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace
from app.services.exceptions import ToolValidationError


def _extract_text_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract embedded digital text from a PDF and write it to a .txt file.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: dict (not used for v1)
    """
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "extract_text_from_pdf requires exactly one input file",
            code="validation_error",
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found for text extraction")

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # Prepare workspace
    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # Open PDF and extract text using layout‑aware blocks for better reading order
    doc = fitz.open(src_path)
    page_count = len(doc)
    if page_count == 0:
        raise ValueError("PDF contains no pages")
    block_texts: List[str] = []
    for page in doc:
        # Get raw blocks: each block is a tuple (x0, y0, x1, y1, "text", block_no, block_type)
        raw_blocks = page.get_text("blocks")
        # Filter out empty/whitespace blocks and keep (y0, x0, text)
        filtered = []
        for blk in raw_blocks:
            # blk[4] holds the text for the block
            txt = blk[4]
            if txt and txt.strip():
                filtered.append((blk[1], blk[0], txt))  # (y0, x0, text)
        # Sort blocks top‑to‑bottom, then left‑to‑right
        for _, _, txt in sorted(filtered, key=lambda b: (b[0], b[1])):
            # Strip trailing whitespace but keep internal newlines as produced by the block
            block_texts.append(txt.strip())
    # Join blocks with a blank line between them; also separate pages with an extra newline
    full_text = "\n\n".join(block_texts)
    char_count = len(full_text)

    # Write extracted text to a .txt file in the outputs folder
    txt_path = output_dir / "extracted_text.txt"
    txt_path.write_text(full_text, encoding="utf-8")

    # Build metadata and warnings
    warnings: List[str] = []
    if char_count < 100:
        warnings.append(
            "Very little extractable text was found. This PDF may require OCR."
        )
    meta = {
        "summary": full_text[:200].replace("\n", " ").strip(),
        "page_count": page_count,
        "char_count": char_count,
        "extraction_mode": "digital_text",
        "layout_mode": "block_sorted",
    }

    return standard_result(
        job_id=job_id,
        primary_path=txt_path,
        meta=meta,
        warnings=warnings,
    )


def register() -> None:
    tool_registry.register(
        tool_id="extract_text_from_pdf",
        label="Extract Text from PDF",
        description="Extracts embedded text from a PDF into a plain text file.",
        category="convert",
        supported_inputs=["pdf"],
        output_type="txt",
        multi_file=False,
        configurable=False,
        handler=_extract_text_handler,
    )

from typing import Any, Dict, List
import os
import shutil
import zipfile
from pathlib import Path

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace


def _pdf_to_image_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Render each page of a PDF to images (PNG or JPG) and return a zip archive.

    Options (payload["options"]) may include:
        - format: "png" (default) or "jpg"
    """
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No PDF input provided")
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found")
    img_format = payload.get("options", {}).get("format", "png").lower()
    if img_format == "jpeg":
        img_format = "jpg"
    if img_format not in {"png", "jpg"}:
        raise ValueError("Unsupported image format for PDF to Image")
    job_id = payload.get("job_id")
    if not job_id:
        raise ValueError("Missing job_id in payload")

    ws = create_workspace(job_id)
    temp_dir = ws["temp"]
    output_dir = ws["outputs"]

    # Render each page to an image file
    import fitz  # PyMuPDF
    doc = fitz.open(src_path)
    if len(doc) == 0:
        raise ValueError("PDF contains no pages")
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img_path = temp_dir / f"page_{i}.{img_format}"
        if img_format == "png":
            pix.save(str(img_path))
        else:
            # Convert to JPEG via Pillow
            from PIL import Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(str(img_path), format="JPEG", quality=95)
    # Create zip archive of images
    zip_name = f"pages.{img_format}.zip"
    zip_path = temp_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for img_file in temp_dir.iterdir():
            if img_file.is_file() and img_file.suffix.lstrip('.') == img_format:
                zipf.write(str(img_file), arcname=img_file.name)
    final_path = output_dir / zip_name
    zip_path.replace(final_path)
    # Clean up temp images
    shutil.rmtree(temp_dir, ignore_errors=True)
    # Return standardized result
    return standard_result(
        job_id=job_id,
        primary_path=final_path,
        meta={"format": img_format, "page_count": len(doc)},
        warnings=[],
    )


def register() -> None:
    tool_registry.register(
        tool_id="pdf_to_image",
        label="PDF to Image",
        description="Render each PDF page as an image (PNG or JPG) and bundle them in a zip.",
        category="convert",
        supported_inputs=["pdf"],
        output_type="zip",
        multi_file=False,
        configurable=True,
        handler=_pdf_to_image_handler,
    )

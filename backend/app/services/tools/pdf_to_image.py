import os
import shutil
import tempfile
import zipfile
from typing import Any, Dict, List

import fitz  # PyMuPDF

from app.core.registry import tool_registry


def _pdf_to_image_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Render each page of a PDF to an image (PNG or JPG) and return a zip archive.

    Options expected in payload["options"]:
        - format: "png" or "jpg" (default "png")
    """
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No PDF input provided")

    src_path = inputs[0].get("temp_path")
    if not src_path or not os.path.exists(src_path):
        raise FileNotFoundError("Source PDF not found")

    img_format = payload.get("options", {}).get("format", "png").lower()
    if img_format == "jpeg":
        img_format = "jpg"
    if img_format not in {"png", "jpg"}:
        raise ValueError("Unsupported image format for PDF to Image")

    job_id = payload.get("job_id")
    if not job_id:
        raise ValueError("Missing job_id in payload")

    temp_dir = tempfile.mkdtemp(prefix="pdf2img_")
    image_paths: List[str] = []

    try:
        doc = fitz.open(src_path)

        if len(doc) == 0:
            raise ValueError("PDF contains no pages")

        # Render each page at 2x resolution for decent quality
        matrix = fitz.Matrix(2, 2)

        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img_path = os.path.join(temp_dir, f"page_{i}.{img_format}")

            if img_format == "png":
                pix.save(img_path)
            else:
                # Convert pixmap to JPEG via Pillow
                from PIL import Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(img_path, format="JPEG", quality=95)

            image_paths.append(img_path)

        if not image_paths:
            raise ValueError("No images were generated from the PDF")

        zip_filename = f"pages.{img_format}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for path in image_paths:
                zipf.write(path, arcname=os.path.basename(path))

        size = os.path.getsize(zip_path)

        # Persist zip for download
        out_dir = os.path.join(os.getcwd(), "outputs", job_id)
        os.makedirs(out_dir, exist_ok=True)
        dest_path = os.path.join(out_dir, zip_filename)
        shutil.move(zip_path, dest_path)

        return {
            "output": {
                "filename": os.path.basename(dest_path),
                "download_url": f"/api/jobs/{job_id}/download",
                "size_bytes": size,
                "mime_type": "application/zip",
            }
        }
    finally:
        # Clean up temporary images
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass


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

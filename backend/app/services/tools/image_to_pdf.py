from typing import Any, Dict, List
import os
import tempfile

from PIL import Image

from app.core.registry import tool_registry
from app.services.tools.base import mock_output


def _image_to_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Combine uploaded images into a single PDF.

    Supported image formats are those Pillow can open. The images are taken in the order they appear in ``payload['inputs']``.
    """
    input_paths: List[str] = []
    for inp in payload.get("inputs", []):
        p = inp.get("temp_path")
        if p and os.path.exists(p):
            input_paths.append(p)
    if not input_paths:
        raise ValueError("No image inputs provided")

    images = [Image.open(p).convert("RGB") for p in input_paths]
    temp_dir = tempfile.mkdtemp(prefix="img2pdf_")
    out_path = os.path.join(temp_dir, "merged.pdf")
    # Save first image and append others
    images[0].save(out_path, save_all=True, append_images=images[1:])
    size = os.path.getsize(out_path)
    # Persist output PDF
    import shutil
    job_id = payload.get("job_id")
    out_dir = os.path.join(os.getcwd(), "outputs", job_id)
    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, "merged.pdf")
    shutil.move(out_path, dest_path)
    return {
        "output": {
            "filename": "merged.pdf",
            "download_url": f"/api/jobs/{job_id}/download",
            "size_bytes": size,
        }
    }


def register() -> None:
    tool_registry.register(
        tool_id="image_to_pdf",
        label="Image to PDF",
        description="Combine one or more images into a single PDF document.",
        category="convert",
        supported_inputs=["jpg", "jpeg", "png", "webp"],
        output_type="pdf",
        multi_file=True,
        configurable=False,
        handler=_image_to_pdf_handler,
    )
from typing import Any, Dict, List
from pathlib import Path
import os
import tempfile
from PIL import Image

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace


def _image_to_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Combine uploaded images into a single PDF."""
    job_id = payload["job_id"]
    ws = create_workspace(job_id)
    input_paths: List[Path] = []
    for inp in payload.get("inputs", []):
        p = inp.get("temp_path")
        if p and Path(p).exists():
            input_paths.append(Path(p))
    if not input_paths:
        raise ValueError("No image inputs provided")
    images = [Image.open(str(p)).convert("RGB") for p in input_paths]
    out_path = ws["temp"] / "merged.pdf"
    images[0].save(str(out_path), save_all=True, append_images=images[1:])
    final_path = ws["outputs"] / "merged.pdf"
    out_path.replace(final_path)
    return standard_result(
        job_id=job_id,
        primary_path=final_path,
        meta={"image_count": len(input_paths)},
    )


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

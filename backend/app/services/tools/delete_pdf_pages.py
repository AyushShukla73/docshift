from typing import Any, Dict, List
import shutil
from pathlib import Path
from app.services.storage import create_workspace
from app.services.tools.base import standard_result
from PyPDF2 import PdfReader, PdfWriter
from app.core.registry import tool_registry

def _delete_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No input PDF provided")
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found")
    options = payload.get("options", {}) or {}
    selected_pages = options.get("selected_pages") or []
    if not selected_pages:
        raise ValueError("No pages selected for deletion")
    selected_set = set(int(p) for p in selected_pages)
    reader = PdfReader(src_path)
    total_pages = len(reader.pages)
    if any(p < 1 or p > total_pages for p in selected_set):
        raise ValueError("Selected page out of bounds")
    remaining = [i for i in range(1, total_pages + 1) if i not in selected_set]
    if not remaining:
        raise ValueError("At least one page must remain after deletion")
    writer = PdfWriter()
    for pi in remaining:
        writer.add_page(reader.pages[pi - 1])
    job_id = payload.get("job_id")
    if not job_id:
        raise ValueError("Missing job_id in payload")
    ws = create_workspace(job_id)
    temp_dir = ws["temp"]
    out_path = temp_dir / "deleted_pages.pdf"
    with open(out_path, "wb") as f:
        writer.write(f)
    final_path = ws["outputs"] / out_path.name
    out_path.replace(final_path)
    return standard_result(
        job_id=job_id,
        primary_path=final_path,
        meta={"action": "delete_pages", "removed": list(selected_set)},
        warnings=[],
    )

def register() -> None:
    tool_registry.register(
        tool_id="delete_pdf_pages",
        label="Delete PDF Pages",
        description="Remove selected pages from a PDF document.",
        category="organize",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=_delete_handler,
    )

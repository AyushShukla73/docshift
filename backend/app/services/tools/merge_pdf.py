from typing import Any, Dict, List
import os
import tempfile

from PyPDF2 import PdfMerger

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace
from pathlib import Path


def _merge_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple PDF inputs into a single PDF.

    The handler expects each input dict to contain a ``temp_path`` pointing to the uploaded file on disk.
    It uses the per‑job workspace (jobs/<job_id>/…) and returns a unified result via ``standard_result``.
    """
    job_id = payload["job_id"]
    # Build deterministic workspace for this job
    ws = create_workspace(job_id)
    temp_dir = ws["temp"]
    merger = PdfMerger()
    for inp in payload.get("inputs", []):
        temp_path = inp.get("temp_path")
        if temp_path and Path(temp_path).exists():
            merger.append(temp_path)
    output_path = temp_dir / "merged.pdf"
    merger.write(str(output_path))
    merger.close()
    # Move final artifact to the outputs folder
    final_path = ws["outputs"] / "merged.pdf"
    output_path.replace(final_path)
    # Return the standardized contract
    return standard_result(
        job_id=job_id,
        primary_path=final_path,
        meta={"tool": "merge_pdf"},
    )


def register() -> None:
    tool_registry.register(
        tool_id="merge_pdf",
        label="Merge PDFs",
        description="Combine multiple PDFs into a single document.",
        category="organize",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=True,
        configurable=False,
        handler=_merge_handler,
    )
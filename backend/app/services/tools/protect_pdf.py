from typing import Any, Dict, List
from pathlib import Path
import os

from PyPDF2 import PdfReader, PdfWriter

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace
from app.services.exceptions import ToolValidationError


def _protect_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt a PDF with a user‑provided password.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: dict that must contain a non‑empty "password" entry
    """
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "protect_pdf requires exactly one input file",
            code="validation_error",
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found for protection")

    # Validate password option
    options = payload.get("options", {}) or {}
    password = options.get("password")
    if password is None or not isinstance(password, str) or not password.strip():
        raise ToolValidationError(
            "protect_pdf requires a non‑empty password option",
            code="validation_error",
        )
    password = password.strip()

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # Prepare workspace
    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # Read source PDF and write encrypted version
    reader = PdfReader(src_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(user_password=password)

    # Determine output filename – keep original stem + _protected.pdf
    original_name = Path(src_path).stem
    out_name = f"{original_name}_protected.pdf"
    out_path = output_dir / out_name
    with open(out_path, "wb") as out_file:
        writer.write(out_file)

    # Build metadata
    meta = {
        "summary": f"PDF encrypted with password protection (output: {out_name})",
        "encryption_applied": True,
    }

    return standard_result(
        job_id=job_id,
        primary_path=out_path,
        meta=meta,
        warnings=[],
    )


def register() -> None:
    tool_registry.register(
        tool_id="protect_pdf",
        label="Protect PDF",
        description="Encrypt a PDF with a password so it requires the password to open.",
        category="secure",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=_protect_pdf_handler,
    )

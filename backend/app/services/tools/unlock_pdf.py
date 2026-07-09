from typing import Any, Dict, List
from pathlib import Path
import os

from PyPDF2 import PdfReader, PdfWriter

from app.core.registry import tool_registry
from app.services.tools.base import standard_result
from app.services.storage import create_workspace
from app.services.exceptions import ToolValidationError, ToolProcessingError


def _unlock_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Remove password protection from a PDF using the provided password.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: dict that must contain a non‑empty "password"
    """
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "unlock_pdf requires exactly one input file",
            code="validation_error",
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found for unlocking")

    # Validate password option
    options = payload.get("options", {}) or {}
    password = options.get("password")
    if password is None or not isinstance(password, str) or not password.strip():
        raise ToolValidationError(
            "unlock_pdf requires a non‑empty password option",
            code="validation_error",
        )
    password = password.strip()

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # Prepare workspace
    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # Open source PDF and verify encryption
    reader = PdfReader(src_path)
    if not reader.is_encrypted:
        raise ToolProcessingError(
            "This PDF is not password‑protected",
            code="pdf_not_encrypted",
        )
    # Attempt to decrypt
    try:
        decrypt_result = reader.decrypt(password)
    except Exception as e:
        # PyPDF2 may raise if password type is wrong
        raise ToolProcessingError(
            f"Failed to decrypt PDF: {e}",
            code="invalid_pdf_password",
        )
    if decrypt_result == 0:
        raise ToolProcessingError(
            "The provided password could not unlock this PDF",
            code="invalid_pdf_password",
        )

    # Copy pages to a new writer (unencrypted)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    # Determine output filename
    original_stem = Path(src_path).stem
    out_name = f"{original_stem}_unlocked.pdf"
    out_path = output_dir / out_name
    with open(out_path, "wb") as out_file:
        writer.write(out_file)

    # Build metadata
    meta = {
        "summary": f"PDF unlocked (output: {out_name})",
        "encryption_removed": True,
    }

    return standard_result(
        job_id=job_id,
        primary_path=out_path,
        meta=meta,
        warnings=[],
    )


def register() -> None:
    tool_registry.register(
        tool_id="unlock_pdf",
        label="Unlock PDF",
        description="Remove password protection from a PDF using the correct password.",
        category="optimize",
        supported_inputs=["pdf"],
        output_type="pdf",
        multi_file=False,
        configurable=True,
        handler=_unlock_pdf_handler,
    )

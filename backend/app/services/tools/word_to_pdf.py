from pathlib import Path
import subprocess
import shutil
from typing import Any, Dict, List

from app.core.registry import tool_registry
from app.services.exceptions import ToolValidationError, ToolProcessingError, ToolDependencyError
from app.services.storage import create_workspace
from app.services.tools.base import standard_result


def _word_to_pdf_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single DOCX file to PDF using LibreOffice headless mode.

    Expected payload keys:
        - job_id: str
        - inputs: list with a single dict containing "temp_path"
        - options: currently unused (reserved for future extensions)
    """
    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ToolValidationError(
            "word_to_pdf requires exactly one input file", code="validation_error"
        )
    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source DOCX not found for conversion")

    # Ensure the file is a DOCX – reject legacy .doc explicitly
    src_path_obj = Path(src_path)
    if src_path_obj.suffix.lower() == ".doc":
        raise ToolValidationError(
            "Legacy .doc files are not supported yet. Please upload a .docx file.",
            code="validation_error",
        )
    if src_path_obj.suffix.lower() != ".docx":
        raise ToolValidationError(
            f"Unsupported file type '{src_path_obj.suffix}'. Only .docx is allowed.",
            code="validation_error",
        )

    job_id = payload.get("job_id")
    if not job_id:
        raise ToolValidationError("Missing job_id in payload", code="validation_error")

    # LibreOffice binary may be called "libreoffice" or "soffice" depending on install.
    libreoffice_cmd = shutil.which("libreoffice") or shutil.which("soffice")
    # If not found on PATH, try the default Windows installation directories.
    if not libreoffice_cmd:
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files\LibreOffice\program\libreoffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\libreoffice.exe",
        ]
        for p in possible_paths:
            if Path(p).exists():
                libreoffice_cmd = str(p)
                break
    if not libreoffice_cmd:
        raise ToolDependencyError(
            "LibreOffice executable not found. Install LibreOffice and ensure its binary (libreoffice or soffice) is on your system PATH.",
            code="libreoffice_missing",
        )

    ws = create_workspace(job_id)
    output_dir = ws["outputs"]

    # Run LibreOffice in headless mode to convert DOCX -> PDF.
    try:
        result = subprocess.run(
            [
                libreoffice_cmd,
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(output_dir),
                str(src_path),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise ToolProcessingError(
            f"LibreOffice conversion failed: {e.stderr or e.stdout}",
            code="libreoffice_conversion_error",
        )

    # LibreOffice creates a PDF with the same stem as the DOCX.
    output_pdf_name = f"{src_path_obj.stem}.pdf"
    out_path = output_dir / output_pdf_name
    if not out_path.exists():
        raise ToolProcessingError(
            "Conversion succeeded but output PDF not found", code="output_missing"
        )

    meta = {
        "summary": f"Converted DOCX '{src_path_obj.name}' to PDF",
        "source_type": "docx",
        "conversion_engine": "libreoffice",
    }
    warnings: List[str] = []
    return standard_result(
        job_id=job_id,
        primary_path=out_path,
        meta=meta,
        warnings=warnings,
    )


def register() -> None:
    tool_registry.register(
        tool_id="word_to_pdf",
        label="Word to PDF",
        description="Convert a DOCX document into a PDF.",
        category="convert",
        supported_inputs=["docx"],
        output_type="pdf",
        multi_file=False,
        configurable=False,
        handler=_word_to_pdf_handler,
    )
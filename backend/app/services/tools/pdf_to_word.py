"""PDF → Word conversion using **pdf2docx**.

Creates a real DOCX file from the uploaded PDF. This replaces the previous placeholder
implementation. The conversion is performed with the `pdf2docx` library, which extracts
text, tables and simple formatting.
"""

from pathlib import Path
from app.core.registry import tool_registry
from app.services.storage import create_workspace
from app.services.tools.base import standard_result

# pdf2docx is added to the backend requirements (see backend/requirements.txt).
# Import guarded – missing optional dependency should not crash startup.
try:
    from pdf2docx import Converter  # type: ignore
except ImportError:  # pragma: no cover
    Converter = None  # Fallback placeholder – registration will be skipped.



def _pdf_to_word_handler(payload: dict) -> dict:
    """Convert a single PDF to DOCX.

    The payload must contain a single input with a temporary file path (``temp_path``).
    The generated DOCX is written to the job's output directory and returned via
    ``standard_result``.
    """
    # Ensure the optional pdf2docx library is available.
    if Converter is None:
        raise RuntimeError("pdf2docx library is not installed; PDF → DOCX conversion unavailable.")

    inputs = payload.get("inputs", [])
    if len(inputs) != 1:
        raise ValueError("pdf_to_word expects exactly one input file")
    src_path = inputs[0].get("temp_path")
    if not src_path:
        raise ValueError("Missing temp_path for input PDF")
    job_id = payload.get("job_id")
    if not job_id:
        raise ValueError("Missing job_id in payload")

    ws = create_workspace(job_id)
    out_dir: Path = ws["outputs"]
    output_path = out_dir / "converted.docx"

    # Perform conversion – pdf2docx writes directly to the output file.
    try:
        cv = Converter(src_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    except Exception as exc:
        # Wrap any library error so the dispatcher can surface it cleanly.
        raise RuntimeError(f"PDF→DOCX conversion failed: {exc}")

    meta = {"note": "Converted PDF to DOCX via pdf2docx."}
    return standard_result(job_id=job_id, primary_path=output_path, meta=meta)


def register() -> None:
    # Register the tool unconditionally. If the optional pdf2docx library is missing,
    # the handler will raise a clear error when invoked.
    tool_registry.register(
        tool_id="pdf_to_word",
        label="PDF to Word",
        description="Convert a PDF document into an editable DOCX file.",
        category="convert",
        supported_inputs=["pdf"],
        output_type="docx",
        multi_file=False,
        configurable=False,
        handler=_pdf_to_word_handler,
    )

from typing import Any, Dict, List
import os
import tempfile
import zipfile

from PyPDF2 import PdfReader, PdfWriter

from app.core.registry import tool_registry
from app.services.tools.base import mock_output


def _split_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Split a PDF according to options.

    Options expected in ``payload['options']``:
        - mode: one of "range", "each", "n"
        - range_start, range_end (for "range")
        - n_pages (for "n")
    Returns a zip archive containing resulting PDFs.
    """
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No input PDF provided")
    inp = inputs[0]
    src_path = inp.get("temp_path")
    if not src_path or not os.path.exists(src_path):
        raise FileNotFoundError("Source PDF not found")

    mode = payload.get("options", {}).get("mode", "each")
    reader = PdfReader(src_path)
    total_pages = len(reader.pages)

    temp_dir = tempfile.mkdtemp(prefix="split_pdf_")
    output_files: List[str] = []

    if mode == "range":
        start = int(payload["options"].get("range_start", 1)) - 1
        end = int(payload["options"].get("range_end", total_pages))
        writer = PdfWriter()
        for p in range(start, min(end, total_pages)):
            writer.add_page(reader.pages[p])
        out_path = os.path.join(temp_dir, "range.pdf")
        with open(out_path, "wb") as f:
            writer.write(f)
        output_files.append(out_path)
    elif mode == "each":
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            out_path = os.path.join(temp_dir, f"page_{i+1}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            output_files.append(out_path)
    elif mode == "n":
        n = int(payload["options"].get("n_pages", 2))
        for start in range(0, total_pages, n):
            writer = PdfWriter()
            for p in range(start, min(start + n, total_pages)):
                writer.add_page(reader.pages[p])
            out_path = os.path.join(temp_dir, f"pages_{start+1}_to_{min(start+n,total_pages)}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            output_files.append(out_path)
    else:
        raise ValueError(f"Unsupported split mode: {mode}")

    # Create zip archive
    zip_path = os.path.join(temp_dir, "split_results.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for fp in output_files:
            zipf.write(fp, os.path.basename(fp))
    size = os.path.getsize(zip_path)
    # Persist zip for download
    import shutil
    job_id = payload.get("job_id")
    out_dir = os.path.join(os.getcwd(), "outputs", job_id)
    os.makedirs(out_dir, exist_ok=True)
    dest_path = os.path.join(out_dir, "split_results.zip")
    shutil.move(zip_path, dest_path)
    return {
        "output": {
            "filename": "split_results.zip",
            "download_url": f"/api/jobs/{job_id}/download",
            "size_bytes": size,
        }
    }


def register() -> None:
    tool_registry.register(
        tool_id="split_pdf",
        label="Split PDF",
        description="Extract ranges or individual pages from a PDF.",
        category="organize",
        supported_inputs=["pdf"],
        output_type="zip",
        multi_file=False,
        configurable=True,
        handler=_split_handler,
    )
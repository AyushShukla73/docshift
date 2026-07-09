from typing import Any, Dict, List
import shutil
import zipfile
from pathlib import Path
from app.services.storage import create_workspace
from app.services.tools.base import standard_result

from PyPDF2 import PdfReader, PdfWriter

from app.core.registry import tool_registry


def _split_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Split a PDF according to options and return a unified result.

    All validation (range checks, mode handling) remains exactly as before, but the file handling now uses the per‑job
    workspace (``jobs/<job_id>/temp`` and ``jobs/<job_id>/outputs``) and the result is built via ``standard_result``.
    """
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No input PDF provided")

    src_path = inputs[0].get("temp_path")
    if not src_path or not Path(src_path).exists():
        raise FileNotFoundError("Source PDF not found")

    options = payload.get("options", {}) or {}
    raw_mode = str(options.get("mode", "each")).strip().lower()

    # Normalize mode values from frontend
    if raw_mode in {"range", "page_range", "page-range"}:
        mode = "range"
    elif raw_mode in {"each", "each_page", "each-page"}:
        mode = "each"
    elif raw_mode in {"n", "every_n", "every-n"}:
        mode = "n"
    else:
        raise ValueError(f"Unsupported split mode: {raw_mode}")

    reader = PdfReader(src_path)
    total_pages = len(reader.pages)
    if total_pages == 0:
        raise ValueError("The PDF contains no pages")

    job_id = payload.get("job_id")
    if not job_id:
        raise ValueError("Missing job_id in payload")

    ws = create_workspace(job_id)
    temp_dir = ws["temp"]
    output_paths: List[Path] = []

    try:
        if mode == "range":
            raw_start = options.get("start", options.get("range_start"))
            raw_end = options.get("end", options.get("range_end"))
            if raw_start is None or raw_end is None:
                raise ValueError("Invalid page range for split: missing start or end page")
            start_page = int(raw_start)
            end_page = int(raw_end)
            if start_page < 1 or end_page < 1:
                raise ValueError("Page numbers must be at least 1")
            if start_page > end_page:
                raise ValueError("Start page cannot be greater than end page")
            if end_page > total_pages:
                raise ValueError("Requested range exceeds PDF page count")
            writer = PdfWriter()
            for pi in range(start_page - 1, end_page):
                writer.add_page(reader.pages[pi])
            out_path = temp_dir / f"pages_{start_page}_to_{end_page}.pdf"
            with open(out_path, "wb") as f:
                writer.write(f)
            output_paths.append(out_path)

        elif mode == "each":
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])
                out_path = temp_dir / f"page_{i + 1}.pdf"
                with open(out_path, "wb") as f:
                    writer.write(f)
                output_paths.append(out_path)

        elif mode == "n":
            raw_n = options.get("n_pages", options.get("every_n"))
            if raw_n is None:
                raise ValueError("Split-by-N mode requires n_pages")
            n = int(raw_n)
            if n <= 0:
                raise ValueError("n_pages must be greater than 0")
            for start_idx in range(0, total_pages, n):
                writer = PdfWriter()
                end_idx = min(start_idx + n, total_pages)
                for pi in range(start_idx, end_idx):
                    writer.add_page(reader.pages[pi])
                out_path = temp_dir / f"pages_{start_idx + 1}_to_{end_idx}.pdf"
                with open(out_path, "wb") as f:
                    writer.write(f)
                output_paths.append(out_path)

        if not output_paths:
            raise ValueError("No split output files were generated")

        # Zip all generated PDFs
        zip_path = temp_dir / "split_results.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for p in output_paths:
                zipf.write(p, p.name)

        final_path = ws["outputs"] / zip_path.name
        zip_path.replace(final_path)

        return standard_result(
            job_id=job_id,
            primary_path=final_path,
            meta={"mode": mode, "output_count": len(output_paths)},
            warnings=[],
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


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
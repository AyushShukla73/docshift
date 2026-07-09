from typing import Any, Dict, List
import os
import shutil
import tempfile
import zipfile

from PyPDF2 import PdfReader, PdfWriter

from app.core.registry import tool_registry


def _split_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Split a PDF according to options.

    Accepted frontend/backend option variants:

    mode:
      - "range" or "page_range"
      - "each" or "each_page"
      - "n" or "every_n"

    range mode fields:
      - start / end
      - or range_start / range_end

    n mode fields:
      - n_pages
      - or every_n
    """
    inputs = payload.get("inputs", [])
    if not inputs:
        raise ValueError("No input PDF provided")

    src_path = inputs[0].get("temp_path")
    if not src_path or not os.path.exists(src_path):
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

    temp_dir = tempfile.mkdtemp(prefix="split_pdf_")
    output_files: List[str] = []

    try:
        if mode == "range":
            # Accept both naming conventions
            raw_start = options.get("start", options.get("range_start"))
            raw_end = options.get("end", options.get("range_end"))

            if raw_start is None or raw_end is None:
                raise ValueError(
                    "Invalid page range for split: missing start or end page"
                )

            try:
                start_page = int(raw_start)
                end_page = int(raw_end)
            except (TypeError, ValueError):
                raise ValueError(
                    "Invalid page range for split: start and end must be integers"
                )

            if start_page < 1 or end_page < 1:
                raise ValueError(
                    "Invalid page range for split: page numbers must be at least 1"
                )

            if start_page > end_page:
                raise ValueError(
                    f"Invalid page range for split: start page {start_page} "
                    f"cannot be greater than end page {end_page}"
                )

            if end_page > total_pages:
                raise ValueError(
                    f"Invalid page range for split: requested {start_page}-{end_page}, "
                    f"but the PDF only has {total_pages} pages"
                )

            writer = PdfWriter()
            # inclusive range
            for page_index in range(start_page - 1, end_page):
                writer.add_page(reader.pages[page_index])

            out_path = os.path.join(
                temp_dir, f"pages_{start_page}_to_{end_page}.pdf"
            )
            with open(out_path, "wb") as f:
                writer.write(f)

            output_files.append(out_path)

        elif mode == "each":
            for i in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                out_path = os.path.join(temp_dir, f"page_{i + 1}.pdf")
                with open(out_path, "wb") as f:
                    writer.write(f)

                output_files.append(out_path)

        elif mode == "n":
            raw_n = options.get("n_pages", options.get("every_n"))
            if raw_n is None:
                raise ValueError("Split-by-N mode requires n_pages")

            try:
                n = int(raw_n)
            except (TypeError, ValueError):
                raise ValueError("n_pages must be a valid integer")

            if n <= 0:
                raise ValueError("n_pages must be greater than 0")

            for start_idx in range(0, total_pages, n):
                writer = PdfWriter()
                end_idx = min(start_idx + n, total_pages)

                for page_index in range(start_idx, end_idx):
                    writer.add_page(reader.pages[page_index])

                out_path = os.path.join(
                    temp_dir,
                    f"pages_{start_idx + 1}_to_{end_idx}.pdf",
                )
                with open(out_path, "wb") as f:
                    writer.write(f)

                output_files.append(out_path)

        if not output_files:
            raise ValueError("No split output files were generated")

        zip_filename = "split_results.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for fp in output_files:
                zipf.write(fp, os.path.basename(fp))

        size = os.path.getsize(zip_path)

        out_dir = os.path.join(os.getcwd(), "outputs", job_id)
        os.makedirs(out_dir, exist_ok=True)

        dest_path = os.path.join(out_dir, zip_filename)
        shutil.move(zip_path, dest_path)

        return {
            "output": {
                "filename": zip_filename,
                "download_url": f"/api/jobs/{job_id}/download",
                "size_bytes": size,
                "mime_type": "application/zip",
            }
        }

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
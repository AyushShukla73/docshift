"""Helpers for building tool handlers.
Provides a ``standard_result`` helper that builds the unified result payload.
"""
import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional


def standard_result(
    job_id: str,
    primary_path: Path,
    *,
    extra_files: Optional[List[Path]] = None,
    meta: Optional[Dict[str, Any]] = None,
    warnings: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Construct the normalized output contract.

    * ``primary_path`` – the file that the UI should treat as the main result.
    * ``extra_files`` – any additional artifacts (will be listed in ``output_files``).
    * ``meta`` – tool‑specific free‑form metadata.
    * ``warnings`` – human‑readable warning messages.
    """

    def file_info(p: Path) -> Dict[str, Any]:
        return {
            "name": p.name,
            "path": str(p),
            "media_type": mimetypes.guess_type(p.name)[0] or "application/octet-stream",
            "size_bytes": p.stat().st_size,
        }

    primary_info = file_info(primary_path)
    all_files = [primary_info]
    if extra_files:
        all_files.extend([file_info(p) for p in extra_files])

    return {
        "output": {
            "success": True,
            "tool_id": None,  # filled by dispatcher
            "job_id": job_id,
            "primary_output_name": primary_info["name"],
            "primary_output_path": primary_info["path"],
            "primary_output_media_type": primary_info["media_type"],
            "output_files": all_files,
            "result_meta": meta or {},
            "warnings": warnings or [],
            # Backward‑compatible fields for the existing UI
            "filename": primary_info["name"],
            "download_url": f"/api/jobs/{job_id}/download",
            "size_bytes": primary_info["size_bytes"],
            "mime_type": primary_info["media_type"],
        }
    }

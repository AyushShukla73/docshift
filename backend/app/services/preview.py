"""Preview generation utilities (stub).

Current implementation provides a placeholder that can be extended by individual tool
handlers to attach preview data (e.g., text snippets, image URLs, etc.) to the job
output. The function returns ``None`` by default, preserving backward compatibility.
"""

from typing import Any, Dict, Optional


def generate_preview(result: Dict[str, Any], tool_id: str) -> Optional[Dict[str, Any]]:
    """Generate preview data for supported tools.

    * ``result`` – dict returned by the tool handler (contains an ``output`` key).
    * ``tool_id`` – ID of the tool that produced the result.
    Returns a ``dict`` with ``type`` and ``data`` or ``None`` when no preview is available.
    """
    import base64
    import zipfile
    import mimetypes
    from pathlib import Path

    output = result.get("output", {})
    # Helper to build text preview (truncated)
    def text_preview(path_str: str) -> Optional[Dict[str, Any]]:
        p = Path(path_str)
        if not p.is_file():
            return None
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None
        truncated = txt[:2000]
        if len(txt) > 2000:
            truncated += "\n... (truncated)"
        return {"type": "text", "data": truncated}

    # Text previews for extraction tools
    if tool_id in ("extract_text_from_pdf", "ocr_extract_text"):
        primary_path = output.get("primary_output_path")
        if primary_path:
            return text_preview(primary_path)
        return None

    # Image gallery preview for pdf_to_image (zip of images)
    if tool_id == "pdf_to_image":
        zip_path = output.get("primary_output_path")
        if not zip_path:
            return None
        p = Path(zip_path)
        if not p.is_file():
            return None
        try:
            with zipfile.ZipFile(p, "r") as z:
                images = []
                for name in z.namelist():
                    if len(images) >= 6:
                        break
                    if not name.lower().endswith((".png", ".jpg", ".jpeg")):
                        continue
                    data = z.read(name)
                    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
                    b64 = base64.b64encode(data).decode()
                    images.append(f"data:{mime};base64,{b64}")
                if images:
                    return {"type": "image_gallery", "data": images}
        except Exception:
            return None
        return None

    # Image preview for image_to_pdf – show source images (paths stored in meta)
    if tool_id == "image_to_pdf":
        meta = output.get("result_meta", {})
        preview_paths = meta.get("preview_images")
        if not preview_paths:
            return None
        images = []
        for path_str in preview_paths[:6]:
            p = Path(path_str)
            if not p.is_file():
                continue
            try:
                data = p.read_bytes()
                mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
                b64 = base64.b64encode(data).decode()
                images.append(f"data:{mime};base64,{b64}")
            except Exception:
                continue
        if images:
            return {"type": "image_gallery", "data": images}
        return None

    # No preview for other tools
    return None

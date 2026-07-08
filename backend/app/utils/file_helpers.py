from typing import Optional

EXT_MAP = {
    "pdf": "pdf",
    "docx": "docx",
    "doc": "doc",
    "jpg": "jpg",
    "jpeg": "jpg",
    "png": "png",
    "webp": "webp",
    "gif": "gif",
    "txt": "txt",
}

MIME_MAP = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/msword": "doc",
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/gif": "gif",
    "text/plain": "txt",
}


def detect_type(filename: str, content_type: Optional[str] = None) -> Optional[str]:
    """Return normalized internal type, e.g. 'pdf', 'docx', 'jpg'."""
    if filename and "." in filename:
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext in EXT_MAP:
            return EXT_MAP[ext]
    if content_type and content_type in MIME_MAP:
        return MIME_MAP[content_type]
    return None


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
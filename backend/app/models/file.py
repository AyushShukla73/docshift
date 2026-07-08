from typing import Optional
from pydantic import BaseModel


class FileMeta(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size_bytes: int
    detected_type: str  # normalized internal type, e.g. "pdf", "docx", "jpg"
    storage_path: Optional[str] = None
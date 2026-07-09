from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class JobInput(BaseModel):
    file_id: str
    filename: str
    detected_type: str
    size_bytes: int
    temp_path: str | None = None


class JobOutput(BaseModel):
    # Backward‑compatible fields (still used by UI)
    filename: Optional[str] = None
    download_url: Optional[str] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None

    # New normalized contract fields
    success: Optional[bool] = None
    tool_id: Optional[str] = None
    job_id: Optional[str] = None
    primary_output_name: Optional[str] = None
    primary_output_path: Optional[str] = None
    primary_output_media_type: Optional[str] = None
    output_files: Optional[List[Dict[str, Any]]] = None
    result_meta: Optional[Dict[str, Any]] = None
    warnings: Optional[List[str]] = None

class JobStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(BaseModel):
    job_id: str
    tool_id: str
    status: str = JobStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    inputs: List[JobInput] = []
    options: Dict[str, Any] = {}
    output: Optional[JobOutput] = None
    error: Optional[Union[str, dict]] = None
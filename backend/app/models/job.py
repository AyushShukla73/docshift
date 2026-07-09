from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class JobInput(BaseModel):
    file_id: str
    filename: str
    detected_type: str
    size_bytes: int
    temp_path: str | None = None


class JobOutput(BaseModel):
    filename: Optional[str] = None
    download_url: Optional[str] = None
    size_bytes: Optional[int] = None


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
    error: Optional[str] = None
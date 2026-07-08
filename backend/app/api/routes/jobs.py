from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.file import FileMeta
from app.models.job import Job, JobStatus
from app.services.dispatcher import dispatch
from app.services.storage import job_store
from app.utils.file_helpers import detect_type, human_size

router = APIRouter()


@router.post("/request", response_model=Job)
async def create_job(
    tool_id: str = Form(...),
    options: Optional[str] = Form(None),  # JSON string
    files: List[UploadFile] = File(...),
):
    """Create and synchronously execute a placeholder processing job."""
    import json

    parsed_options = {}
    if options:
        try:
            parsed_options = json.loads(options)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid options JSON")

    inputs = []
    for f in files:
        content = await f.read()
        detected = detect_type(f.filename or "", f.content_type)
        if detected is None:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type for {f.filename}",
            )
        inputs.append(
            {
                "file_id": f.filename or "file",
                "filename": f.filename or "file",
                "detected_type": detected,
                "size_bytes": len(content),
                "content_type": f.content_type,
            }
        )

    job = Job(
        job_id=f"job_{int(__import__('time').time() * 1000)}",
        tool_id=tool_id,
        status=JobStatus.PENDING,
        inputs=inputs,
        options=parsed_options,
    )

    job_store[job.job_id] = job
    job = await dispatch(job)
    job_store[job.job_id] = job
    return job


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/download")
async def download_result(job_id: str):
    job = job_store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != JobStatus.COMPLETED or not job.output:
        raise HTTPException(status_code=409, detail="Result not ready")
    # Placeholder: in the future, stream the actual file.
    return {
        "job_id": job.job_id,
        "filename": job.output.filename,
        "download_url": job.output.download_url,
        "note": "Placeholder download endpoint.",
    }
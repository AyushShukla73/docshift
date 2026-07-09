from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.file import FileMeta
from app.models.job import Job, JobStatus
from app.services.dispatcher import dispatch
from app.services.storage import job_store
from app.utils.file_helpers import detect_type, human_size
from app.core.registry import tool_registry

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
    import time
    from app.services.storage import create_workspace

    job_id = f"job_{int(time.time() * 1000)}"
    workspace = create_workspace(job_id)

    inputs = []
    for f in files:
        content = await f.read()
        detected = detect_type(f.filename or "", f.content_type)
        if detected is None:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type for {f.filename}",
            )
        safe_name = (f.filename or "file").replace("/", "_")
        input_path = workspace["inputs"] / safe_name
        with open(input_path, "wb") as tmp_file:
            tmp_file.write(content)
        inputs.append(
            {
                "file_id": f.filename or "file",
                "filename": f.filename or "file",
                "detected_type": detected,
                "size_bytes": len(content),
                "content_type": f.content_type,
                "temp_path": str(input_path),
            }
        )

    # Validate file count against tool definition
    tool_def = tool_registry.get(tool_id)
    if tool_def:
        if not tool_def.multi_file and len(inputs) != 1:
            raise HTTPException(status_code=400, detail=f"Tool '{tool_id}' expects exactly one input file")
        if tool_def.multi_file and len(inputs) < 1:
            raise HTTPException(status_code=400, detail=f"Tool '{tool_id}' requires at least one input file")
    job = Job(
        job_id=job_id,
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
    # Serve the actual file as attachment based on stored primary_output_path
    from fastapi.responses import FileResponse
    import os

    primary_path = job.output.primary_output_path if job.output and job.output.primary_output_path else None
    if not primary_path or not os.path.exists(primary_path):
        raise HTTPException(status_code=404, detail="Output file not found")
    # Determine mime type (basic guess based on extension)
    ext = os.path.splitext(job.output.filename or "")[1].lower()
    mime = {
        ".pdf": "application/pdf",
        ".zip": "application/zip",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }.get(ext, "application/octet-stream")
    return FileResponse(
        path=primary_path,
        media_type=mime,
        filename=job.output.filename,
    )
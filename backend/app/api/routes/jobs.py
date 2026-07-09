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
    for f in files:
        content = await f.read()
        detected = detect_type(f.filename or "", f.content_type)
        if detected is None:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type for {f.filename}",
            )
        # Write uploaded content to a temporary file so backend handlers can access it.
        import tempfile, os
        safe_name = (f.filename or "file").replace("/", "_")
        temp_path = os.path.join(tempfile.gettempdir(), f"job_{int(__import__('time').time()*1000)}_{safe_name}")
        with open(temp_path, "wb") as tmp_file:
            tmp_file.write(content)
        inputs.append(
            {
                "file_id": f.filename or "file",
                "filename": f.filename or "file",
                "detected_type": detected,
                "size_bytes": len(content),
                "content_type": f.content_type,
                "temp_path": temp_path,
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
    # Serve the actual file as attachment
    from fastapi import Response
    from fastapi.responses import FileResponse
    import os
    # Compute path based on job_id and stored filename
    output_dir = os.path.join(os.getcwd(), "outputs", job.job_id)
    file_path = os.path.join(output_dir, job.output.filename) if job.output and job.output.filename else None
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Output file not found")
    # Determine mime type (basic guess based on extension)
    ext = os.path.splitext(job.output.filename)[1].lower()
    mime = {
        ".pdf": "application/pdf",
        ".zip": "application/zip",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }.get(ext, "application/octet-stream")
    return FileResponse(
        path=file_path,
        media_type=mime,
        filename=job.output.filename,
    )
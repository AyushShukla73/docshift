"""
Generic processing dispatcher.

Receives a Job, validates the tool against the backend registry,
calls the registered handler, and returns an updated Job.
"""
import asyncio
from typing import Any, Dict

from app.core.registry import tool_registry
from app.models.job import Job, JobOutput, JobStatus
from app.services import preview as preview_service


async def dispatch(job: Job) -> Job:
    tool_def = tool_registry.get(job.tool_id)
    if tool_def is None:
        job.status = JobStatus.FAILED
        job.error = f"Unknown tool_id: {job.tool_id}"
        return job

    # Validate that every input is supported by the tool.
    for inp in job.inputs:
        if not tool_registry.supports(job.tool_id, inp.detected_type):
            job.status = JobStatus.FAILED
            job.error = (
                f"Tool '{job.tool_id}' does not accept input type "
                f"'{inp.detected_type}' (file: {inp.filename})"
            )
            return job

    handler = tool_registry.get_handler(job.tool_id)
    if handler is None:
        job.status = JobStatus.FAILED
        job.error = f"No handler registered for tool '{job.tool_id}'"
        return job

    job.status = JobStatus.PROCESSING
    try:
        # Handlers may be sync; run in executor to keep async surface clean.
        payload: Dict[str, Any] = {
            "job_id": job.job_id,
            "tool_id": job.tool_id,
            "inputs": [i.model_dump() for i in job.inputs],
            "options": job.options,
        }
        result = await asyncio.to_thread(handler, payload)
        job_output_data = result.get("output", {})
        job.output = JobOutput(**job_output_data)
        job.output.preview = preview_service.generate_preview(result, job.tool_id)
        # Ensure tool_id and job_id are populated in output contract
        if job.output.tool_id is None:
            job.output.tool_id = job.tool_id
        if job.output.job_id is None:
            job.output.job_id = job.job_id
        job.status = JobStatus.COMPLETED
    except Exception as exc:  # pragma: no cover - placeholder guard
        job.status = JobStatus.FAILED
        # Use structured error if available
        try:
            from app.services.exceptions import ToolExecutionError
        except Exception:
            ToolExecutionError = Exception
        if isinstance(exc, ToolExecutionError):
            job.error = {
                "message": str(exc),
                "code": getattr(exc, "error_code", "tool_execution_error"),
                "details": getattr(exc, "details", None),
            }
        else:
            job.error = {"message": str(exc), "code": "unknown_error"}


    from datetime import datetime
    job.updated_at = datetime.utcnow()
    return job
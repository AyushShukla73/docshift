"""
Generic processing dispatcher.

Receives a Job, validates the tool against the backend registry,
calls the registered handler, and returns an updated Job.
"""
import asyncio
from typing import Any, Dict

from app.core.registry import tool_registry
from app.models.job import Job, JobOutput, JobStatus


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
        job.output = JobOutput(**result.get("output", {}))
        job.status = JobStatus.COMPLETED
    except Exception as exc:  # pragma: no cover - placeholder guard
        job.status = JobStatus.FAILED
        job.error = f"Handler error: {exc!r}"

    from datetime import datetime
    job.updated_at = datetime.utcnow()
    return job
"""
In-memory job store. Swap for a DB/Redis later without touching routes.
Also provides workspace creation utilities for per‑job file handling.
"""
from typing import Dict
from pathlib import Path
import os
from app.models.job import Job

# Simple in‑memory store for Job objects.
job_store: Dict[str, Job] = {}


def create_workspace(job_id: str) -> Dict[str, Path]:
    """Create a deterministic per‑job workspace directory.

    Structure::
        <cwd>/jobs/<job_id>/
            inputs/   – original uploaded files
            temp/     – temporary processing files
            outputs/  – final artifacts for download
    """
    base = Path(os.getcwd()) / "jobs" / job_id
    inputs_dir = base / "inputs"
    temp_dir = base / "temp"
    outputs_dir = base / "outputs"
    for d in (inputs_dir, temp_dir, outputs_dir):
        d.mkdir(parents=True, exist_ok=True)
    return {"base": base, "inputs": inputs_dir, "temp": temp_dir, "outputs": outputs_dir}

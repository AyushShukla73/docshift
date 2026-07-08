"""In-memory job store. Swap for a DB/Redis later without touching routes."""
from typing import Dict
from app.models.job import Job

job_store: Dict[str, Job] = {}
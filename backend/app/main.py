from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, jobs
from app.core.config import settings
from app.core.registry import tool_registry

app = FastAPI(
    title="DocShift API",
    version="0.1.0",
    description="Foundational API for the DocShift document utility platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])


@app.on_event("startup")
async def startup_event() -> None:
    """Register all available tools at startup."""
    from app.services.tools import register_all_tools  # noqa: WPS433
    register_all_tools()
    print(f"[DocShift] Registered {len(tool_registry.list_tools())} tools.")


@app.get("/")
async def root():
    return {"name": "DocShift API", "version": "0.1.0", "docs": "/docs"}
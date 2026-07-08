"""Helpers for building placeholder tool handlers."""
from typing import Any, Dict


def mock_output(filename: str, size_bytes: int = 0) -> Dict[str, Any]:
    return {
        "output": {
            "filename": filename,
            "download_url": f"/api/jobs/mock/download/{filename}",
            "size_bytes": size_bytes,
        }
    }


def stub_handler(output_filename: str):
    """Return a placeholder handler that yields a mock success response."""

    def _handler(payload: Dict[str, Any]) -> Dict[str, Any]:
        # In the future: real conversion logic goes here.
        return mock_output(output_filename, size_bytes=1024)

    return _handler
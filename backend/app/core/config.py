from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DocShift"
    environment: str = "development"
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    upload_dir: str = "./_uploads"
    output_dir: str = "./_outputs"
    max_upload_mb: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
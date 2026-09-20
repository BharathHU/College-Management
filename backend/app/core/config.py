from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WORKSPACE_DIR = BASE_DIR.parent


class Settings(BaseSettings):
    app_name: str = "College Management System"
    database_url: str = Field(..., description="SQLAlchemy database URL; use mysql+pymysql for deployments")
    secret_key: str = Field(default="change-this-to-a-long-random-secret")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    frontend_url: str = Field(default="http://localhost:5173")
    backend_cors_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")

    model_config = SettingsConfigDict(
        env_file=[BASE_DIR / ".env", WORKSPACE_DIR / ".env"],
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

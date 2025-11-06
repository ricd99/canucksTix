from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    REDDIT_PASSWORD: str
    REDDIT_USER_AGENT: str
    REDDIT_USERNAME: str
    GEMINI_API_KEY: str

    API_PREFIX: str = "/api"
    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    class Config:
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

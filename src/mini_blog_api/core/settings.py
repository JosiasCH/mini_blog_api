# src/mini_blog_api/core/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    database_url: str = Field(..., alias="DATABASE_URL")

    @classmethod
    def from_env(cls) -> "Settings":
        test_url = os.getenv("TEST_DATABASE_URL") or os.getenv("test_database_url")
        if test_url and not os.getenv("DATABASE_URL"):
            os.environ["DATABASE_URL"] = test_url
        return cls()

settings = Settings.from_env()

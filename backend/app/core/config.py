from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field
from typing import List


class Settings(BaseSettings):
    app_name: str = "Retail ERP"
    environment: str = "development"
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = Field(..., alias="DATABASE_URL")

    cors_origins: List[AnyHttpUrl] = []
    
    admin_email: str = "admin@example.com"
    admin_password: str = "changeme"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()

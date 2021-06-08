from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    database_url: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
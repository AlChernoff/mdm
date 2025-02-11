import os
import urllib.parse
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_file: Path | None = Path(__file__).resolve().parent.parent / ".env.local"
if os.environ.get("_PYTEST_IS_RUNNING"):
    env_file = None


class AppSettings(BaseSettings):
    server_debug: bool = False
    env_name: str = ""

    model_config = SettingsConfigDict(env_file=env_file, extra="allow")


settings = AppSettings()


class DBSettings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_pass: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db_name: str = "postgres"
    echo_sql: bool = True

    def connection_string(self) -> str:
        postgres_pass = urllib.parse.quote_plus(self.postgres_pass)
        return f"postgresql+asyncpg://{self.postgres_user}:{postgres_pass}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"

    model_config = SettingsConfigDict(env_file=env_file, extra="allow")


db_settings = DBSettings()

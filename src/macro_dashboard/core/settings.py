from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # -------- runtime --------
    env: str = Field(default="local", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # -------- FRED --------
    fred_api_key: Optional[str] = Field(default=None, alias="FRED_API_KEY")
    fred_base_url: str = "https://api.stlouisfed.org/fred"
    fred_timeout_seconds: int = 10
    fred_retry_count: int = 3
    fred_rate_limit_per_sec: float = 3.0
    fred_backoff_max_seconds: float = 30.0

    # -------- Postgres / RDS --------
    db_host: Optional[str] = Field(default=None, alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="postgres", alias="DB_NAME")
    db_user: Optional[str] = Field(default=None, alias="DB_USER")
    db_password: Optional[str] = Field(default=None, alias="DB_PASSWORD")
    db_sslmode: Optional[str] = Field(default=None, alias="DB_SSLMODE")

    # Optional override if you prefer one variable instead of parts:
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")


    def postgres_dsn(self) -> str:
        """
        Returns a SQLAlchemy DSN.
        Prefers DATABASE_URL if set; otherwise builds from DB_* parts.
        """
        if self.database_url:
            return self.database_url

        if not (self.db_host and self.db_user and self.db_password):
            raise RuntimeError(
                "Set DATABASE_URL or set DB_HOST, DB_USER, and DB_PASSWORD."
            )

        ssl = f"?sslmode={self.db_sslmode}" if self.db_sslmode else ""
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}{ssl}"
        )


@lru_cache
def get_settings() -> Settings:
    s = Settings()

    # Enforce DB connectivity settings exist.
    _ = s.postgres_dsn()

    return s
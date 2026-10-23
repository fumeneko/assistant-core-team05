
"""Read and validate assistant configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

from assistant_core.errors import ConfigError


class Settings(BaseModel):
    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    llm_api_key: str | None = Field(default=None, repr=False)
    credit_rate_vnd: int = Field(default=450_000, gt=0)
    retake_multiplier: float = Field(default=1.5, gt=0)
    max_credits: int = Field(default=30, gt=0)
    log_level: str = "INFO"


def load_settings(env_file: str | None = ".env") -> Settings:
    """Load environment settings without exposing credentials."""
    if env_file is not None:
        load_dotenv(env_file, override=False)

    try:
        settings = Settings(
            data_dir=Path(os.getenv("ASSISTANT_DATA_DIR", "data")),
            llm_provider=os.getenv("LLM_PROVIDER", "stub"),
            llm_api_key=os.getenv("LLM_API_KEY") or None,
            credit_rate_vnd=int(os.getenv("CREDIT_RATE_VND", "450000")),
            retake_multiplier=float(
                os.getenv("RETAKE_MULTIPLIER", "1.5")
            ),
            max_credits=int(os.getenv("MAX_CREDITS", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
    except (ValueError, ValidationError):
        raise ConfigError("Invalid environment configuration") from None

    if settings.llm_provider != "stub" and not settings.llm_api_key:
        raise ConfigError(
            "LLM_API_KEY is required for a non-stub provider"
        )

    return settings

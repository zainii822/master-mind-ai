import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Locate marketmind directory root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(default="", validation_alias="OPENAI_API_KEY")
    DEFAULT_MODEL: str = Field(default="gpt-4o-mini", validation_alias="DEFAULT_MODEL")
    PLANNING_MODEL: str = Field(default="gpt-4o", validation_alias="PLANNING_MODEL")
    DEFAULT_TEMPERATURE: float = Field(default=0.2, validation_alias="DEFAULT_TEMPERATURE")
    REQUEST_TIMEOUT: float = Field(default=30.0, validation_alias="REQUEST_TIMEOUT")
    MAX_ITERATIONS: int = Field(default=10, validation_alias="MAX_ITERATIONS")
    MAX_BUDGET_USD: float = Field(default=1.00, validation_alias="MAX_BUDGET_USD")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

settings = Settings()

# Fallback check
if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == 'sk-""':
    settings.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
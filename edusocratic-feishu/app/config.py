import os
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "EduSocratic"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/edusocratic"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_MAX_RETRIES: int = 3
    ZHIPU_API_KEY: str = ""
    ZHIPU_MODEL: str = "glm-4"

    # Cost Circuit Breaker
    DAILY_LIMIT_PER_STUDENT: int = 20
    MONTHLY_BUDGET_PER_CLASS: float = 50.0
    PER_REQUEST_COST: float = 0.02

    # ASR
    ASR_PROVIDER: str = "xunfei"
    XUNFEI_APP_ID: str = ""
    XUNFEI_API_KEY: str = ""
    XUNFEI_API_SECRET: str = ""
    ASR_MIN_CONFIDENCE: float = 0.7

    # Feishu
    FEISHU_APP_ID: str = ""
    FEISHU_APP_SECRET: str = ""
    FEISHU_VERIFICATION_TOKEN: str = ""
    FEISHU_ENCRYPT_KEY: str = ""

    # Cache
    CACHE_TTL: int = 86400
    SIMHASH_THRESHOLD: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_yaml_config() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "base.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

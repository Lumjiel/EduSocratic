from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    # LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    llm_timeout: int = 30
    llm_max_retries: int = 2

    # 飞书
    feishu_app_id: str = ""
    feishu_app_secret: str = ""
    feishu_verification_token: str = ""
    feishu_encrypt_key: str = ""

    # 数据库
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/edusocratic"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # 配额
    daily_limit_per_student: int = 20
    monthly_budget_cents: int = 5000
    cache_ttl_seconds: int = 86400


settings = Settings()

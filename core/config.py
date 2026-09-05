from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    QWEN_API_KEY: str
    QWEN_MODEL: str = "qwen-plus"
    QWEN_BASE_URL: str

    DEEPSEEK_API_KEY: str | None = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"

    WECOM_CORP_ID: str
    WECOM_AGENT_ID: str
    WECOM_SECRET: str



settings = Settings()
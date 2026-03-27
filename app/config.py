from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hotspot Hub"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/hotspot_hub"
    refresh_interval_minutes: int = 30
    request_timeout_seconds: int = 15
    max_items_per_source: int = 50
    default_timezone: str = "Asia/Shanghai"
    admin_token: str = "change-me"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

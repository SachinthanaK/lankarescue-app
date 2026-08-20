from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    enable_demo_staff: bool = True
    allowed_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origin_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

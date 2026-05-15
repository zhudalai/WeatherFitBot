from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # API Keys
    openweather_api_key: str = ""
    openrouter_api_key: str = ""
    openrouter_model: str = "anthropic/claude-sonnet-4"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # App
    app_env: str = "development"
    app_port: int = 8000
    cors_origins: str = "http://localhost:5173"

    # Cache TTL (seconds)
    weather_cache_ttl: int = 900
    forecast_cache_ttl: int = 1800

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"
    CORS_ALLOW_ORIGINS: str = "*"
    DOWNLOAD_RATELIMIT: int = 0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        if self.CORS_ALLOW_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ALLOW_ORIGINS.split(",") if o.strip()]

    @property
    def llm_enabled(self) -> bool:
        return bool(self.OPENAI_API_KEY)


settings = Settings()

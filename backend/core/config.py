from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SIH Matchmaker"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str

    # CORS
    FRONTEND_URL: str = "http://localhost:5500"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

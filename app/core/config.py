from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    # SMTP_SERVER: str
    # SMTP_PORT: int
    # SMTP_USERNAME: str
    # SMTP_PASSWORD: str

@lru_cache()
def get_settings():
    return Settings()
from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sensitive Info Audit"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: SecretStr = "changethis"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # SQLite for the application's own database
    DATABASE_URL: str = "sqlite+aiosqlite:///./audit.db"

    class Config:
        env_file = ".env"

settings = Settings()

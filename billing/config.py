from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8081

    # DB
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    API_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()

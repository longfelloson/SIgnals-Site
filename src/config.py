from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AuthSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str


class Settings(AuthSettings, DatabaseSettings, BaseSettings):
    TEMPLATES_PATH: str
    STATIC_PATH: str


settings = Settings()

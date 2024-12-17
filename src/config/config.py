import os

from dotenv import load_dotenv
from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    #openssl rand -hex 32
    DB_URL: str = os.getenv("DB_URL")
    SECRET_KEY_JWT: str = '6493e95c7f0a9f34c051bd37622a16bde3a61910f60926abe975c27b75e37c64'
    ALGORITHM: str = 'HS256'
    MAIL_USERNAME: EmailStr = 'username@test.com'
    MAIL_PASSWORD: str = 'password'
    MAIL_FROM: str = 'from@test.com'
    MAIL_PORT: int = 435
    MAIL_SERVER: str = 'smtp.meta.com'
    REDIS_DOMAIN: str = 'mighty-flea-23780.upstash.io'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "AVzkAAIjcDFjOThlMzMwMWQ3ZDU0OTE4YTllYzhhODBiMDU4NDc5MnAxMA"
    CLD_NAME: str = 'cloud_name'
    CLD_API_KEY: str = 'api_key'
    CLD_API_SECRET: str = 'api'

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()

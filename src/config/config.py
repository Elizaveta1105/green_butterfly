from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #openssl rand -hex 32
    DB_URL: str = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"
    SECRET_KEY_JWT: str = '6493e95c7f0a9f34c051bd37622a16bde3a61910f60926abe975c27b75e37c64'
    ALGORITHM: str = 'HS256'
    MAIL_USERNAME: EmailStr = 'username@test.com'
    MAIL_PASSWORD: str = 'password'
    MAIL_FROM: str = 'from@test.com'
    MAIL_PORT: int = 435
    MAIL_SERVER: str = 'smtp.meta.com'
    REDIS_DOMAIN: str = 'ec2-34-247-151-18.eu-west-1.compute.amazonaws.com',
    REDIS_PORT: int = 19050
    REDIS_PASSWORD: str = "pf0c47bc798cd112e5dca21af6bced9c0fdf287f73f603918cef6d6012be24126"
    CLD_NAME: str = 'cloud_name'
    CLD_API_KEY: str = 'api_key'
    CLD_API_SECRET: str = 'api'

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


config = Settings()

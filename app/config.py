import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    x_token: str = os.getenv("X_TOKEN")


settings = Settings()

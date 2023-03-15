from pydantic import BaseSettings


class Settings(BaseSettings):
    AUTH_TOKEN: str
    PAGE_ID: str
    PATH_TO_FILE: str

    class Config:
        env_file = "env/.env"
        env_file_encoding = "utf-8"


settings = Settings()

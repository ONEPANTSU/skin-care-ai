from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
import os


class FilesConfig(BaseSettings):
    template_path: str = "templates"
    uploads_path: str = "files/uploads"
    processed_path: str = "files/processed"

    def create_dirs(self):
        dirs_to_create = [self.uploads_path, self.processed_path]
        for dir_to_create in dirs_to_create:
            if not os.path.exists(dir_to_create):
                os.makedirs(dir_to_create)


class AppConfig(BaseSettings):
    title: str = Field(alias="APP_TITLE")
    host: str = Field(alias="APP_HOST")
    port: int = Field(alias="APP_PORT")
    origins: list[str] = Field(alias="APP_ORIGINS")


class Config:
    def __init__(self, env_path: str = ".env"):
        load_dotenv(env_path)
        self.app = AppConfig()
        self.files = FilesConfig()

import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.router import Router
from src.config import Config
from src.service import Service


class App(FastAPI):
    def __init__(self, config: Config, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config.app
        super().__init__(*args, **kwargs, title=self.config.title)
        self.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.mount(
            f"/{config.files.processed_path}",
            StaticFiles(directory=config.files.processed_path),
            name="processed",
        )
        self.mount(
            f"/{config.files.uploads_path}",
            StaticFiles(directory=config.files.uploads_path),
            name="uploads",
        )
        service = Service(config.files)
        templates = Jinja2Templates(directory=config.files.template_path)
        router = Router(service, templates, config.files)
        self.include_router(router)

    def run(self):
        uvicorn.run(self, host=self.config.host, port=self.config.port)

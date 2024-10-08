import logging
import os
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.config import FilesConfig
from src.service import Service


class Router(APIRouter):
    def __init__(
        self,
        service: Service,
        templates: Jinja2Templates,
        files_config: FilesConfig,
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(prefix="", tags=["ai"])
        self.service = service
        self.templates = templates
        self.files_config = files_config
        self.add_api_route("/", self.get_upload_page, methods=["GET"])
        self.add_api_route("/upload/", self.upload, methods=["POST"])

    async def get_upload_page(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def upload(self, file: UploadFile = File(...)):
        try:
            unique_filename = f"{uuid4()}_{file.filename}"
            file_path = os.path.join(self.files_config.uploads_path, unique_filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            processed_files: list[str] = self.service.process_image(file_path)

            return JSONResponse({"success": True, "data": processed_files})

        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)})

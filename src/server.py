import os
import logging
from dataclasses import dataclass

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from src.skin_cv import process_image, PROCESSED_PATH


@dataclass
class Context:
    model: str | None = None


class App(FastAPI):
    ctx = Context()


app = App()

app.mount("/static", StaticFiles(directory="templates"), name="static")


@app.get("/")
async def read_index():
    logging.info("Serving index.html")
    return FileResponse("templates/index.html")


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    logging.info(f"Received file upload: {file.filename}")
    try:
        file_path = os.path.join(PROCESSED_PATH, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        processed_paths, cancer_classes = process_image(file_path, app.ctx.model)
        logging.info(
            f"Successfully processed image. Generated files: {processed_paths}"
        )
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "paths": processed_paths,
                    "cancer": cancer_classes
                },
            }
        )
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/processed/{filename}")
async def get_processed_image(filename: str):
    logging.info(f"Requested processed image: {filename}")
    file_path = os.path.join(PROCESSED_PATH, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    logging.warning(f"Processed image not found: {filename}")
    raise HTTPException(status_code=404, detail="File not found")

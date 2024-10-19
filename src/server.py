import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from skin_ai import process_image, PROCESSED_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

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

        processed_paths = process_image(file_path)
        logging.info(
            f"Successfully processed image. Generated files: {processed_paths}"
        )
        return JSONResponse(content={"success": True, "data": processed_paths})
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


if __name__ == "__main__":
    port = 8080
    logging.info(f"Server starting on http://localhost:{port}")
    uvicorn.run(app, host="localhost", port=port)

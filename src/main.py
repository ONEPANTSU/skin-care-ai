import argparse
import logging
import sys

import uvicorn

from src.server import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skin disease detection")
    parser.add_argument("--port", "-p", type=int, help="Server's port", default=8080)
    parser.add_argument(
        "--model", "-m", type=str, help="Detection model", default="yolo"
    )
    port = parser.parse_args().port
    app.ctx.model = parser.parse_args().model

    logging.info(f"Server starting on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

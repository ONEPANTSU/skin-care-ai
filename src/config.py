import os

from dotenv import load_dotenv

load_dotenv(".env")

PROCESSED_PATH = "files/processed"
GPT_API_KEY = os.environ.get("GPT_API_KEY")
TESSDATA_DIR = (
    r'--tessdata-dir "/opt/homebrew/Cellar/tesseract/5.4.1_2/share/tessdata/"'
)

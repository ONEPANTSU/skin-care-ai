import os

from ultralytics import YOLO

from src.config import PROCESSED_PATH

acne_model = YOLO("models/yolo.pt")


def process_image(image_path: str):
    result = acne_model(image_path)
    file_name = os.path.basename(image_path)
    name, ext = os.path.splitext(file_name)
    save_path = os.path.join(PROCESSED_PATH, f"{name}_yolo{ext}")
    result[0].save(filename=save_path, labels=False, conf=False)
    return os.path.basename(save_path)

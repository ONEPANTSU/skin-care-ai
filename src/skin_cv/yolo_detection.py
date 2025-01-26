import os

from ultralytics import YOLO

from src.config import PROCESSED_PATH

cancer_model = YOLO("models/yolo.pt")


def process_image(image_path: str):
    results = cancer_model(image_path)
    file_name = os.path.basename(image_path)
    name, ext = os.path.splitext(file_name)
    save_path = os.path.join(PROCESSED_PATH, f"{name}_yolo{ext}")
    results[0].save(filename=save_path, labels=True, conf=True)
    classes = [results[0].names[int(cls)] for r in results for cls in r.boxes.cls]
    return os.path.basename(save_path), classes

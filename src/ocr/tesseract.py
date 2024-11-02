import pytesseract
from PIL import Image
from textblob import TextBlob


def process_image_to_text(
    image_path: str,
) -> str:
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def process_image_with_confidences(
    image_path: str,
) -> tuple[str, float]:
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    confidences = [float(conf) / 100 for conf in data["conf"] if conf != "-1"]
    if confidences:
        overall_confidence = sum(confidences) / len(confidences)
    else:
        overall_confidence = 0
    text = " ".join(data.get("text", []))
    return text, overall_confidence


def recognize_text_if_sure(image_path) -> str | None:
    text, confidence = process_image_with_confidences(image_path)
    if confidence > 0.5:
        return str(TextBlob(text).correct())
    return None

import easyocr
from textblob import TextBlob


def process_image_to_text(image_path: str, lang_list: list[str] | None = None) -> str:
    if not lang_list:
        lang_list = ["en"]
    reader = easyocr.Reader(lang_list)
    return "\n".join(reader.readtext(image_path, detail=0))


def process_image_with_confidences(image_path: str) -> tuple[str, float]:
    lang_list = ["en", "ch_sim"]
    reader = easyocr.Reader(lang_list)
    data = reader.readtext(image_path, detail=1)
    texts = []
    confidences = []
    for _, txt, confidence in data:
        texts.append(txt)
        confidences.append(confidence)
    overall_confidence = sum(confidences) / len(confidences)
    return " ".join(texts), overall_confidence


def recognize_text_if_sure(image_path: str) -> str | None:
    text, confidence = process_image_with_confidences(image_path)
    if confidence > 0.5:
        return str(TextBlob(text).correct())
    return None

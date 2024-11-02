import logging

from src.ocr import tesseract, easyocr
from src.ocr.llm_comparator import compare_texts


def recognize_text(image_path: str) -> str:
    # lightweight tesseract recognition
    if text := tesseract.recognize_text_if_sure(image_path):
        logging.info("Text recognized by tesseract")
        return text

    # lightweight easyocr recognition
    if text := easyocr.recognize_text_if_sure(image_path):
        logging.info("Text recognized by easyocr")
        return text

    # heavy ensemble recognition
    ocr_models_result = {
        "tesseract_en": tesseract.process_image_to_text(image_path),
        "easyocr_en": easyocr.process_image_to_text(image_path, ["en"]),
        "easyocr_ch": easyocr.process_image_to_text(image_path, ["ch_sim"]),
        "easyocr_en_ch": easyocr.process_image_to_text(image_path, ["en", "ch_sim"]),
    }
    text = compare_texts(ocr_models_result)
    logging.info("Text recognized by ensemble")
    return text

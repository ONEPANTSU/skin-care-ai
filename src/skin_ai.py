import os
import cv2
import numpy as np
import mediapipe as mp
from typing import List
import logging

from src import clip_detection, yolo_detection
from src.config import PROCESSED_PATH

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

os.makedirs(PROCESSED_PATH, exist_ok=True)


def increase_contrast(input_image):
    logging.info("Increasing image contrast")
    lab_color_space = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
    lightness_channel, a_channel, b_channel = cv2.split(lab_color_space)
    clahe_processor = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_lightness = clahe_processor.apply(lightness_channel)
    merged_image = cv2.merge((enhanced_lightness, a_channel, b_channel))
    output_image = cv2.cvtColor(merged_image, cv2.COLOR_LAB2BGR)
    return output_image


def remove_face(image):
    logging.info(f"Initial image shape: {image.shape}, dtype: {image.dtype}")
    mp_face_mesh = mp.solutions.face_mesh

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
    ) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            mask = np.ones_like(image, dtype=np.uint8) * 255
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = image.shape
                landmarks = np.array(
                    [(int(pt.x * w), int(pt.y * h)) for pt in face_landmarks.landmark]
                )

                eye_indices = [
                    33,
                    133,
                    159,
                    145,
                    153,
                    154,
                    155,
                    133,
                    362,
                    263,
                    386,
                    374,
                    380,
                    381,
                    382,
                ]
                mouth_indices = [
                    61,
                    291,
                    0,
                    17,
                    13,
                    14,
                    17,
                    84,
                    91,
                    181,
                    146,
                    61,
                ]  # Контур рта

                left_eye_pts = landmarks[eye_indices[: len(eye_indices) // 2]]
                right_eye_pts = landmarks[eye_indices[len(eye_indices) // 2 :]]
                mouth_pts = landmarks[mouth_indices]

                cv2.fillPoly(mask, [left_eye_pts], (0, 0, 0))
                cv2.fillPoly(mask, [right_eye_pts], (0, 0, 0))
                cv2.fillPoly(mask, [mouth_pts], (0, 0, 0))

            image = cv2.bitwise_and(image, mask)

    return image


def detect_acne(image):
    logging.info("Detecting acne")
    image_without_bg = remove_background(image.copy())
    removed_face = remove_face(image_without_bg.copy())
    contrasted = increase_contrast(removed_face.copy())
    gray_image = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, threshold_image = cv2.threshold(blurred_image, 140, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(
        threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return image


def detect_redness(image):
    logging.info("Detecting redness")
    image_without_bg = remove_background(image.copy())
    removed_face = remove_face(image_without_bg.copy())
    hsv = cv2.cvtColor(removed_face, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.add(mask1, mask2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [
        contour for contour in contours if 10000 < cv2.contourArea(contour) < 1000000
    ]
    cv2.drawContours(image, filtered_contours, -1, (255, 0, 0), 2)
    return image


def detect_uneven_tone(image):
    logging.info("Detecting uneven tone")
    image_without_bg = remove_background(image.copy())
    removed_face = remove_face(image_without_bg.copy())
    contrasted = increase_contrast(removed_face.copy())
    gray = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)
    uneven_tone_image = cv2.Laplacian(gray, cv2.CV_64F)
    uneven_tone_image = np.uint8(np.absolute(uneven_tone_image))
    _, mask = cv2.threshold(uneven_tone_image, 30, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [
        contour for contour in contours if 500 < cv2.contourArea(contour) < 1000000
    ]
    cv2.drawContours(image, filtered_contours, -1, (255, 0, 0), 2)
    return image


def save_image(image, problem_type, original_image_path):
    logging.info(f"Saving {problem_type} image")
    file_name = os.path.basename(original_image_path)
    name, ext = os.path.splitext(file_name)
    save_path = os.path.join(PROCESSED_PATH, f"{name}_{problem_type}{ext}")
    cv2.imwrite(save_path, image)
    return os.path.basename(save_path)


def remove_background(image):
    mask = np.zeros(image.shape[:2], np.uint8)
    rect = (50, 50, image.shape[1] - 50, image.shape[0] - 50)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    return image * mask2[:, :, np.newaxis]


def process_image(image_path: str) -> List[str]:
    logging.info(f"Processing image: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image at {image_path}")

    yolo_path = yolo_detection.process_image(image_path)
    clip_path = clip_detection.process_image(image_path, 64)

    acne_image = detect_acne(image.copy())
    redness_image = detect_redness(image.copy())
    uneven_tone_image = detect_uneven_tone(image.copy())

    paths = [yolo_path, clip_path]
    for img, problem in (
        (acne_image, "acne"),
        (redness_image, "redness"),
        (uneven_tone_image, "uneven_tone"),
    ):
        paths.append(save_image(img, problem, image_path))

    logging.info(f"Image processing complete. Generated files: {paths}")
    return paths

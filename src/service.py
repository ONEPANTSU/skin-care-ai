import os
import cv2
import numpy as np
from src.config import FilesConfig


class Service:
    def __init__(self, files_config: FilesConfig):
        self.processed_path = files_config.processed_path

    def process_image(self, image_path: str) -> list[str]:
        image = cv2.imread(image_path)
        acne_image = self.detect_acne(image.copy())
        redness_image = self.detect_redness(image.copy())
        uneven_tone_image = self.detect_uneven_tone(image.copy())

        paths = []
        for img, problem in (
            (acne_image, "acne"),
            (redness_image, "redness"),
            (uneven_tone_image, "uneven_tone"),
        ):
            paths.append(self.save_image(img, problem, image_path))
        return paths

    @staticmethod
    def increase_contrast(input_image):
        lab_color_space = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
        lightness_channel, a_channel, b_channel = cv2.split(lab_color_space)
        clahe_processor = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_lightness = clahe_processor.apply(lightness_channel)
        merged_image = cv2.merge((enhanced_lightness, a_channel, b_channel))
        output_image = cv2.cvtColor(merged_image, cv2.COLOR_LAB2BGR)
        return output_image

    def detect_acne(self, image):
        contrasted = self.increase_contrast(image.copy())
        gray_image = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        _, threshold_image = cv2.threshold(
            blurred_image, 140, 255, cv2.THRESH_BINARY_INV
        )
        contours, _ = cv2.findContours(
            threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for contour in contours:
            if 10000 > cv2.contourArea(contour) > 150:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return image

    @staticmethod
    def detect_redness(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
            contour
            for contour in contours
            if 10000 < cv2.contourArea(contour) < 1000000
        ]
        cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 2)

        return image

    def detect_uneven_tone(self, image):
        contrasted = self.increase_contrast(image.copy())
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
        cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 2)
        return image

    def save_image(self, image, problem_type, original_image_path):
        file_name = os.path.basename(original_image_path)
        name, ext = os.path.splitext(file_name)
        save_path = os.path.join(self.processed_path, f"{name}_{problem_type}{ext}")
        cv2.imwrite(save_path, image)
        return save_path

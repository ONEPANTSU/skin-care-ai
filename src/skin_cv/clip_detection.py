import os

import torch
import clip
from PIL import ImageDraw
import numpy as np
from PIL import Image

from src.config import PROCESSED_PATH


def divide_image(image_path, segment_size):
    image = Image.open(image_path)
    width, height = image.size
    segments = []

    for top in range(0, height, segment_size):
        for left in range(0, width, segment_size):
            box = (left, top, left + segment_size, top + segment_size)
            segment = image.crop(box)
            segments.append((segment, box))

    return segments, image


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("models/clip.pt", device=device)

labels = [
    "skin with trouble (acne, pimples, wrinkles, redness)",
    "part of face (eye, nose, hair, ear)",
    "no skin trouble (clear skin, no skin)",
]


def classify_segment(segment):
    image = preprocess(segment).unsqueeze(0).to(device)
    text_inputs = torch.cat([clip.tokenize(label) for label in labels]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text_inputs)

        logits_per_image = (image_features @ text_features.T).softmax(dim=-1)
        probs = logits_per_image.cpu().numpy()

    max_prob_label = labels[np.argmax(probs)]
    if max_prob_label == labels[0]:
        return True, max_prob_label
    else:
        return False, "clear skin"


def mark_segments(image, segments):
    draw = ImageDraw.Draw(image)

    for segment, box in segments:
        has_issues, label = classify_segment(segment)
        if has_issues:
            draw.rectangle(box, outline="blue", width=1)

    return image


def process_image(image_path, segment_size=64):
    segments, full_image = divide_image(image_path, segment_size)
    marked_image = mark_segments(full_image, segments)

    file_name = os.path.basename(image_path)
    name, ext = os.path.splitext(file_name)
    save_path = os.path.join(PROCESSED_PATH, f"{name}_clip{ext}")
    marked_image.save(save_path)
    return os.path.basename(save_path)

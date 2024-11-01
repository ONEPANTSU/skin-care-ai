#!/bin/bash

if [ -z "$1" ]; then
  echo "Please specify a model name: clip or yolo"
  exit 1
fi

mkdir -p /app/models

case "$1" in
  clip)
    echo "Downloading CLIP model..."
    curl -L -o /app/models/clip.pt https://openaipublic.azureedge.net/clip/models/5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f/ViT-B-16.pt
    ;;
  yolo)
    echo "Downloading YOLO model..."
    curl -L -o /app/models/yolo.pt https://huggingface.co/Tinny-Robot/acne/resolve/main/acne.pt
    ;;
  *)
    echo "Invalid model name. Please specify either 'clip' or 'yolo'."
    exit 1
    ;;
esac

echo "Model downloaded successfully to /app/models/"

# skin-care-ai

## 📖 Описание
Проект представляет собой приложение по уходу за кожей с использованием ИИ. Сервер обрабатывает изображения лиц, 
увеличивая контрастность и выделяя области с акне, прыщами, покраснениями и неровным тоном кожи. 
Пользователи могут загружать свои фотографии, а в ответ получат несколько изображений с обозначенными областями интереса.

## ⭐️ Запуск приложения
Скачайте необходимые модели и разместите их в директории `/models`: 
- [models/yolo.pt](https://huggingface.co/Tinny-Robot/acne/resolve/main/acne.pt)
- [models/ViT-B-16.pt](https://openaipublic.azureedge.net/clip/models/5806e77cd80f8b59890b7e101eabd078d9fb84e6937f9e85e4ecb61988df416f/ViT-B-16.pt)

Установите зависимости:
```bash
pip install -r requirements.txt
```
Запустите сервер
```bash
python src/server.py
```
## 🖼️ Пример работы приложения
![files/example.jpg](files/example.jpg)

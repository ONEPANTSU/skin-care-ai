.SILENT:

run:
	python -m src.main

docker-build:
	docker build -f docker/Dockerfile-app . -t skin-care-app --build-arg MODEL=$(MODEL)

docker-run:
	docker run -d --name skin-care-app -p $(PORT):$(PORT) -v ./files/processed:/app/files/processed skin-care-app -p $(PORT)

docker-compose-run:
	docker-compose build
	docker-compose up
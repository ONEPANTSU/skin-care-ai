.SILENT:

run:
	python -m src.main -m $(MODEL)

docker-build:
	docker build -f docker/Dockerfile-app . -t skin-care-app --build-arg MODEL=$(MODEL)

docker-run:
	docker run -d --name skin-care-app -p $(PORT):$(PORT) -v ./files/processed:/app/files/processed skin-care-app -p $(PORT)

compose-run:
	docker-compose -d -f docker-compose.yaml --env-file .env up --build
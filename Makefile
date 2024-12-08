.SILENT:

run:
	python -m src.main -m $(MODEL)

docker-build:
	docker build -f docker/Dockerfile-app . -t skincare-cv --build-arg MODEL=$(MODEL)

docker-run:
	docker run -d --name skincare-cv -p $(PORT):$(PORT) -v ./files/processed:/app/files/processed skincare-cv -p $(PORT)

compose-run:
	docker-compose -d -f docker-compose.yaml --env-file .env up --build

push-images:
	docker build -f docker/Dockerfile-app . -t onepantsu/skincare-cv:v1.0-clip --build-arg MODEL=clip
	docker push onepantsu/skincare-cv:v1.0-clip
	docker build -f docker/Dockerfile-jupyter . -t onepantsu/skincare-genegpt:v1.0
	docker push onepantsu/skincare-genegpt:v1.0
	docker build -f docker/Dockerfile-migrations . -t onepantsu/skincare-migrations:v1.0
	docker push onepantsu/skincare-migrations:v1.0

minikube-run:
	. ./k8s/minikube-up.sh

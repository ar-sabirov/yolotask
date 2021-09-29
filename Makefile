build:
	docker-compose build
	pip install -r requirements-dev.txt

start:
	docker-compose up -d

stop:
	docker-compose down

test:
	docker-compose up -d --remove-orphans
	-PYTHONPATH=. pytest
	docker-compose down

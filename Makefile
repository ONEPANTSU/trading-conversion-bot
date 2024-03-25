PHONY:
.SILENT:

run:
	python3 run.py

build:
	docker-compose build
	docker-compose push

up:
	docker-compose up -d

down:
	docker-compose down

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

revision:
	alembic revision --autogenerate -m "$(name)"

bash-bot:
	docker exec -it trading-conversion-bot bash

bash-db:
	docker exec -it trading-conversion-bot-db bash

black:
	black src -l 79
include .env

ENV_FILE = .env

install:
	@echo "Installing dependencies..."
	pyenv install 3.11.4 --skip-existing
	pyenv local 3.11.4
	curl -sSL https://install.python-poetry.org | python3 - --version 1.7.1
	poetry install --no-root --sync
	poetry self add poetry-dotenv-plugin

activate:
	@echo "Activating virtual environment..."
	poetry shell

compose-start:
	docker compose --env-file $(ENV_FILE)\
	 up -d

compose-stop:
	docker compose down

compose-build:
	docker compose build

docker-delete-volumes:
	docker volume prune -f

start-ngrok:
	ngrok http --domain=${NGROK_DOMIAN} 8080

run-with-clean-db: compose-stop docker-delete-volumes compose-build compose-start
	uvicorn app.main:app --reload --port 8080

clean:
	@echo "Cleaning env and hooks..."
	deactivate || exit 0
	rm -rf ./.git/hooks
	rm -rf ./.venv/
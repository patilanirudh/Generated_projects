.PHONY: install dev test lint run docker-build docker-up clean

install:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	PYTHONPATH=src uvicorn spacexinsight.main:app --reload --port 8000

test:
	PYTHONPATH=src pytest -q --cov=src --cov-report=term-missing

lint:
	ruff check src tests

docker-build:
	docker build -t SpaceXInsight .

docker-up:
	docker compose up --build

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov **/__pycache__

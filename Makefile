.PHONY: install dev test lint format run clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev: ## Install all dependencies (production + dev)
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	python -m pytest tests/ -v

coverage: ## Run tests with coverage report
	python -m pytest tests/ --cov=. --cov-report=term-missing --cov-config=setup.cfg

lint: ## Run linter
	python -m flake8 chatbot_backend.py tests/

format: ## Auto-format code with black
	python -m black chatbot_backend.py tests/

check: lint test ## Run lint + tests (use before committing)

run: ## Start the chatbot server
	python chatbot_backend.py

clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; \
	rm -rf htmlcov .coverage; true

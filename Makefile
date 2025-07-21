# E-Commerce FastAPI Backend Makefile

.PHONY: help install dev test clean run deploy lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  dev         Install development dependencies"
	@echo "  test        Run all tests"
	@echo "  run         Start the development server"
	@echo "  run-prod    Start the production server"
	@echo "  clean       Clean up cache and temporary files"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  deploy      Deploy to production"

# Install dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Install development dependencies
dev: install
	pip install pytest pytest-asyncio httpx black flake8 mypy

# Run tests
test:
	python tests/run_all_tests.py

# Run quick tests
test-quick:
	python -m pytest tests/ -x --tb=short

# Start development server
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start production server
run-prod:
	python scripts/start.py

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Code formatting
format:
	black app/ tests/ main.py
	isort app/ tests/ main.py

# Linting
lint:
	flake8 app/ main.py
	mypy app/ main.py

# Deploy to Render
deploy:
	git add .
	git commit -m "Deploy update"
	git push origin master

# Setup development environment
setup: install dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the development server"

# Database operations
db-test:
	python tests/test_mongodb.py

# Health check
health:
	curl -s http://localhost:8000/health | python -m json.tool

# API documentation
docs:
	@echo "API documentation available at:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc: http://localhost:8000/redoc"
